# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/schedular/delete_appointment.py
# Compiled at: 2012-10-12 07:02:39
from coils.foundation import *
from coils.core import *
from coils.core.logic import DeleteCommand

class DeleteAppointment(DeleteCommand):
    __domain__ = 'appointment'
    __operation__ = 'delete'

    def delete_comment(self):
        self._ctx.run_command('appointment::delete-comment', appointment=self.obj)

    def delete_participants(self):
        self._ctx.run_command('appointment::delete-participants', object=self.obj)

    def run(self):
        if self.obj is None:
            raise CoilsException('No appointment provided for deletion.')
        self.delete_participants()
        self.delete_comment()
        DeleteCommand.run(self)
        return