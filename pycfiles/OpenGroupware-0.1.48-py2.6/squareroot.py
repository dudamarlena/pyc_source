# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/macros/math/squareroot.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import MacroCommand
from math import sqrt

class SquareRootMacro(MacroCommand):
    __domain__ = 'macro'
    __operation__ = 'square-root'

    @property
    def descriptor(self):
        return {'name': 'square-root', 'parameters': {'var1': {'type': 'numeric'}}, 'help': 'square-root returns root from given value'}

    def parse_parameters(self, **params):
        MacroCommand.parse_parameters(self, **params)
        self._var1 = params.get('var1', None)
        if self._var1 is None:
            raise CoilsException('NULL input provided to square-root macro')
        if not isinstance(self._var1, (int, float)):
            raise CoilsException('Non-numeric value provided to square-root macro')
        return

    def run(self):
        self.set_result(sqrt(self._var1))