# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/macros/logic/or_.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import MacroCommand

class OrMacro(MacroCommand):
    __domain__ = 'macro'
    __operation__ = 'or'

    @property
    def descriptor(self):
        return {'name': 'or', 'parameters': {'var1': {'type': 'any'}, 'var2': {'type': 'any'}}, 'help': 'Boolean OR'}

    def parse_parameters(self, **params):
        MacroCommand.parse_parameters(self, **params)
        self._var1 = params.get('var1', False)
        self._var2 = params.get('var2', False)

    def run(self):
        self.set_result(self._var1 or self._var2)