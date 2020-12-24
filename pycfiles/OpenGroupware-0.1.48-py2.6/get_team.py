# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/team/get_team.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class GetTeam(GetCommand):
    __domain__ = 'team'
    __operation__ = 'get'
    mode = None

    def __init__(self):
        GetCommand.__init__(self)

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)
        if 'member_id' in params:
            self.query_by = 'membership'
            self.set_multiple_result_mode()
            self.object_ids.append(int(params['member_id']))
        elif 'email' in params:
            self.query_by = 'email'
            self.set_multiple_result_mode()
            self._email = params['email'].lower()
        elif 'name' in params:
            self.query_by = 'name'
            self.set_single_result_mode()
            self._name = params['name']

    def run(self):
        db = self._ctx.db_session()
        if self.query_by == 'object_id':
            query = db.query(Team).filter(Team.object_id.in_(self.object_ids))
        elif self.query_by == 'membership':
            query = db.query(Team)
            query = query.join(CompanyAssignment)
            query = query.filter(CompanyAssignment.child_id.in_(self.object_ids))
        elif self.query_by == 'email':
            query = db.query(Team).filter(Team.email.ilike(self._email))
        elif self.query_by == 'name':
            query = db.query(Team).filter(Team.name.ilike(self._name))
        else:
            self.set_multiple_result_mode()
            query = db.query(Team)
        self.disable_access_check()
        self.set_return_value(query.all())