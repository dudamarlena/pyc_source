# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/kill_process.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *

class KillProcess(Command):
    __domain__ = 'process'
    __operation__ = 'kill'

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self._obj = params.get('process', params.get('object', None))
        self._signal = int(params.get('signal', 15))
        self._callback = params.get('callback', None)
        return

    def run(self):
        if self._obj.state == 'R':
            self._result = self._ctx.send(None, ('coils.workflow.executor/kill:{0}').format(self._obj.object_id), {'signal': self._signal}, callback=self._callback)
        elif self._obj.state in ('I', 'Q'):
            self._obj.state = 'H'
            self._result = None
        raise CoilsException('Process is not in a killable state')
        return