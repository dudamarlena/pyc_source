# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/no_sql/redis_m.py
# Compiled at: 2020-02-03 23:11:43
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: PyCharm
@file: redis_m.py
@create at: 2017-12-26 14:50

这一行开始写关于本文件的说明与解释
"""
from crwy.exceptions import CrwyImportException
from crwy.decorates import cls2singleton
try:
    import redis
except ImportError:
    raise CrwyImportException('You should install redis plugin first! try: pip install redis')

@cls2singleton
class RedisDb(object):

    def __init__(self, **kwargs):
        if 'url' in kwargs.keys():
            url = kwargs.pop('url')
            self.pool = redis.ConnectionPool.from_url(url, **kwargs)
        else:
            self.pool = redis.ConnectionPool(**kwargs)
        self.db = redis.StrictRedis(connection_pool=self.pool)


def get_redis_client(**kwargs):
    r = RedisDb(**kwargs)
    return r.db