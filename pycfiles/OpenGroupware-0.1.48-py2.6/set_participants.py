# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/schedular/set_participants.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.foundation import *
from globals import *
from keymap import COILS_PARTICIPANT_KEYMAP

class EventMember(KVC):

    def __init__(self):
        self.participant_role = 'REQ-PARTICIPANT'
        self.comment = ''
        self.rsvp = 0
        self.participant_status = 'NEEDS-ACTION'
        self.participant_id = None
        self.appointment_id = None
        return


class SetParticipants(Command):
    """ Set the status, role, comment, and rsvp or a participant, or add a participant
        Supported parameters are: appointment [entity] OR appoinment_id [int] , status,
        role, comment, rsvp [int] """
    __domain__ = 'appointment'
    __operation__ = 'set-participants'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.appointment = params.get('appointment', None)
        self.appointment_id = params.get('appointment_id', None)
        self.participants = params.get('participants', [])
        return

    def map_participants(self):
        result = []
        self.participant_ids = []
        for participant in self.participants:
            x = EventMember()
            x.take_values(participant, COILS_PARTICIPANT_KEYMAP)
            x.appointment_id = self.appointment.object_id
            self.participant_ids.append(x.participant_id)
            result.append(x)

        self.participants = result

    def check_parameters(self):
        if self.appointment_id is None and self.appointment is None:
            raise CoilsException('No appointment provided to set-participants')
        return

    def run(self):
        db = self._ctx.db_session()
        self.check_parameters()
        self.map_participants()
        if self.appointment is None:
            self.appointment = self._ctx.run_command('appointment::get', id=int(self.appointment_id))
        if self.appointment is None:
            raise 'Participant set cannot identify the relevant appointment'
        else:
            self._result = True
        import pprint
        for x in self.participants:
            self.log.debug(pprint.pformat(x))
            for y in self.appointment.participants:
                self.log.debug(pprint.pformat(y))
                if y.participant_id is not None:
                    if x.participant_id == int(y.participant_id):
                        y.take_values(x, None)
                        y._db_status = 'updated'
                        break
                else:
                    self.log.error(('NULL participantId# encountered in appointmentId#{0}').format(self.appointment.object_id))
            else:
                participant = Participant()
                participant.take_values(x, None)
                db.add(participant)

        query = db.query(Participant).filter(and_(Participant.appointment_id == self.appointment.object_id, not_(Participant.participant_id.in_(self.participant_ids))))
        count = 0
        for x in query.all():
            db.delete(x)
            count = count + 1

        self.log.debug(('{0} participants deleted from appointment.').format(count))
        return