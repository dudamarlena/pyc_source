# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/get_process_properties.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *

class GetProcessProperties(Command):
    __domain__ = 'process'
    __operation__ = 'get-properties'

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self._obj = params.get('process', params.get('object', None))
        if self._obj is None:
            self._pid = params.get('pid', params.get('id', None))
        else:
            self._pid = self._obj.object_id
        self._context_id = params.get('runas', self._ctx.account_id)
        self._callback = params.get('callback', None)
        if self._pid is None:
            raise CoilsException('ProcessId required to retreive process OIE proprties')
        return

    def run(self):
        self._result = self._ctx.send(None, ('coils.workflow.manager/get_properties:{0}').format(self._pid), None, callback=self._callback)
        return