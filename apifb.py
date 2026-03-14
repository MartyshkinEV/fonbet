"""Parsing and selection helpers for Fonbet API payload stored in json.txt."""

from __future__ import annotations

from typing import Any


def _optional(item: dict[str, Any], key: str, default: Any = "None") -> Any:
    return item.get(key, default)


class Sports:
    sports_ids: list[Any]
    sports_parentId: list[Any]
    sports_kinds: list[Any]
    sports_sortOrder: list[Any]
    sports_name: list[Any]
    sports_parentIds: list[Any]
    sports_name_tip: list[Any]

    def __init__(self):
        from classy import Jsn_txt

        sports_data = Jsn_txt(categ="sports").cate

        self.sports_ids = []
        self.sports_parentId = []
        self.sports_kinds = []
        self.sports_sortOrder = []
        self.sports_name = []
        self.sports_parentIds = []
        self.sports_name_tip = []

        for sport in sports_data:
            self.sports_ids.append(sport["id"])
            self.sports_parentId.append(_optional(sport, "parentId"))
            self.sports_kinds.append(_optional(sport, "kind"))
            self.sports_sortOrder.append(_optional(sport, "sortOrder"))
            self.sports_name.append(_optional(sport, "name"))
            self.sports_parentIds.append(_optional(sport, "parentIds"))
            self.sports_name_tip.append(str(_optional(sport, "name", "None")).split(".")[0])


class Event:
    event_name: list[Any]
    event_team1: list[Any]
    event_team1Id: list[Any]
    event_statisticsType: list[Any]
    event_team2: list[Any]
    event_specialTableId: list[Any]
    event_team2Id: list[Any]
    event_startTime: list[Any]
    event_kind: list[Any]
    event_state: list[Any]
    event_parentId: list[Any]
    event_priority: list[Any]
    event_sportId: list[Any]
    event_id: list[Any]
    event_tv: list[Any]
    event_info: list[Any]
    event_notMatch: list[Any]
    event_place: list[Any]
    event_level: list[Any]
    event_rootKind: list[Any]
    event_sortOrder: list[Any]
    event_num: list[Any]

    def __init__(self):
        from classy import Jsn_txt

        events_data = Jsn_txt(categ="events").cate

        self.event_id = []
        self.event_name = []
        self.event_num = []
        self.event_notMatch = []
        self.event_parentId = []
        self.event_team1 = []
        self.event_statisticsType = []
        self.event_kind = []
        self.event_rootKind = []
        self.event_place = []
        self.event_priority = []
        self.event_specialTableId = []
        self.event_sportId = []
        self.event_team2 = []
        self.event_team1Id = []
        self.event_startTime = []
        self.event_level = []
        self.event_tv = []
        self.event_team2Id = []
        self.event_sortOrder = []
        self.event_info = []
        self.event_state = []

        for event in events_data:
            self.event_sportId.append(_optional(event, "sportId"))
            self.event_id.append(_optional(event, "id"))
            self.event_state.append(_optional(event, "state"))
            self.event_parentId.append(_optional(event, "parentId"))
            self.event_tv.append(_optional(event, "tv"))
            self.event_team1Id.append(_optional(event, "team1Id"))
            self.event_sortOrder.append(_optional(event, "sortOrder"))
            self.event_info.append(_optional(event, "info"))
            self.event_notMatch.append(_optional(event, "notMatch"))
            self.event_statisticsType.append(_optional(event, "statisticsType"))
            self.event_priority.append(_optional(event, "priority"))
            self.event_team2.append(_optional(event, "team2"))
            self.event_startTime.append(_optional(event, "startTime"))
            self.event_num.append(_optional(event, "num"))
            self.event_level.append(_optional(event, "level"))
            self.event_kind.append(_optional(event, "kind"))
            self.event_rootKind.append(_optional(event, "rootKind"))
            self.event_team1.append(_optional(event, "team1"))
            self.event_specialTableId.append(_optional(event, "specialTableId"))
            self.event_team2Id.append(_optional(event, "team2Id"))
            self.event_name.append(_optional(event, "name"))
            self.event_place.append(_optional(event, "place"))


class Sel_play:
    index_tip: set[int]
    str_ids: list[Any]
    event_idos: list[Any]

    def sport_name(self, spr_name: str):
        spr = Sports()

        indices: list[int] = []
        sport_ids: list[Any] = []

        for i, sport_name in enumerate(spr.sports_name_tip):
            if sport_name == spr_name:
                indices.append(i)
                sport_ids.append(spr.sports_ids[i])

        self.index_tip = set(indices)
        self.str_ids = sport_ids

    def __init__(self, spr_name):
        from classy import Tims

        t_nw = Tims().ts_nw
        self.sport_name(spr_name)

        events = Event()
        id_ev: list[Any] = []
        for i, start_time in enumerate(events.event_startTime):
            if start_time < t_nw:
                id_ev.append(events.event_sportId[i])

        self.event_idos = id_ev


class CustomFac:
    custom_e: list[Any]
    custom_all: list[Any]

    def __init__(self):
        from classy import Jsn_txt

        custom_factors = Jsn_txt(categ="customFactors").cate
        self.custom_e = []
        self.custom_all = []

        for custom in custom_factors:
            self.custom_e.append(custom["e"])
            self.custom_all.append(custom)


class Sob_live:
    live_sb: list[Any]
    custom_all: list[Any]
    index_event: list[int]
    sport_id: list[Any]

    def __init__(self):
        events = Event()
        custom_factors = CustomFac()

        self.live_sb = []
        self.custom_all = []
        self.index_event = []
        self.sport_id = []

        for i, place in enumerate(events.event_place):
            if place == "live":
                self.live_sb.append(events.event_id[i])
                self.index_event.append(i)
                self.sport_id.append(events.event_sportId[i])

        for event_id in self.live_sb:
            try:
                idx = custom_factors.custom_e.index(event_id)
                self.custom_all.append(custom_factors.custom_all[idx])
            except ValueError:
                continue


class Name_sl:
    sport_id: list[Any]

    def __init__(self, name_sob):
        sl = Sob_live()
        sp = Sports()
        self.sport_id = []

        for i, sport_name in enumerate(sp.sports_name):
            if str(sport_name).split(".")[0] == name_sob:
                self.sport_id.append(sp.sports_ids[i])

        for sport in self.sport_id:
            try:
                print(sl.sport_id.index(sport))
            except ValueError:
                print("ошибка")
