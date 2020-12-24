# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/schedular/create_appointment.py
# Compiled at: 2012-10-12 07:02:39
from coils.foundation import *
from coils.core import *
from coils.core.logic import CreateCommand
from keymap import COILS_APPOINTMENT_KEYMAP
from command import AppointmentCommand

class CreateAppointment(CreateCommand, AppointmentCommand):
    __domain__ = 'appointment'
    __operation__ = 'new'

    def prepare(self, ctx, **params):
        self.keymap = COILS_APPOINTMENT_KEYMAP
        self.entity = Appointment
        CreateCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        CreateCommand.parse_parameters(self, **params)

    def do_participants(self):
        participants = KVC.subvalues_for_key(self.values, ['_PARTICIPANTS', 'participants'])
        if len(participants) == 0:
            participants = [{'companyId': self._ctx.account_id}]
        self._ctx.run_command('appointment::set-participants', participants=participants, appointment=self.obj)

    def create_resource_string(self):
        if '_RESOURCES' in self.values:
            resources = []
            for entity in self.values.get('_RESOURCES'):
                if 'objectId' in entity:
                    resources.append(int(entity.get('objectId')))

            names = self._ctx.run_command('resource::get-names', ids=resources)
            self.obj.set_resource_names(names)

    def do_values(self, cyclic=False, parent_date_id=None):
        CreateCommand.run(self)
        self.create_resource_string()
        self.do_participants()
        if cyclic:
            if parent_date_id is None:
                self.obj.parent_id = self.obj.object_id
            else:
                self.obj.parent_id = parent_date_id
        else:
            self.obj.parent_id = None
        self.save()
        self.set_ics_properties()
        return

    def run(self, parent_object_id=None):
        cyclic = False
        if isinstance(self.values, list):
            self.log.debug(('values is a list of {0} items, possible recurrence').format(len(self.values)))
            values_list = self.values
            self.values = values_list[0]
            if len(values_list) > 1:
                self.log.debug(('recurring event with {0} components detected').format(len(values_list)))
                cyclic = True
        self.do_values(cyclic=cyclic)
        if cyclic:
            parent_date_id = self.obj.object_id
            for values in values_list[1:]:
                self.values = values
                self.obj = None
                self.do_values(cyclic=True, parent_date_id=parent_date_id)

        return