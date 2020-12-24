# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/get_schedule.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime
from sqlalchemy import *
from coils.core import *

class GetProcessSchdule(AsyncronousCommand):
    __domain__ = 'workflow'
    __operation__ = 'get-schedule'

    def parse_success_response(self, data):
        self.set_return_value(data['schedule'])

    def parse_failure_response(self, data):
        self.set_return_value(None)
        return

    def parse_parameters(self, **params):
        AsyncronousCommand.parse_parameters(self, **params)
        self._route_id = 0
        if 'route' in params:
            self._route_id = params.get('route').object_id
        elif 'route_id' in params:
            self._route_id = int(params.get('route_id'))

    def run(self):
        self.set_return_value(None)
        if self._ctx.amq_available:
            self.callout('coils.workflow.scheduler/list_jobs', {'contextId': self._ctx.account_id, 'routeId': self._route_id})
            self.wait()
        return