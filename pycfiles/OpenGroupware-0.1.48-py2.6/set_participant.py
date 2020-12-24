# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/schedular/set_participant.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.foundation import *
from globals import *

class SetParticipant(Command):
    """ Set the status, role, comment, and rsvp or a participant, or add a participant
        Supported parameters are: appointment [entity] OR appoinment_id [int] , status,
        role, comment, rsvp [int] """
    __domain__ = 'participant'
    __operation__ = 'set'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.appointment = params.get('appointment', None)
        self.appointment_id = params.get('appointment_id', None)
        self.status = params.get('status', None)
        self.role = params.get('role', None)
        self.comment = params.get('comment', None)
        self.participant_id = params.get('participant_id', None)
        self.rsvp = params.get('rsvp', None)
        return

    def polish_parameters(self):
        if self.status is not None:
            self.status = self.status.upper().strip()
        if self.role is not None:
            self.role = self.role.upper().strip()
        if self.comment is not None:
            self.comment = self.comment.strip()
        return

    def check_parameters(self):
        if self.status is not None and self.status not in COILS_PARTICIPANT_STATUS:
            raise CoilsException('Undefined participant status in participation update')
        if self.role is not None and self.role not in COILS_PARTICIPANT_ROLES:
            raise CoilsException('Undefined participant role in participation update')
        return

    def run(self):
        self.polish_parameters()
        self.check_parameters()
        self._result = False
        if self.participant_id is None:
            raise 'No participant identified for participant update'
        if self.appointment is None and self.appointment_id is not None:
            self.appointment = self._ctx.run_command('appointment::get', id=int(self.appointment_id))
        if self.appointment is None:
            raise 'Participant set cannot identify the relevant appointment'
        else:
            self._result = True
        values = {'appointment_id': int(self.appointment_id), 'participant_id': int(self.participant_id)}
        if self.role is not None:
            values['participant_role'] = self.role
        if self.comment is not None:
            values['comment'] = self.comment
        if self.status is not None:
            values['participant_status'] = self.status
        if self.rsvp is not None:
            values['rsvp'] = int(self.rsvp)
        for participant in self.appointment.participants:
            if participant.participant_id == int(self.participant_id):
                participant.take_values(values, COILS_PARTICIPANT_STATUS)
                participant._db_status = 'updated'
                break
        else:
            db = self._ctx.db_session()
            participant = Participant()
            participant.take_values(values, COILS_PARTICIPANT_STATUS)
            db.add(participant)

        return