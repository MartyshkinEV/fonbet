import pymongo


def conn_mongo(name_bd):
    'подключение к базе данных'
    from pymongo import MongoClient

    client = MongoClient()
    client = MongoClient('localhost', 37017)
    db = client[name_bd]
    return (db)


def collecsion_conn(name_bd,name_collect):
    from myvk.mongo_class import conn_mongo

    'импортируем данные функции conn_mongo подключкение к базе данных'
    db=conn_mongo(name_bd)
    collection = db[name_collect]
    return (collection)

def apend_list(name_bd,name_collect,listik):
    'передать список для добавления через цикл фор добавит'
    from myvk.mongo_class import collecsion_conn
    import pymongo

    collect=collecsion_conn(name_bd,name_collect)
    for x in listik:
        collect.insert_one(x)
        print(f'успешно добавлено в базу и таблицу {name_collect}')


def updateOne(name_db,name_coll,id_key,update_1):
    from myvk.mongo_class import collecsion_conn

    collect=collecsion_conn(name_db,name_coll)
    collect.update_one(id_key, {'$set': update_1}, upsert=False)



def delete_drop(name_db, name_cl):
    from myvk.mongo_class import collecsion_conn
    coll = collecsion_conn(name_db,name_cl)
    coll.drop()

