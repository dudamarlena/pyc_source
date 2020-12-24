# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/unschedule_process.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime
from sqlalchemy import *
from coils.core import *

class UnscheduleProcess(AsyncronousCommand):
    __domain__ = 'process'
    __operation__ = 'unschedule'

    def parse_sucess_response(self, data):
        self.set_return_value(True)

    def parse_failure_response(self, data):
        self.set_return_value(False)

    def parse_parameters(self, **params):
        AsyncronousCommand.parse_parameters(self, **params)
        self._uuid = params.get('uuid', None)
        if self._uuid is None:
            raise CoilsException('Request to cancel scheduled process with no scheduled process id')
        return

    def run(self):
        self.set_return_value(False)
        self.set_return_value(self.callout('coils.workflow.scheduler/unschedule_job', {'UUID': self._uuid, 'contextId': self._ctx.account_id}))
        self.wait()