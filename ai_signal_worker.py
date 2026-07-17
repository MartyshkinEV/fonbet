"""Public-line signal worker for the dashboard.

This worker does not authenticate, does not read account data, and does not
place bets. It fetches a public Fonbet events feed, extracts live tennis markets,
and writes analytical signals for the dashboard.
"""

from __future__ import annotations

import json
import os
import time
import gzip
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

TENNIS_DIR = Path(os.environ.get("TENNIS_API_DIR", "/opt/fonbet_suite/tenniss_api")).resolve()
ARTIFACTS_DIR = Path(os.environ.get("ARTIFACTS_DIR", TENNIS_DIR / "artifacts")).resolve()
LIVE_DIR = ARTIFACTS_DIR / "live_betting"
INTERVAL = int(os.environ.get("AI_WORKER_INTERVAL_SECONDS", "20"))
FEED_URL = os.environ.get(
    "FONBET_FEED_URL",
    "https://line-lb54-w.bk6bba-resources.com/ma/events/list?lang=en&version=72519110016&scopeMarket=1600",
)
USER_AGENT = os.environ.get(
    "FONBET_USER_AGENT",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
)

MARKET_SNAPSHOTS_PATH = LIVE_DIR / "market_snapshots.jsonl"
EVENT_WATCH_PATH = LIVE_DIR / "event_ml_watch.jsonl"
PROCESS_LOG_PATH = LIVE_DIR / "process_log.jsonl"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def log(stage: str, status: str, message: str, **extra: Any) -> None:
    append_jsonl(
        PROCESS_LOG_PATH,
        {
            "timestamp_utc": now_iso(),
            "stage": stage,
            "status": status,
            "message": message,
            **extra,
        },
    )


def fetch_payload() -> dict[str, Any]:
    request = Request(
        FEED_URL,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json,text/plain,*/*",
            "Origin": "https://fon.bet",
            "Referer": "https://fon.bet/",
        },
    )
    with urlopen(request, timeout=12) as response:
        body = response.read()
    if body[:2] == b"\x1f\x8b":
        body = gzip.decompress(body)
    payload = json.loads(body.decode("utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("unexpected feed payload")
    return payload


def sports_maps(payload: dict[str, Any]) -> tuple[dict[int, dict[str, Any]], set[int]]:
    sports = payload.get("sports") or []
    sports_by_id = {
        int(item["id"]): item
        for item in sports
        if isinstance(item, dict) and item.get("id") not in (None, "")
    }

    def root_id(sport_id: int) -> int:
        current = sports_by_id.get(sport_id, {})
        seen: set[int] = set()
        while isinstance(current, dict):
            parent = current.get("parentId")
            if parent in (None, ""):
                return int(current.get("id") or sport_id)
            try:
                parent_id = int(parent)
            except (TypeError, ValueError):
                return sport_id
            if parent_id in seen:
                return sport_id
            seen.add(parent_id)
            current = sports_by_id.get(parent_id, {})
        return sport_id

    tennis_sports = {sport_id for sport_id in sports_by_id if root_id(sport_id) == 4}
    return sports_by_id, tennis_sports


def factors_by_event(payload: dict[str, Any]) -> dict[int, dict[int, dict[str, Any]]]:
    out: dict[int, dict[int, dict[str, Any]]] = {}
    for item in payload.get("customFactors") or []:
        if not isinstance(item, dict) or item.get("e") in (None, ""):
            continue
        event_id = int(item["e"])
        factors: dict[int, dict[str, Any]] = {}
        for factor in item.get("factors") or []:
            if isinstance(factor, dict) and factor.get("f") not in (None, ""):
                factors[int(factor["f"])] = factor
        out[event_id] = factors
    return out


def normalized_probability(odds_a: float, odds_b: float) -> tuple[float, float]:
    implied_a = 1.0 / odds_a
    implied_b = 1.0 / odds_b
    total = implied_a + implied_b
    if total <= 0:
        return 0.0, 0.0
    return implied_a / total, implied_b / total


def score_market(event: dict[str, Any], competition: str, factors: dict[int, dict[str, Any]]) -> dict[str, Any] | None:
    p1_factor = factors.get(921)
    p2_factor = factors.get(923)
    if not p1_factor or not p2_factor:
        return None
    try:
        p1_odds = float(p1_factor["v"])
        p2_odds = float(p2_factor["v"])
    except (KeyError, TypeError, ValueError):
        return None
    if p1_odds <= 1 or p2_odds <= 1:
        return None

    p1_prob, p2_prob = normalized_probability(p1_odds, p2_odds)

    options = [
        ("player1", event.get("team1") or "player1", p1_prob, p1_odds),
        ("player2", event.get("team2") or "player2", p2_prob, p2_odds),
    ]
    scored_options = []
    for side, selection, probability, odds in options:
        if not 1.55 <= odds <= 3.50:
            continue
        confidence = abs(p1_prob - p2_prob)
        odds_fit = max(0.0, 1.0 - abs(odds - 2.05) / 1.50)
        score = probability * 0.55 + confidence * 0.20 + odds_fit * 0.25
        scored_options.append((score, side, selection, probability, odds))
    if not scored_options:
        return None

    score, side, selection, selected_prob, selected_odds = max(scored_options, key=lambda item: item[0])
    signal_score = round(score, 4)
    return {
        "timestamp_utc": now_iso(),
        "status": "candidate",
        "stage": "public_line_scoring",
        "event_id": event.get("id"),
        "market_id": str(event.get("id")),
        "market_type": "match_winner",
        "competition": competition,
        "player1_name": event.get("team1") or "",
        "player2_name": event.get("team2") or "",
        "selection_side": side,
        "selection_name": selection,
        "selected_player_name": selection,
        "selected_side": side,
        "odds": selected_odds,
        "selected_odds": selected_odds,
        "model_probability": round(selected_prob, 4),
        "selected_probability": round(selected_prob, 4),
        "implied_probability": round(1.0 / selected_odds, 4),
        "edge": 0.0,
        "ranking_score": signal_score,
        "source": "public_feed",
        "note": "public-line analytical signal; no account login; no bet placement",
    }


def extract_cycle(payload: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    sports_by_id, tennis_sports = sports_maps(payload)
    factor_map = factors_by_event(payload)
    events = payload.get("events") or []
    live_tennis: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []

    for event in events:
        if not isinstance(event, dict):
            continue
        if event.get("place") != "live" or event.get("level") != 1:
            continue
        try:
            sport_id = int(event.get("sportId"))
            event_id = int(event.get("id"))
        except (TypeError, ValueError):
            continue
        if sport_id not in tennis_sports:
            continue

        competition = str((sports_by_id.get(sport_id) or {}).get("name") or "")
        live_tennis.append(
            {
                "timestamp_utc": now_iso(),
                "event_id": event_id,
                "sport_id": sport_id,
                "competition": competition,
                "team1": event.get("team1") or "",
                "team2": event.get("team2") or "",
                "place": event.get("place"),
                "level": event.get("level"),
            }
        )
        candidate = score_market(event, competition, factor_map.get(event_id, {}))
        if candidate is not None:
            candidates.append(candidate)

    candidates.sort(key=lambda item: float(item.get("ranking_score") or 0), reverse=True)
    return live_tennis, candidates


def run_cycle() -> None:
    log("fetch", "started", "Запрашиваю публичную линию Fonbet", url=FEED_URL)
    payload = fetch_payload()
    log(
        "fetch",
        "ok",
        "Линия получена",
        sports=len(payload.get("sports") or []),
        events=len(payload.get("events") or []),
        custom_factors=len(payload.get("customFactors") or []),
    )

    live_tennis, candidates = extract_cycle(payload)
    log("extract", "ok", "Live tennis события извлечены", live_tennis=len(live_tennis))

    for market in live_tennis[:200]:
        append_jsonl(MARKET_SNAPSHOTS_PATH, market)
    for candidate in candidates[:50]:
        append_jsonl(EVENT_WATCH_PATH, candidate)

    log(
        "score",
        "ok",
        "Scoring завершён",
        candidates=len(candidates),
        top_score=candidates[0]["ranking_score"] if candidates else 0,
    )


def main() -> None:
    LIVE_DIR.mkdir(parents=True, exist_ok=True)
    log("worker", "started", "AI signal worker запущен", interval_seconds=INTERVAL)
    while True:
        try:
            run_cycle()
        except Exception as exc:
            log("worker", "error", "Ошибка цикла сбора/scoring", error=str(exc))
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
