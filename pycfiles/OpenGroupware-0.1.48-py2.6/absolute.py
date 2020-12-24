# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/macros/math/absolute.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import MacroCommand

class AbsoluteMacro(MacroCommand):
    __domain__ = 'macro'
    __operation__ = 'absolute'

    @property
    def descriptor(self):
        return {'name': 'and', 'parameters': {'var1': {'type': 'numeric'}}, 'help': ''}

    def parse_parameters(self, **params):
        MacroCommand.parse_parameters(self, **params)
        self._var1 = params.get('var1', None)
        if self._var1 is None:
            raise CoilsException('NULL input provided to absolute macro')
        try:
            self._var1 = float(self._var1)
        except ValueError:
            raise CoilsException('Non-numeric input given to absolute macro')

        return

    def run(self):
        self.set_result(abs(self._var1))