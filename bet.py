"""Helpers for creating bet requests and parsing coupon responses."""

from __future__ import annotations

from typing import Any

CLOBAL = "GLOBAL"


def _optional(source: dict[str, Any] | None, key: str, default: Any = "None") -> Any:
    if not source:
        return default
    return source.get(key, default)


class Requets_Id:
    requestId = ""

    def __init__(self):
        from betconfig import headers, betRequestId, data_betRequestId
        import requests

        response = requests.post(betRequestId, headers=headers, data=data_betRequestId)
        jresponse = response.json()
        print(jresponse)
        self.requestId = jresponse["requestId"]


class Bets_Info:
    sums = ""
    bonusBets = ""
    ifnobet_id = ""
    ifnobet_rootId = ""
    ifnobet_kindName = ""
    ifnobet_kind = ""
    ifnobet_rootKind = ""
    ifnobet_sportId = ""
    ifnobet_competitionId = ""
    ifnobet_competitionName = ""
    ifnobet_startTime = ""
    ifnobet_team1Id = ""
    ifnobet_team2Id = ""
    ifnobet_team1 = ""
    ifnobet_team2 = ""
    ifnobet_rootTeam1Id = ""
    ifnobet_rootTeam2Id = ""
    ifnobet_rootTeam1 = ""
    ifnobet_rootTeam2 = ""
    ifnobet_name = ""
    ifnobet_rootName = ""
    ifnobet_place = ""
    ifnobet_timer = ""
    ifnobet_timerSeconds = ""
    ifnobet_timerDirection = ""
    ifnobet_score = ""
    ifnobet_betIncompatible = ""
    ifnobet_timerTimestamp = ""
    ifnobet_timerTimestampMsec = ""
    infofac_id = ""
    infofac_v = ""
    infofac_blocked = ""
    infofac_couponFactorCaption = ""
    infofac_couponChoiceCaption = ""
    infofac_couponFactorCaptionParametered = ""
    infofac_couponChoiceCaptionParametered = ""
    betis = ""

    def __init__(self, e_event, factor_f):
        import requests
        from betconfig import fsing, headers, deviceId

        data = (
            '{"sysId":1,"clientId":20211191,'
            f'"fsid":"{fsing}",'
            '"lang":"ru","bets":[{'
            f'"place":"live","factorId":{factor_f},"eventId":{e_event}'
            '}],"CDI":0,"deviceId":"'
            f"{deviceId}"
            '"}'
        )

        response = requests.post(
            "https://clientsapi04w.bk6bba-resources.com/coupon/betSlipInfo",
            headers=headers,
            data=data,
        )
        payload = response.json()

        bets = payload.get("bets", [])
        self.betis = bets
        self.bonusBets = payload.get("bonusBets", "")
        self.sums = payload.get("sums", "")

        event = bets[0].get("event", {}) if bets else {}
        factor = bets[0].get("factor", {}) if bets else {}

        self.infofac_id = _optional(factor, "id")
        self.infofac_v = _optional(factor, "v")
        self.infofac_couponFactorCaption = _optional(factor, "couponFactorCaption")
        self.infofac_couponChoiceCaption = _optional(factor, "couponChoiceCaption")
        self.infofac_couponFactorCaptionParametered = _optional(
            factor, "couponFactorCaptionParametered"
        )
        self.infofac_couponChoiceCaptionParametered = _optional(
            factor, "couponChoiceCaptionParametered"
        )

        self.ifnobet_id = _optional(event, "id")
        self.ifnobet_rootId = _optional(event, "rootId")
        self.ifnobet_kindName = _optional(event, "kindName")
        self.ifnobet_kind = _optional(event, "kind")
        self.ifnobet_rootKind = _optional(event, "rootKind")
        self.ifnobet_sportId = _optional(event, "sportId")
        self.ifnobet_competitionId = _optional(event, "competitionId")
        self.ifnobet_competitionName = _optional(event, "competitionName")
        self.ifnobet_startTime = _optional(event, "startTime")
        self.ifnobet_team1Id = _optional(event, "team1Id")
        self.ifnobet_team2Id = _optional(event, "team2Id")
        self.ifnobet_team1 = _optional(event, "team1")
        self.ifnobet_team2 = _optional(event, "team2")
        self.ifnobet_rootTeam1Id = _optional(event, "rootTeam1Id")
        self.ifnobet_rootTeam2Id = _optional(event, "rootTeam2Id")
        self.ifnobet_rootTeam1 = _optional(event, "rootTeam1")
        self.ifnobet_rootTeam2 = _optional(event, "rootTeam2")
        self.ifnobet_name = _optional(event, "name")
        self.ifnobet_rootName = _optional(event, "rootName")
        self.ifnobet_place = _optional(event, "place")
        self.ifnobet_timer = _optional(event, "timer")
        self.ifnobet_timerSeconds = _optional(event, "timerSeconds")
        self.ifnobet_timerDirection = _optional(event, "timerDirection")
        self.ifnobet_timerTimestamp = _optional(event, "timerTimestamp")
        self.ifnobet_timerTimestampMsec = _optional(event, "timerTimestampMsec")
        self.ifnobet_score = _optional(event, "score")
        self.ifnobet_betIncompatible = _optional(event, "betIncompatible")


class Stav_bet:
    coupon_resultCode = ""
    coupon_regTime = ""
    coupon_bets_event = ""
    coupon_bets = ""
    coupon_clientSaldo = ""
    coupon_amountMax = ""
    coupon_checkCode = ""
    coupon_bets_value = ""
    coupon_amountMin = ""
    coupon_bonusAccountClientSaldo = ""
    coupon_amount = ""
    coupon_bets_factor = ""
    coupon_regId = ""
    result = ""
    coupon_bets_score = ""
    coupon_bonusAccountAmount = ""

    def __init__(self, event_id, fac_id, amount):
        from betconfig import fsing, headers, deviceId
        import requests
        import traceback
        from sqlmyskr import Inser_into_one
        import time

        requestId = Requets_Id().requestId
        print(requestId)
        bet_info = Bets_Info(event_id, fac_id)

        print("-------", requestId)

        data = (
            '{"sysId":1,"clientId":20211191,'
            f'"fsid":"{fsing}","requestId":{requestId}'
            ',"coupon":{'
            f'"amount":{amount}'
            ',"flexParam":false,"flexBet":"any","bets":[{'
            f'"num":1,"event":{bet_info.ifnobet_id},"factor":{bet_info.infofac_id},"value":{bet_info.infofac_v}, '
            f'"score":"{bet_info.ifnobet_score}"'
            '}],"mirror":"https://www.fon.bet"},"lang":"ru","CDI":0,"deviceId":"'
            f"{deviceId}"
            '"}'
        )

        print(data)

        response = None
        try:
            insert_in = (
                requestId,
                amount,
                bet_info.ifnobet_id,
                bet_info.infofac_id,
                bet_info.infofac_v,
            )
            Inser_into_one(
                "betResult",
                "requestId ,amount , ifnobet_id, infofac_id , infofac_v ",
                "?,?,?,?,?",
                insert_in,
            )
            response = requests.post(
                "https://clientsapi52w.bk6bba-resources.com/coupon/bet",
                headers=headers,
                data=data,
            )
            print(response.json())
            self.result = response.json().get("result", "")
            print("ставка сделана")
        except Exception:
            print(f"Ошибка ставки:\n", traceback.format_exc())

        time.sleep(10)
        try:
            if response is None:
                raise RuntimeError("response is empty")

            coupon = response.json()["coupon"]
            self.coupon_resultCode = coupon["resultCode"]
            self.coupon_regId = coupon["regId"]
            self.coupon_checkCode = coupon["checkCode"]
            self.coupon_regTime = coupon["regTime"]
            self.coupon_clientSaldo = coupon["clientSaldo"]
            self.coupon_bonusAccountClientSaldo = coupon["bonusAccountClientSaldo"]
            self.coupon_bonusAccountAmount = coupon["bonusAccountAmount"]
            self.coupon_amountMin = coupon["amountMin"]
            self.coupon_amountMax = coupon["amountMax"]
            self.coupon_amount = coupon["amount"]
            self.coupon_bets_event = coupon["bets"][0]["event"]
            self.coupon_bets_factor = coupon["bets"][0]["factor"]
            self.coupon_bets_value = coupon["bets"][0]["value"]
            self.coupon_bets_score = coupon["bets"][0]["score"]
        except Exception:
            print("Ошибка:\n", traceback.format_exc())


class betResult:
    def __init__(self, requestId):
        from betconfig import headers, deviceId
        import requests

        data = (
            '{"sysId":1,"clientId":20211191,"fsid":"ogWFF9sq4yhzCLqKyCoDebpr",'
            f'"requestId":{requestId}'
            ',"lang":"ru","CDI":0,"deviceId":"'
            f"{deviceId}"
            '"}'
        )

        response = requests.post(
            "https://clientsapi31w.bk6bba-resources.com/coupon/betResult",
            headers=headers,
            data=data,
        )

        j_resp = response.json()
        print("betResult", j_resp)


def Proverka_bet(event_id, factor_id):
    from connt import cursor

    cursor.execute(
        """SELECT * FROM  betResult WHERE ifnobet_id=? and infofac_id=? """,
        (event_id, factor_id),
    )
    cur = cursor.fetchall()
    if len(cur) == 0:
        return 0
    return 1
