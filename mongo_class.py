"""MongoDB helper functions used by project scripts."""

from __future__ import annotations

import os

from pymongo import MongoClient


MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", "37017"))


def conn_mongo(name_bd):
    """Подключение к базе данных."""
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    return client[name_bd]


def collecsion_conn(name_bd, name_collect):
    """Backward-compatible collection connector (kept misspelled name)."""
    db = conn_mongo(name_bd)
    return db[name_collect]


def apend_list(name_bd, name_collect, listik):
    """Передать список для добавления через цикл for."""
    collect = collecsion_conn(name_bd, name_collect)
    for item in listik:
        collect.insert_one(item)
        print(f"успешно добавлено в базу и таблицу {name_collect}")


def updateOne(name_db, name_coll, id_key, update_1):
    collect = collecsion_conn(name_db, name_coll)
    collect.update_one(id_key, {"$set": update_1}, upsert=False)


def delete_drop(name_db, name_cl):
    coll = collecsion_conn(name_db, name_cl)
    coll.drop()
