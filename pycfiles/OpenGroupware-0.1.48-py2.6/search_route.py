# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/search_route.py
# Compiled at: 2012-10-12 07:02:39
from coils.foundation import Route
from coils.core import *
from coils.core.logic import SearchCommand
from keymap import COILS_ROUTE_KEYMAP

class SearchRoutes(SearchCommand):
    __domain__ = 'route'
    __operation__ = 'search'
    mode = None

    def __init__(self):
        SearchCommand.__init__(self)

    def prepare(self, ctx, **params):
        SearchCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        SearchCommand.parse_parameters(self, **params)

    def run(self):
        self._query = self._parse_criteria(self._criteria, Route, COILS_ROUTE_KEYMAP)
        data = self._query.all()
        self.log.debug('query returned %d objects' % len(data))
        self.set_return_value(data)