# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/schedular/get_appointment_range.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime, timedelta
from sqlalchemy import *
from coils.foundation import *
from coils.core import *
from coils.core.logic import GetCommand
from utility import get_panel_ids
from command import AppointmentCommand

class GetAppointmentRange(GetCommand, AppointmentCommand):
    __domain__ = 'appointment'
    __operation__ = 'get-range'

    def __init__(self):
        GetCommand.__init__(self)

    def prepare(self, ctx, **params):
        self.start = datetime.today()
        self.span = timedelta(days=8)
        self.end = self.start + self.span
        self.parts = []
        self.names = None
        self.kinds = None
        self.mode = 2
        GetCommand.prepare(self, ctx, **params)
        return

    def set_assumed_participants(self):
        self.parts.append(self._ctx.account_id)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if bool(params.get('visible_only', False)):
            self._required_right = 'v'
        else:
            self._required_right = 'l'
        self.parse_range(start=params.get('start', None), end=params.get('end', None), span=params.get('span', None))
        self.parse_participants(participants=params.get('participants', None), exclude=params.get('exclude', None), resources=params.get('resources', None))
        self.parse_kinds(kinds=params.get('kinds', None))
        return

    def parse_range(self, start=None, end=None, span=None):
        if start is None:
            self.start = self._ctx.get_utctime() - timedelta(days=1)
        else:
            self.start = start
        if span is None:
            self.span = timedelta(days=45)
        else:
            self.span = timedelta(days=int(span))
            self.end = self.start + self.span
        if end is None:
            self.end = self.start + self.span
        else:
            self.end = end
        return

    def parse_participants(self, participants=None, exclude=None, resources=None):
        if participants is None:
            self.log.debug('no participants specified, assuming panel.')
            self.set_assumed_participants()
        else:
            if isinstance(participants, list):
                for p in participants:
                    if hasattr(p, 'object_id'):
                        self.parts.append(p.object_id)
                    elif isinstance(p, int):
                        self.parts.append(p)

            kinds = self._ctx.type_manager.group_ids_by_type(self.parts)
            if kinds.has_key('Resource'):
                if self.names is None:
                    self.names = []
                name_list = self._ctx.run_command('resource::get-names', ids=kinds['Resource'])
                self.log.debug(('converted participant ids {0} into resource names {1}.').format(kinds['Resource'], name_list))
                if name_list is not None:
                    for name in name_list:
                        self.names.append(name)

                for object_id in kinds['Resource']:
                    self.parts.remove(object_id)

                self.log.debug('removed resource object ids from participant list')
        self.flatten_teams()
        if resources is None:
            pass
        else:
            if self.names is None:
                self.names = []
            if isinstance(resources, list):
                self.names.extend(params['resources'])
            else:
                self.names.extend(params['resources'].split(','))
        return

    def parse_kinds(self, kinds=None):
        if kinds is None:
            pass
        elif isinstance(kinds, list):
            self.kinds = params['kinds']
        else:
            self.kinds = []
            for kind in kinds.split(','):
                self.kinds.append(kind.lower().strip())

            return

    def flatten_teams(self):
        tm = self._ctx.type_manager
        index = tm.group_ids_by_type(self.parts)
        if index.has_key('Team'):
            teams = self._ctx.run_command('team::get', ids=index['Team'], access_check=False)
            for team in teams:
                for member in team.members:
                    if member.child_id not in self.parts:
                        self.parts.append(member.child_id)

    def get_query(self):
        db = self._ctx.db_session()
        query = db.query(Appointment)
        query = query.join(Participant)
        query = query.join(DateInfo)
        query = query.filter(Appointment.status != 'archived')
        query = query.filter(Appointment.end > self.start)
        query = query.filter(Appointment.start < self.end)
        if self.kinds is not None:
            query = query.filter(Appointment.kind.in_(self.kinds))
        participant_clause = or_()
        self.log.debug(('participants: {0}').format(self.parts))
        participant_clause.append(Participant.participant_id.in_(self.parts))
        if self.names is not None:
            participant_clause.append(self.get_resource_filter())
        query = query.filter(participant_clause)
        return query

    def get_resource_filter(self):
        if self.names is None:
            return
        else:
            outer = or_()
            for name in self.names:
                inner = or_()
                inner.append(Appointment._resource_names == name)
                inner.append(Appointment._resource_names.ilike('%s,%%' % name))
                inner.append(Appointment._resource_names.ilike('%%,%s,%%' % name))
                inner.append(Appointment._resource_names.ilike('%%,%s' % name))
                outer.append(inner)

            return outer

    def add_result(self, appointment):
        if appointment not in self._result:
            self._result.append(appointment)

    def run(self):
        query = self.get_query()
        self.set_return_value(self.load_special_values(query.all()), right=self._required_right)


class GetAppointmentOverviewRange(GetAppointmentRange):
    __domain__ = 'appointment'
    __operation__ = 'get-overview-range'

    def set_assumed_participants(self):
        self.parts.extend(get_panel_ids(self._ctx, self._ctx.account_id))