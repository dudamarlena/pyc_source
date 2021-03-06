# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/foorti/foorti_systems.py
# Compiled at: 2017-02-13 23:00:12
import redis
SYSTEMS = {'default': redis.Redis(host='localhost', port=6379)}

def setup_redis_system(name, host, port, **kw):
    SYSTEMS[name] = redis.Redis(host=host, port=port, **kw)


def get_redis(system='default'):
    return SYSTEMS[system]


class redis_obj:

    def __init__(self, name, system):
        self.name = name
        self.conn = get_redis(system)

    def clear(self):
        self.conn.delete(self.name)