# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/macros/math/sumof.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import MacroCommand

class SumOfMacro(MacroCommand):
    __domain__ = 'macro'
    __operation__ = 'sumof'

    @property
    def descriptor(self):
        return {'name': 'sumof', 'parameters': {'var1': {'type': 'numeric'}, 'var2': {'type': 'numeric'}}, 'help': ''}

    def parse_parameters(self, **params):
        MacroCommand.parse_parameters(self, **params)
        self._var1 = params.get('var1', None)
        self._var2 = params.get('var2', None)
        if self._var1 is None or self._var2 is None:
            raise CoilsException('NULL input provided to sumof macro')
        if not isinstance(self._var1, (int, float)) or not isinstance(self._var2, (int, float)):
            raise CoilsException('Non-numeric input provided to sumof macro')
        return

    def run(self):
        self.set_result(self._var1 + self._var2)