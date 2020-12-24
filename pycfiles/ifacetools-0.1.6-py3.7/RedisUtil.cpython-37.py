# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\redisutil\RedisUtil.py
# Compiled at: 2019-08-07 21:06:47
# Size of source mod 2**32: 698 bytes
import redis, ast

class RedisUtil:

    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self._RedisUtil__initredis()

    def __initredis(self):
        self.redis = redis.Redis(self.host, self.port, self.db)

    def getdata(self, key):
        return self.redis.get(key)