# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/delete_table.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.logic.workflow.tables import Table

class DeleteTable(Command):
    __domain__ = 'table'
    __operation__ = 'delete'

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.obj = params.get('object')

    def run(self, **params):
        if self.obj is not None:
            Table.Delete(self.obj.get_name())
            self.obj = None
        self._result = None
        return