# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/macros/strings/substring.py
# Compiled at: 2012-10-12 07:02:39
import re
from coils.core import *
from coils.core.logic import MacroCommand

class SubstringMacro(MacroCommand):
    __domain__ = 'macro'
    __operation__ = 'substring'

    @property
    def descriptor(self):
        return {'name': 'substring', 'parameters': {'var1': {'type': 'any'}, 'var2': {'type': 'any'}}, 'help': 'Returns substring if found from original string'}

    def parse_parameters(self, **params):
        MacroCommand.parse_parameters(self, **params)
        self._var1 = params.get('var1', None)
        self._var2 = params.get('var2', None)
        if self._var1 is None or self._var2 is None:
            raise CoilsException('NULL input provided to substring macro')
        return

    def run(self):
        m = re.search(str(self._var2), str(self._var1))
        if m:
            self.set_result(str(self._var1)[m.start():m.end()])
        else:
            self.set_result('')