# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/get_route.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand
from utility import filename_for_route_markup

class GetRoute(GetCommand):
    __domain__ = 'route'
    __operation__ = 'get'

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)
        if self.query_by is None:
            if 'name' in params:
                self.mode = 1
                self.query_by = 'name'
                self.name = params['name'].lower()
        return

    def add_route_markup(self, routes):
        for route in routes:
            handle = BLOBManager.Open(filename_for_route_markup(route), 'rb', encoding='binary')
            if handle is not None:
                bpml = handle.read()
                route.set_markup(bpml)
                BLOBManager.Close(handle)
            else:
                route.set_markup('')

        return routes

    def run(self, **params):
        db = self._ctx.db_session()
        if self.query_by == 'object_id':
            if len(self.object_ids) > 0:
                query = db.query(Route).filter(and_(Route.object_id.in_(self.object_ids), Route.status != 'archived'))
        elif self.query_by == 'name':
            query = db.query(Route).filter(and_(func.lower(Route.name).like(self.name), Route.status != 'archived'))
        else:
            self.mode = 2
            query = db.query(Route)
        self.set_return_value(self.add_route_markup(query.all()))