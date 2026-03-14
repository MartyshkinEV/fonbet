"""MongoDB helper functions used by project scripts."""

from __future__ import annotations

from pymongo import MongoClient


def conn_mongo(name_bd):
    """Подключение к базе данных."""
    client = MongoClient("localhost", 37017)
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
