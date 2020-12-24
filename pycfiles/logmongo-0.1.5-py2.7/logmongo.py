# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/logmongo.py
# Compiled at: 2016-12-08 20:58:27
import pymongo
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import CollectionInvalid
from socket import getfqdn
from time import time
from prettyprint import pp
from time import sleep

class Logmongo(Collection):

    def __init__(self, name, db='logs', size=524288000, capped=True, host='localhost', port=27017):
        database = MongoClient(host=host, port=port)[db]
        try:
            database.create_collection(name, capped=capped, size=size)
        except CollectionInvalid:
            pass

        super(Logmongo, self).__init__(database, name)

    def write(self, record=None, **kwargs):
        """Log all kwargs with timestamp to collection"""
        record = self._unite(record, kwargs)
        if 'when' not in record:
            record['when'] = int(time() * 1000)
        if 'source' not in record:
            record['source'] = getfqdn()
        self.save(record, w=0)

    def query(self, record=None, **kwargs):
        """just like find, but accepts kwargs for query"""
        record = self._unite(record, kwargs)
        return self.find(record)

    def _unite(self, record, kwargs):
        if record:
            return dict(record.items() + kwargs.items())
        else:
            return kwargs

    def tail(self, query=None, n=10):
        """print all entries that match query until killed"""
        nskip = self.count() - n
        if nskip < 0:
            nskip = 0
        if query == None:
            query = {}
        cursor = self.find(query, cursor_type=pymongo.CursorType.TAILABLE_AWAIT, skip=nskip)
        while cursor.alive:
            try:
                entry = cursor.next()
                pp(entry)
            except StopIteration:
                sleep(1)

        return

    def update(self):
        """logs should not be updated"""
        pass

    def remove(self):
        """logs should not be removed, maybe set archive bit?"""
        pass