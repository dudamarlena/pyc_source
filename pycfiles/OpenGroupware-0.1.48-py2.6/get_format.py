# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/get_format.py
# Compiled at: 2012-10-12 07:02:39
import pickle
from sqlalchemy import *
from coils.core import *
from coils.logic.workflow.formats import Format

class GetFormat(Command):
    __domain__ = 'format'
    __operation__ = 'get'

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.name = params.get('name', None)
        return

    def run(self):
        if self.name is None:
            result = []
            for name in Format.ListFormats():
                result.append(Format.Load(name))

            self._result = result
        else:
            format = Format.Load(self.name)
            self._result = format
        return