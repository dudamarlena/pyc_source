# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/schedular/delete_participants.py
# Compiled at: 2012-10-12 07:02:39
from coils.foundation import *
from coils.core import *

class DeleteParticipants(Command):
    __domain__ = 'appointment'
    __operation__ = 'delete-participants'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.obj = params.get('object', None)
        self.appointment_id = params.get('id', None)
        return

    def run(self):
        self._result = False
        db = self._ctx.db_session()
        if self.obj is None and self.appointment_id is not None:
            self.obj = self._ctx.run_command('appointment::get', id=self.appointment_id)
            if self.obj is None:
                raise CoilsException('Unable to marshall specified appointment for deletion.')
        elif self.obj is None:
            raise CoilsException('No Appointment provided to deletion.')
        query = db.query(Participant).filter(Participant.appointment_id == self.obj.object_id)
        for participant in query.all():
            self._ctx.db_session().delete(participant)

        self._result = True
        return