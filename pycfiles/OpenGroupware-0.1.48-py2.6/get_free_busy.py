# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/schedular/get_free_busy.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime, timedelta
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand
from command import AppointmentCommand

class GetFreeBusy(GetCommand, AppointmentCommand):
    __domain__ = 'schedular'
    __operation__ = 'get-free-busy'

    def __init__(self):
        GetCommand.__init__(self)

    def prepare(self, ctx, **params):
        GetCommand.prepare(self, ctx, **params)
        self.set_multiple_result_mode()

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if bool(params.get('visible_only', False)):
            self._required_right = 'v'
        else:
            self._required_right = 'l'
        self.start = params.get('start', datetime.today() - timedelta(days=30))
        self.end = params.get('end', datetime.today() + timedelta(days=90))
        self.target = params.get('object', None)
        return

    def lookup_teams(self):
        return [ team.object_id for team in self._ctx.run_command('team::get', member_id=self.target.object_id) if team.object_id != 10003
               ]

    def get_context_ids(self):
        self.cids = [
         self.target.object_id]
        self.cids.extend(self.lookup_teams())

    def get_query(self):
        db = self._ctx.db_session()
        query = db.query(Appointment)
        query = query.join(Participant).filter(Participant.participant_id.in_(self.cids))
        query = query.filter(Appointment.status != 'archived')
        query = query.filter(Appointment.end > self.start)
        query = query.filter(Appointment.start < self.end)
        return query

    def run(self):
        self.disable_access_check()
        self.get_context_ids()
        query = self.get_query()
        result = []
        for appointment in query.all():
            record = {'start': appointment.start, 'end': appointment.end, 'busy': True, 
               'team': True}

            def update_record(record, role, status, isteam):
                record['team'] = isteam
                if role == 'NON-PARTICIPANT':
                    record['busy'] = False
                elif status == 'DECLINED':
                    record['busy'] = False

            for participant in appointment.participants:
                if participant.object_id == self.target.object_id:
                    update_record(record, role=participant.participant_role, status=participant.participant_status, isteam=False)
                    break
                elif participant.object_id in self.cids:
                    update_record(record, role=participant.participant_role, status=participant.participant_status, isteam=True)

            result.append(record)

        self.set_return_value(result)