# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/macros/logic/not_.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import MacroCommand

class NotMacro(MacroCommand):
    __domain__ = 'macro'
    __operation__ = 'not'

    @property
    def descriptor(self):
        return {'name': 'not', 'parameters': {'var': {'type': 'any'}}, 'help': 'Boolean Not'}

    def parse_parameters(self, **params):
        MacroCommand.parse_parameters(self, **params)
        self._var = params.get('var', False)

    def run(self):
        self.set_result(not self._var)