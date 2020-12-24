# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cbrand/projects/python-sqlalchemy-filterparams/build/lib/sqlalchemy_filterparams/query_config.py
# Compiled at: 2016-02-20 19:34:56
# Size of source mod 2**32: 1150 bytes
from .filters import DEFAULT_FILTERS
from .util import DEFAULT_CONVERTERS

class QueryConfig:

    def __init__(self):
        self.model = None
        self.expressions = None
        self.session = None
        self._converters = None
        self.converters = None
        self._filters = None
        self.filters = None
        self.query = None

    @property
    def converters(self):
        return self._converters

    @converters.setter
    def converters(self, value):
        if value is None:
            value = DEFAULT_CONVERTERS.copy()
        self._converters = value

    @property
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, value):
        if value is None:
            value = DEFAULT_FILTERS
        self._filters = dict((filter_obj.name, filter_obj) for filter_obj in value)

    def filter_for(self, filter_name):
        if filter_name not in self._filters:
            raise KeyError('Filter %s not found' % filter_name)
        filter_cl = self._filters[filter_name]
        return filter_cl(self.converters)