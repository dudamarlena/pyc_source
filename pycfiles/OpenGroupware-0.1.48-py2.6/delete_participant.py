# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/schedular/delete_participant.py
# Compiled at: 2012-10-12 07:02:39
from coils.foundation import *
from coils.core import *
from coils.core.logic import DeleteCommand
from keymap import COILS_PARTICIPANT_KEYMAP

class DeleteParticipant(DeleteCommand):
    __domain__ = 'participant'
    __operation__ = 'delete'

    def __init__(self):
        DeleteCommand.__init__(self)

    def parse_parameters(self, **params):
        DeleteCommand.parse_parameters(self, **params)
        if self.obj is None:
            self.appointment = params.get('appointment', None)
            self.appointment_id = params.get('appointment_id', None)
            self.participant_id = params.get('participant_id', None)
        return

    def run(self, **params):
        if self.obj is None:
            db = self._ctx.db_session()
            if self.appointment_id is None and self.appointment is not None:
                appointment_id = self.appointment.object_id
            elif self.appointment_id is not None:
                appointment_id = self.appointment_id
            else:
                raise CoilsException('No appointment specified for participant deletion')
            if self.participant_id is None:
                raise CoilsException('No participant specified for participant deletion')
            query = db.query(Participant).filter(and_(Participant.appointment_id == appointment_id, Participant.participant_id == self.participant_id))
            self.obj = query.first()
            if self.obj is None:
                raise CoilsException('Unable to resolve participant for deletion.')
        DeleteCommand.run(self)
        return