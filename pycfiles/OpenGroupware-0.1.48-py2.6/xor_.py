# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/macros/logic/xor_.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import MacroCommand

class XORMacro(MacroCommand):
    __domain__ = 'macro'
    __operation__ = 'xor'

    @property
    def descriptor(self):
        return {'name': 'xor', 'parameters': {'var1': {'type': 'any'}, 'var2': {'type': 'any'}}, 'help': 'Boolean XOR'}

    def parse_parameters(self, **params):
        MacroCommand.parse_parameters(self, **params)
        self._var1 = params.get('var1', False)
        self._var2 = params.get('var2', False)

    def run(self):
        if self._var1 != self._var2:
            self.set_result(True)
        else:
            self.set_result(False)