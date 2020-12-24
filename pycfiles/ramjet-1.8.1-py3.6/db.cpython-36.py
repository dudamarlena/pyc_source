# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ramjet/utils/db.py
# Compiled at: 2017-11-06 22:08:04
# Size of source mod 2**32: 140 bytes
import pymongo
from ramjet.settings import MONGO_HOST, MONGO_PORT

def get_conn():
    return pymongo.MongoClient(MONGO_HOST, MONGO_PORT)