# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/no_sql/redis_m.py
# Compiled at: 2020-02-03 23:11:43
__doc__ = '\n@author: wuyue\n@contact: wuyue92tree@163.com\n@software: PyCharm\n@file: redis_m.py\n@create at: 2017-12-26 14:50\n\n这一行开始写关于本文件的说明与解释\n'
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