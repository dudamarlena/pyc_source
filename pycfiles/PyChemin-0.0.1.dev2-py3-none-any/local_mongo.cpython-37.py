# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gufranco/PyChemia/tests/local_mongo.py
# Compiled at: 2019-05-14 13:43:02
# Size of source mod 2**32: 432 bytes
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

def has_local_mongo():
    try:
        max_server_selection_delay = 1
        client = MongoClient('localhost', serverSelectionTimeoutMS=max_server_selection_delay)
        client.server_info()
        return True
    except ServerSelectionTimeoutError as err:
        try:
            print(err)
            return False
        finally:
            err = None
            del err