# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/macros/condition/unless.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import MacroCommand
from command import EvaluationCommand

class UnlessMapMacro(MacroCommand, EvaluationCommand):
    __domain__ = 'macro'
    __operation__ = 'unless'

    @property
    def descriptor(self):
        return {'name': 'evaluate', 'parameters': {'operator': {'type': 'string', 'values': ['>',
                                                '>=',
                                                '<',
                                                '<=',
                                                '=',
                                                '!=',
                                                'equals',
                                                'caseIgnoreEquals']}, 
                          'var1': {'type': 'any'}, 'var2': {'type': 'any'}}, 
           'help': 'Compare var1 and var2 using operator; output inverse of boolean.'}

    def parse_parameters(self, **params):
        raise NotImplementedException('Class not implmented')

    def run(self):
        if self.evaluate(self._boolean, self._var1, self._var2):
            self.set_result(False)
        else:
            self.set_result(True)