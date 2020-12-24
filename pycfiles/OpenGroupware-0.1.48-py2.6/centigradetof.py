# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/macros/units/centigradetof.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import MacroCommand

class CentigradeToFarenheitMacro(MacroCommand):
    __domain__ = 'macro'
    __operation__ = 'centigrade-to-farenheit'

    @property
    def descriptor(self):
        return {'name': 'and', 'parameters': {}, 'help': ''}

    def parse_parameters(self, **params):
        MacroCommand.parse_parameters(self, **params)