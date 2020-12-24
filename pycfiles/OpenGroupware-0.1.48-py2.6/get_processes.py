# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/get_processes.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand
from utility import filename_for_process_markup

class GetProcesses(GetCommand):
    __domain__ = 'route'
    __operation__ = 'get-processes'
    mode = None

    def __init__(self):
        GetCommand.__init__(self)

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)
        if self.query_by is None:
            if 'name' in params:
                self.query_by = 'name'
                self.name = params['name']
            elif 'object' in params:
                self.query_by = 'object_id'
                self.object_ids.append(params['object'].object_id)
            elif 'objects' in params:
                self.query_by = 'object_id'
                for route in params['objects']:
                    self.object_ids.append(route.object_id)

        self._archived = params.get('archived', False)
        state = params.get('state', None)
        if state is None:
            self._state = [
             'I', 'F', 'C', 'P', 'Q', 'R']
        elif isinstance(state, list):
            self._state = [ str(x).upper().strip() for x in state ]
        elif isinstance(state, basestring):
            self._state = state.upper().strip()
        else:
            raise CoilsException('Unable to parse "state" parameter.')
        return

    def set_markup(self, processes):
        for process in processes:
            handle = BLOBManager.Open(filename_for_process_markup(process), 'rb', encoding='binary')
            if handle is not None:
                bpml = handle.read()
                process.set_markup(bpml)
                BLOBManager.Close(handle)
            else:
                self.log.error(('Found no process markup for processId#{0}').format(process.object_id))

        return processes

    def run(self):
        self.mode = 2
        route_ids = []
        if self.query_by == 'object_id':
            for route in self._ctx.run_command('route::get', ids=self.object_ids, access_check=self.access_check):
                route_ids.append(route.object_id)

        else:
            if self.query_by == 'name':
                route = self._ctx.run_command('route::get', name=self.name, access_check=self.access_check)
                if route is not None:
                    route_ids.append(route.object_id)
            if len(route_ids) > 0:
                self.log.debug(('retrieving processses for routes {0}').format(route_ids))
                db = self._ctx.db_session()
                if self._archived:
                    query = db.query(Process).filter(and_(Process.route_id.in_(route_ids), Process.state.in_(self._state), Process.status == 'archived')).limit(self.limit)
                else:
                    query = db.query(Process).filter(and_(Process.route_id.in_(route_ids), Process.state.in_(self._state), Process.status != 'archived')).limit(self.limit)
                self.set_return_value(self.set_markup(query.all()))
            else:
                self.set_return_value([])
            return