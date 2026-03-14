"""Utilities for loading Fonbet JSON payloads and time helpers."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

JSON_PATH = Path("json.txt")


class Requet:
    """Fetch payload from configured URL and save it to json.txt.

    NOTE: Class name is kept for backward compatibility.
    """

    cate: list[Any] = []

    def __init__(self) -> None:
        from configur import url_1
        import requests

        if JSON_PATH.exists():
            JSON_PATH.unlink()

        response = requests.get(url_1)
        response.raise_for_status()
        payload = response.json()

        with JSON_PATH.open("w", encoding="utf-8") as outfile:
            json.dump(payload, outfile)

        print("Requet успешно завершил работу!")


class Jsn_txt:
    """Read a category from json.txt.

    NOTE: Class name is kept for backward compatibility.
    """

    cate: Any = ""

    def __init__(self, categ: str):
        with JSON_PATH.open("r", encoding="utf-8") as file:
            text = json.load(file)

        self.cate = text[categ]
        print(" параметр cate готов")


class Tims:
    """Current unix timestamp rounded to integer.

    NOTE: Class name is kept for backward compatibility.
    """

    ts_nw: int | str = ""

    def __init__(self) -> None:
        print("определяется время")
        self.ts_nw = round(time.time())
