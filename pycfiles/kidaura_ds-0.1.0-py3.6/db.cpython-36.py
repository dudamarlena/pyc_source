# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kds/db.py
# Compiled at: 2020-02-20 02:51:30
# Size of source mod 2**32: 330 bytes
import pymongo, os

def get_conn(database='kidaura_v1'):
    client = pymongo.MongoClient(os.environ['MONGO_URI'])
    return client.get_database(database)


def get_collection(coll, database='kidaura_v1'):
    client = pymongo.MongoClient(os.environ['MONGO_URI'])
    db = client.get_database(database)
    return db[coll]