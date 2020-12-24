# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breezekay/Dropbox/Codes/ez/py.ez.co/comb.ez.co/comb/mq/redis.py
# Compiled at: 2014-09-13 05:05:11


def push(redis, key, value):
    return redis.rpush(key, value)


def pop(redis, key):
    return redis.lpop(key)