# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/get_input_message.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class GetInputMessage(Command):
    __domain__ = 'process'
    __operation__ = 'get-input-message'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.process = params.get('process', None)
        return

    def run(self, **params):
        if self.process is not None:
            self._result = self._ctx.run_command('message::get', uuid=self.process.input_message)
        else:
            self._result = None
        return