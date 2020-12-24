# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/sources/source.py
# Compiled at: 2015-10-11 07:17:06
import logging
logger = logging.getLogger(__name__)

class Source(object):
    sources = []

    def __init__(self):
        self._connections = []

    def list(self):
        return self._connections

    @staticmethod
    def connections():
        cons = []
        for source in Source.sources:
            cons += source.list()

        return set(cons)

    @staticmethod
    def connection(options):
        for connection in Source.connections():
            opts = options.get(connection.dbms)
            if connection.matches(opts):
                return connection

        return