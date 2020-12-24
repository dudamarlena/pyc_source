# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/park_process.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *

class ParkProcess(Command):
    __domain__ = 'process'
    __operation__ = 'park'

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self._obj = params.get('process', params.get('object', None))
        self._context_id = params.get('runas', self._ctx.account_id)
        self._callback = params.get('callback', None)
        return

    def run(self):
        self._result = self._ctx.send(None, 'coils.workflow.executor/park', {'processId': self._obj.object_id, 'contextId': self._context_id}, callback=self._callback)
        return