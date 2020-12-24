# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jlopes/PycharmProjects/mcg/core/db/MongoDB.py
# Compiled at: 2017-01-24 01:10:58
# Size of source mod 2**32: 732 bytes
from core.db.Singleton import Singleton
from pymongo import MongoClient
import urllib
from urllib.parse import quote

class MongoDB(metaclass=Singleton):

    def __init__(self, mongo_uri=None):
        self._MongoDB__mongo_uri = mongo_uri

    def get_database(self):
        mongo_client = MongoClient('mongodb://' + self._MongoDB__mongo_uri['user'] + ':' + urllib.parse.quote(self._MongoDB__mongo_uri['password']) + '@' + self._MongoDB__mongo_uri['host'] + ':' + self._MongoDB__mongo_uri['port'] + '/' + self._MongoDB__mongo_uri['db'])
        return mongo_client[self._MongoDB__mongo_uri['db']]

    def __set__(self, instance, value):
        self._MongoDB__mongo_uri(instance, value)