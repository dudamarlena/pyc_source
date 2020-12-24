# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tailow/connection.py
# Compiled at: 2018-06-14 12:05:35
# Size of source mod 2**32: 849 bytes
import sys, asyncio
from motor.motor_asyncio import AsyncIOMotorClient

class ConnectionException(Exception):
    pass


class Connection(object):
    __doc__ = '\n      Default persistable connection object\n    '
    _default_client = None
    _default_database = None

    @classmethod
    def connect(cls, uri, db_name, loop=None):
        if not loop:
            loop = asyncio.get_event_loop()
        cls._default_client = AsyncIOMotorClient(uri, io_loop=loop)
        cls._default_database = cls._default_client[db_name]

    @classmethod
    def disconnect(cls):
        cls._default_client = None
        cls._default_database = None

    @classmethod
    def get_collection(cls, coll):
        if not cls._default_database:
            raise ConnectionException('Not conneted to database')
        return cls._default_database[coll]