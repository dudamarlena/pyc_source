# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/get_process_list.py
# Compiled at: 2012-10-12 07:02:39
from time import time
from coils.core import *

class GetProcessList(AsyncronousCommand):
    __domain__ = 'workflow'
    __operation__ = 'get-process-list'

    def parse_success_response(self, data):
        self.set_return_value(data['processList'])

    def parse_failure_response(self, data):
        self.set_return_value(None)
        return

    def parse_parameters(self, **params):
        AsyncronousCommand.parse_parameters(self, **params)

    def run(self):
        self.set_return_value(None)
        if self._ctx.amq_available:
            self.callout('coils.workflow.manager/ps', {'contextId': self._ctx.account_id})
            self.wait()
        return