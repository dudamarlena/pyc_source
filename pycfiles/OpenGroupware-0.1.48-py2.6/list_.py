# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/list_.py
# Compiled at: 2012-10-12 07:02:39
import time
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class ListRoutes(GetCommand):
    __domain__ = 'route'
    __operation__ = 'list'

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)
        self._props = params.get('properties', [Route.object_id,
         Route.version,
         Route.owner_id,
         Route.name])
        self._contexts = params.get('contexts', None)
        self._mask = params.get('mask', 'r')
        self._limit = params.get('limit', None)
        return

    def run(self):
        self.set_multiple_result_mode()
        self.access_check = False
        manager = BundleManager.get_access_manager('Route', self._ctx)
        self.set_return_value(manager.List(self._ctx, self._props, contexts=self._contexts, mask=self._mask, limit=self._limit))


class ListProcesses(GetCommand):
    __domain__ = 'process'
    __operation__ = 'list'

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)
        self._props = params.get('properties', [Process.object_id,
         Process.version,
         Process.owner_id,
         Process.state,
         Process.route_id])
        self._contexts = params.get('contexts', None)
        self._mask = params.get('mask', 'r')
        self._group = params.get('route_group', None)
        self._limit = params.get('limit', None)
        return

    def run(self):
        self.set_multiple_result_mode()
        self.access_check = False
        manager = BundleManager.get_access_manager('Process', self._ctx)
        self.set_return_value(manager.List(self._ctx, self._props, contexts=self._contexts, mask=self._mask, route_group=self._group, limit=self._limit))