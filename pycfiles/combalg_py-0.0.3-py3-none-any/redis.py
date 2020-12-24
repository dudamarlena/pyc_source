# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/breezekay/Dropbox/Codes/ez/py.ez.co/comb.ez.co/comb/mq/redis.py
# Compiled at: 2014-09-13 05:05:11


def push(redis, key, value):
    return redis.rpush(key, value)


def pop(redis, key):
    return redis.lpop(key)