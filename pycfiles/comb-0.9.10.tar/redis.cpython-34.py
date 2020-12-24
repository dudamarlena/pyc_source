# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breezekay/Dropbox/Codes/nextoa/comb/comb/mq/redis.py
# Compiled at: 2014-09-13 05:05:11
# Size of source mod 2**32: 170 bytes


def push(redis, key, value):
    return redis.rpush(key, value)


def pop(redis, key):
    return redis.lpop(key)