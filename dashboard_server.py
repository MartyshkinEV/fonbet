"""Read-only dashboard for the local Fonbet and tennis ML repositories.

The dashboard does not log in to bookmaker accounts and does not place bets. It
exposes repository status and local analytical artifacts so the deployed service
is safe to keep online.
"""

from __future__ import annotations

import html
import json
import os
import subprocess
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent
TENNIS_DIR = Path(os.environ.get("TENNIS_API_DIR", BASE_DIR.parent / "tenniss_api")).resolve()
PORT = int(os.environ.get("PORT", "8011"))
HOST = os.environ.get("HOST", "0.0.0.0")


def run_git(repo: Path, *args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(repo), *args],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=3,
        ).strip()
    except Exception:
        return ""


def repo_status(repo: Path) -> dict[str, Any]:
    return {
        "path": str(repo),
        "exists": repo.exists(),
        "branch": run_git(repo, "rev-parse", "--abbrev-ref", "HEAD"),
        "commit": run_git(repo, "rev-parse", "--short", "HEAD"),
        "dirty": bool(run_git(repo, "status", "--porcelain")),
    }


def file_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False, "size": 0, "updated": None, "age_seconds": None}
    stat = path.stat()
    now = datetime.now(timezone.utc).timestamp()
    return {
        "exists": True,
        "size": stat.st_size,
        "updated": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "age_seconds": max(0, round(now - stat.st_mtime)),
    }


def read_jsonl_tail(path: Path, limit: int = 40) -> list[dict[str, Any]]:
    if not path.exists() or not path.is_file():
        return []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[-limit:]
    except OSError:
        return []
    rows = []
    for line in lines:
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            payload["_source_file"] = path.name
            rows.append(payload)
    return rows


def live_paths() -> dict[str, Path]:
    live_dir = TENNIS_DIR / "artifacts" / "live_betting"
    return {
        "decisions": live_dir / "decisions.jsonl",
        "recommendations": live_dir / "rl_recommendations.jsonl",
        "actions": live_dir / "rl_actions.jsonl",
        "outcomes": live_dir / "rl_outcomes.jsonl",
        "event_watch": live_dir / "event_ml_watch.jsonl",
        "market_snapshots": live_dir / "market_snapshots.jsonl",
        "process_log": live_dir / "process_log.jsonl",
    }


def ai_process_data() -> dict[str, Any]:
    paths = live_paths()
    streams = {name: file_state(path) for name, path in paths.items()}
    raw_events: list[dict[str, Any]] = []
    for name in ("recommendations", "decisions", "event_watch", "actions"):
        raw_events.extend(read_jsonl_tail(paths[name], limit=60))

    candidates = []
    for event in raw_events[-80:]:
        probability = event.get("selected_probability") or event.get("model_probability") or event.get("probability")
        odds = event.get("selected_odds") or event.get("odds") or event.get("value")
        candidates.append(
            {
                "event_id": event.get("event_id") or event.get("eventId") or event.get("id") or "",
                "match": " - ".join(str(part) for part in (event.get("player1_name") or event.get("team1"), event.get("player2_name") or event.get("team2")) if part),
                "market_type": event.get("market_type") or event.get("action") or event.get("stage") or "",
                "selection": event.get("selected_player_name") or event.get("selection_name") or event.get("selected_side") or "",
                "probability": probability,
                "odds": odds,
                "edge": event.get("selected_edge") or event.get("edge"),
                "score": event.get("ranking_score") or 0,
                "source": event.get("_source_file") or "",
                "timestamp": event.get("timestamp_utc") or event.get("created_at") or "",
            }
        )
    candidates.sort(key=lambda item: float(item.get("score") or 0), reverse=True)

    active_files = sum(1 for state in streams.values() if state["exists"] and state["size"] > 0)
    recent_files = sum(
        1
        for state in streams.values()
        if state["exists"] and state["age_seconds"] is not None and state["age_seconds"] < 600
    )
    pipeline = [
        {"name": "Сбор линии", "status": "active" if streams["market_snapshots"]["exists"] else "waiting"},
        {"name": "Нормализация рынков", "status": "active" if active_files else "waiting"},
        {"name": "ML scoring", "status": "active" if streams["decisions"]["exists"] or streams["event_watch"]["exists"] else "waiting"},
        {"name": "Фильтр риска", "status": "active" if streams["recommendations"]["exists"] or streams["actions"]["exists"] else "waiting"},
        {"name": "Кандидаты", "status": "active" if candidates else "waiting"},
    ]
    return {
        "safe_mode": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "active_files": active_files,
            "recent_files": recent_files,
            "candidate_count": len(candidates),
            "top_score": candidates[0]["score"] if candidates else 0,
        },
        "pipeline": pipeline,
        "streams": streams,
        "candidates": candidates[:30],
        "process_log": read_jsonl_tail(paths["process_log"], limit=30)[-15:],
        "note": "Analytical dashboard only: no account login, no credentials, no bet placement.",
    }


def dashboard_data() -> dict[str, Any]:
    return {
        "safe_mode": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fonbet_repo": repo_status(BASE_DIR),
        "tennis_repo": repo_status(TENNIS_DIR),
        "ai_process": ai_process_data(),
        "disabled_actions": [
            "bookmaker_login",
            "credential_storage",
            "balance_check",
            "coupon_submit",
            "auto_betting",
        ],
    }


def page() -> bytes:
    data = dashboard_data()
    rows = "".join(
        "<tr>"
        f"<td>{html.escape(str(item.get('score', '')))}</td>"
        f"<td>{html.escape(str(item.get('match') or item.get('event_id') or ''))}</td>"
        f"<td>{html.escape(str(item.get('market_type', '')))}</td>"
        f"<td>{html.escape(str(item.get('selection', '')))}</td>"
        f"<td>{html.escape(str(item.get('probability', '')))}</td>"
        f"<td>{html.escape(str(item.get('odds', '')))}</td>"
        f"<td>{html.escape(str(item.get('source', '')))}</td>"
        "</tr>"
        for item in data["ai_process"]["candidates"]
    )
    pipeline = "".join(
        f"<li><b>{html.escape(step['name'])}</b>: {html.escape(step['status'])}</li>"
        for step in data["ai_process"]["pipeline"]
    )
    body = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Fonbet dashboard</title>
  <style>
    body {{ margin:0; font-family:Arial,sans-serif; background:#eef3f8; color:#17202a; }}
    header {{ padding:24px; color:#fff; background:#111827; }}
    main {{ max-width:1200px; margin:0 auto; padding:18px; display:grid; gap:14px; }}
    section {{ background:#fff; border:1px solid #d8dee6; border-radius:8px; padding:16px; }}
    table {{ width:100%; border-collapse:collapse; }} th,td {{ border:1px solid #d8dee6; padding:8px; text-align:left; }} th {{ background:#eef4fb; }}
    .metrics {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; }}
    .metrics div {{ background:#f8fafc; border:1px solid #d8dee6; border-radius:8px; padding:12px; }}
    .metrics b {{ display:block; font-size:24px; color:#2563eb; }}
    @media (max-width:800px) {{ .metrics {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
  <header><h1>Fonbet / Tennis ML dashboard</h1><p>Read-only: no login, no credentials, no bet placement.</p></header>
  <main>
    <section>
      <h2>Status</h2>
      <p>Fonbet repo: {html.escape(str(data['fonbet_repo']))}</p>
      <p>Tennis repo: {html.escape(str(data['tennis_repo']))}</p>
    </section>
    <section>
      <h2>AI process</h2>
      <div class="metrics">
        <div><b>{data['ai_process']['summary']['active_files']}</b><span>active streams</span></div>
        <div><b>{data['ai_process']['summary']['recent_files']}</b><span>recent streams</span></div>
        <div><b>{data['ai_process']['summary']['candidate_count']}</b><span>candidates</span></div>
        <div><b>{data['ai_process']['summary']['top_score']}</b><span>top score</span></div>
      </div>
      <ul>{pipeline}</ul>
    </section>
    <section>
      <h2>Candidates</h2>
      <table><thead><tr><th>Score</th><th>Match</th><th>Market</th><th>Selection</th><th>Probability</th><th>Odds</th><th>Source</th></tr></thead><tbody>{rows or '<tr><td colspan="7">No candidates yet.</td></tr>'}</tbody></table>
    </section>
  </main>
</body>
</html>"""
    return body.encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, content_type: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/health":
            self._send(200, "application/json; charset=utf-8", b'{"status":"ok"}')
            return
        if path == "/api/status":
            self._send(200, "application/json; charset=utf-8", json.dumps(dashboard_data(), ensure_ascii=False, indent=2).encode("utf-8"))
            return
        if path == "/api/ai/process":
            self._send(200, "application/json; charset=utf-8", json.dumps(ai_process_data(), ensure_ascii=False, indent=2).encode("utf-8"))
            return
        if path == "/":
            self._send(200, "text/html; charset=utf-8", page())
            return
        self._send(404, "text/plain; charset=utf-8", b"Not found")


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Dashboard listening on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
