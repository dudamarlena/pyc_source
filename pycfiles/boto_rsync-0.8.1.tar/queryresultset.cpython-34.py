# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/sdb/queryresultset.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3674 bytes
from boto.compat import six

def query_lister(domain, query='', max_items=None, attr_names=None):
    more_results = True
    num_results = 0
    next_token = None
    while more_results:
        rs = domain.connection.query_with_attributes(domain, query, attr_names, next_token=next_token)
        for item in rs:
            if max_items:
                if num_results == max_items:
                    raise StopIteration
                yield item
                num_results += 1

        next_token = rs.next_token
        more_results = next_token is not None


class QueryResultSet(object):

    def __init__(self, domain=None, query='', max_items=None, attr_names=None):
        self.max_items = max_items
        self.domain = domain
        self.query = query
        self.attr_names = attr_names

    def __iter__(self):
        return query_lister(self.domain, self.query, self.max_items, self.attr_names)


def select_lister(domain, query='', max_items=None):
    more_results = True
    num_results = 0
    next_token = None
    while more_results:
        rs = domain.connection.select(domain, query, next_token=next_token)
        for item in rs:
            if max_items:
                if num_results == max_items:
                    raise StopIteration
                yield item
                num_results += 1

        next_token = rs.next_token
        more_results = next_token is not None


class SelectResultSet(object):

    def __init__(self, domain=None, query='', max_items=None, next_token=None, consistent_read=False):
        self.domain = domain
        self.query = query
        self.consistent_read = consistent_read
        self.max_items = max_items
        self.next_token = next_token

    def __iter__(self):
        more_results = True
        num_results = 0
        while more_results:
            rs = self.domain.connection.select(self.domain, self.query, next_token=self.next_token, consistent_read=self.consistent_read)
            for item in rs:
                if self.max_items and num_results >= self.max_items:
                    raise StopIteration
                yield item
                num_results += 1

            self.next_token = rs.next_token
            if self.max_items and num_results >= self.max_items:
                raise StopIteration
            more_results = self.next_token is not None

    def next(self):
        return next(self.__iter__())