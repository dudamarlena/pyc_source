# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/sdb/db/query.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3072 bytes
from boto.compat import six

class Query(object):
    __local_iter__ = None

    def __init__(self, model_class, limit=None, next_token=None, manager=None):
        self.model_class = model_class
        self.limit = limit
        self.offset = 0
        if manager:
            self.manager = manager
        else:
            self.manager = self.model_class._manager
        self.filters = []
        self.select = None
        self.sort_by = None
        self.rs = None
        self.next_token = next_token

    def __iter__(self):
        return iter(self.manager.query(self))

    def next(self):
        if self.__local_iter__ is None:
            self.__local_iter__ = self.__iter__()
        return next(self.__local_iter__)

    def filter(self, property_operator, value):
        self.filters.append((property_operator, value))
        return self

    def fetch(self, limit, offset=0):
        """Not currently fully supported, but we can use this
        to allow them to set a limit in a chainable method"""
        self.limit = limit
        self.offset = offset
        return self

    def count(self, quick=True):
        return self.manager.count(self.model_class, self.filters, quick, self.sort_by, self.select)

    def get_query(self):
        return self.manager._build_filter_part(self.model_class, self.filters, self.sort_by, self.select)

    def order(self, key):
        self.sort_by = key
        return self

    def to_xml(self, doc=None):
        if not doc:
            xmlmanager = self.model_class.get_xmlmanager()
            doc = xmlmanager.new_doc()
        for obj in self:
            obj.to_xml(doc)

        return doc

    def get_next_token(self):
        if self.rs:
            return self.rs.next_token
        if self._next_token:
            return self._next_token

    def set_next_token(self, token):
        self._next_token = token

    next_token = property(get_next_token, set_next_token)