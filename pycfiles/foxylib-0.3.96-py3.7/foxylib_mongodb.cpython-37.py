# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/database/mongodb/foxylib_mongodb.py
# Compiled at: 2020-01-15 23:57:40
# Size of source mod 2**32: 553 bytes
import os
from functools import lru_cache
from pymongo import MongoClient
from foxylib.tools.function.function_tool import FunctionTool

class FoxylibMongodb:
    DBNAME = 'foxylib'

    @classmethod
    def uri(cls):
        return os.environ.get('MONGO_URI')

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def client(cls):
        return MongoClient(host=(cls.uri()))

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def db(cls):
        client = cls.client()
        return client[cls.DBNAME]