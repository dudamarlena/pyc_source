# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/macros/condition/ifthen.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import MacroCommand

class IfThenElseMapMacro(MacroCommand):
    __domain__ = 'macro'
    __operation__ = 'ifthenelse'

    @property
    def descriptor(self):
        return {'name': 'ifthenelse', 'parameters': {'boolean': {'type': 'boolean'}, 'var1': {'type': 'any'}, 'var2': {'type': 'any'}}, 'help': 'Output is var1 if boolean is True, var2 if boolean is false'}

    def parse_parameters(self, **params):
        raise NotImplementedException('Class not implmented')

    def run(self):
        if self.evaluate(self._boolean):
            self.set_result(self._var1)
        else:
            self.set_result(self._var2)