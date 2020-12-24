# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/task/delete_task.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import DeleteCommand
from command import TaskCommand

class DeleteTask(DeleteCommand, TaskCommand):
    __domain__ = 'task'
    __operation__ = 'delete'

    def prepare(self, ctx, **params):
        DeleteCommand.prepare(self, ctx, **params)

    def get_by_id(self, object_id, access_check):
        return self._ctx.run_command('task::get', id=object_id, access_check=access_check)

    def run(self):
        db = self._ctx.db_session()
        for note in self.obj.notes:
            db.delete(note)

        DeleteCommand.run(self)
        self.notify()