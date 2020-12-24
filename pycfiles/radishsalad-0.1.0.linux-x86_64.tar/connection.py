# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kriskin/w/python/ve/lib/python2.6/site-packages/radishsalad/connection.py
# Compiled at: 2011-08-14 13:03:49
import redis

class ConnectionSettings(object):
    connector = None

    @classmethod
    def set_connector(cls, connector):
        cls.connector = connector

    @classmethod
    def default_connector(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = redis.Redis()
        return cls.instance

    @classmethod
    def get_connector(cls):
        return cls.connector or cls.default_connector


def get_redis():
    return ConnectionSettings.get_connector()()