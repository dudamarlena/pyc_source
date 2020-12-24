# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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