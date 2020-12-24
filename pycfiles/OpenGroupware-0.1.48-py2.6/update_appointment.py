# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/schedular/update_appointment.py
# Compiled at: 2012-10-12 07:02:39
from coils.foundation import *
from coils.core import *
from coils.core.logic import UpdateCommand
from keymap import COILS_APPOINTMENT_KEYMAP
from command import AppointmentCommand

class UpdateAppointment(UpdateCommand, AppointmentCommand):
    __domain__ = 'appointment'
    __operation__ = 'set'

    def prepare(self, ctx, **params):
        self.keymap = COILS_APPOINTMENT_KEYMAP
        UpdateCommand.prepare(self, ctx, **params)

    def get_by_id(self, object_id, access_check):
        return self._ctx.run_command('appointment::get', id=object_id, access_check=access_check)

    def parse_parameters(self, **params):
        UpdateCommand.parse_parameters(self, **params)

    def create_resource_string(self):
        if '_RESOURCES' in self.values:
            resources = []
            for entity in self.values.get('_RESOURCES'):
                if 'objectId' in entity:
                    resources.append(int(entity.get('objectId')))

            names = self._ctx.run_command('resource::get-names', ids=resources)
            self.obj.set_resource_names(names)

    def do_participants(self):
        participants = KVC.subvalues_for_key(self.values, ['_PARTICIPANTS', 'participants'])
        if len(participants) > 0:
            self._ctx.run_command('appointment::set-participants', participants=participants, appointment=self.obj)

    def run(self):
        UpdateCommand.run(self)
        self.create_resource_string()
        self.do_participants()
        self.set_ics_properties()