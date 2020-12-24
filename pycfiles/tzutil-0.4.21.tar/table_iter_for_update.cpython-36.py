# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n8f5s77x/tzutil/tzutil/db/pg/table_iter_for_update.py
# Compiled at: 2018-12-04 01:36:04
# Size of source mod 2**32: 971 bytes
from time import time
from tqdm import tqdm
from random import shuffle, randint
DAY_SECONDS = 86400

def table_iter_for_update(pg, redis, R, table_iter, where={}, expire_day=1, next_time=None):
    key = R.TABLE.ITER.UPDATE.ZSET % table_iter._key
    if int(table_iter._id) == 0:
        redis.delete(key)
    for i in table_iter(where):
        redis.zadd(key, 0, i.id)

    now = int(time())
    li = redis.zrangebyscore(key, 0, now)
    if next_time is None:
        expire_sec = expire_day * DAY_SECONDS

        def next_time(o):
            if expire_day > 1:
                if not redis.zscore(key, id):
                    s = randint(1, expire_day) * DAY_SECONDS
            else:
                s = expire_sec
            return now + s

    for id in tqdm(li, unit='row'):
        o = pg.select_one(table_iter._id._table, dict(id=id))
        yield o
        redis.zadd(key, next_time(o), id)