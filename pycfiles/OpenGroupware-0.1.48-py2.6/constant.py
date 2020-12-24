# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/macros/general/constant.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import MacroCommand

class ConstantMacro(MacroCommand):
    __domain__ = 'macro'
    __operation__ = 'constant'

    @property
    def descriptor(self):
        return {'name': 'contstant', 'parameters': {'value': {'type': 'any'}}, 'help': 'Produce a constant value'}

    def parse_parameters(self, **params):
        MacroCommand.parse_parameters(self, **params)
        self._value = params.get('value', None)
        return

    def run(self):
        self.set_result(self._value)