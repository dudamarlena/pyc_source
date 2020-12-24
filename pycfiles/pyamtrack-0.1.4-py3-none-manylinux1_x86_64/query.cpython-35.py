# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_catalog/query.py
# Compiled at: 2020-02-21 06:54:32
# Size of source mod 2**32: 2364 bytes
__doc__ = 'PyAMS_catalog.query module\n'
from hypatia.query import Query
from zope.intid.interfaces import IIntIds
from pyams_utils.registry import query_utility
__docformat__ = 'restructuredtext'

class CatalogResultSet:
    """CatalogResultSet"""

    def __init__(self, query):
        self.query = query
        self.intids = query_utility(IIntIds)
        self.first = []
        self.last = []

    def __iter__(self):
        for item in self.first:
            yield item

        intids = self.intids
        if intids is not None:
            query = self.query
            if isinstance(query, Query):
                query = query.execute()
            if isinstance(query, tuple):
                query = query[1]
            for oid in query:
                if isinstance(oid, int):
                    target = intids.queryObject(oid)
                    if target is not None:
                        yield target
                    else:
                        yield oid

        for item in self.last:
            yield item

    def __len__(self):
        return len(self.first) + len(self.query) + len(self.last)

    def prepend(self, items):
        """Insert a list of elements at the beginning of the results set"""
        insert = self.first.insert
        for index, item in enumerate(items):
            insert(index, item)

    def append(self, items):
        """Append a list of elements at the end of the results set"""
        append = self.last.append
        for item in items:
            append(item)


def or_(source, added):
    """Combine two queries with 'or'"""
    if source is None:
        source = added
    else:
        source |= added
    return source


def and_(source, added):
    """Combine two queries with 'and'"""
    if source is None:
        source = added
    else:
        source &= added
    return source