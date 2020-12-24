# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/schedular/get_appointment.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand
from coils.foundation import Appointment, Contact
from command import AppointmentCommand

class GetAppointment(GetCommand, AppointmentCommand):
    __domain__ = 'appointment'
    __operation__ = 'get'

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)
        self._caldav_uid = None
        if bool(params.get('visible_only', False)):
            self._required_right = 'v'
        else:
            self._required_right = 'l'
        if len(self.object_ids) == 0:
            if 'uid' in params:
                self._caldav_uid = unicode(params.get('uid'))
                self.mode = RETRIEVAL_MODE_SINGLE
        return

    def run(self, **params):
        db = self._ctx.db_session()
        if self._caldav_uid is None:
            query = db.query(Appointment).filter(and_(Appointment.object_id.in_(self.object_ids), Appointment.status != 'archived'))
        else:
            query = db.query(Appointment).filter(and_(Appointment.status != 'archived', Appointment.caldav_uid == self._caldav_uid))
        self.set_return_value(self.load_special_values(query.all()), right=self._required_right)
        return