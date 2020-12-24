# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/account/remove_membership.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *

class RemoveMembership(Command):
    __domain__ = 'account'
    __operation__ = 'remove-membership'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self._user_id = int(params.get('account_id'))

    def run(self):
        self._result = []
        db = self._ctx.db_session()
        query = db.query(Team, CompanyAssignment).filter(and_(Team.object_id == CompanyAssignment.parent_id, CompanyAssignment.child_id == self._user_id))
        teams = []
        assignments = []
        for result in query.all():
            if result[0].object_id not in teams:
                teams.append(result[0].object_id)
            assignments.append(result[1].object_id)

        if len(teams) > 0:
            for team in db.query(Team).filter(Team.object_id.in_(teams)).all():
                team.version = team.version + 1
                self.log.debug(('Removing assignment to Team id#{0} from account id#{1}').format(team.object_id, self._user_id))

            count = db.query(CompanyAssignment).filter(CompanyAssignment.object_id.in_(assignments)).delete(synchronize_session='fetch')
            self.log.debug(('{0} team assignments deleted').format(count))
            self._result.append(count)
        else:
            self._result.append(0)
        query = db.query(Enterprise, CompanyAssignment).filter(and_(Enterprise.object_id == CompanyAssignment.parent_id, CompanyAssignment.child_id == self._user_id))
        enterprises = []
        assignments = []
        for result in query.all():
            if result[0].object_id not in enterprises:
                enterprises.append(result[0].object_id)
            assignments.append(result[1].object_id)

        if len(enterprises) > 0:
            for enterprise in db.query(Enterprise).filter(Enterprise.object_id.in_(enterprises)).all():
                enterprise.version = enterprise.version + 1
                self.log.debug(('Removing assignment to Enterprise id#{0} from account id#{1}').format(enterprise.object_id, self._user_id))

            count = db.query(CompanyAssignment).filter(CompanyAssignment.object_id.in_(assignments)).delete(synchronize_session='fetch')
            self.log.debug(('{0} enterprise assignments deleted').format(count))
            self._result.append(count)
        else:
            self._result.append(0)
        query = db.query(Project, ProjectAssignment).filter(and_(Project.object_id == ProjectAssignment.parent_id, ProjectAssignment.child_id == self._user_id))
        projects = []
        assignments = []
        for result in query.all():
            if result[0].object_id not in projects:
                projects.append(result[0].object_id)
            assignments.append(result[1].object_id)

        if len(projects) > 0:
            for project in db.query(Project).filter(Project.object_id.in_(projects)).all():
                project.version = project.version + 1
                self.log.debug(('Removing assignment to Project id#{0} from account id#{1}').format(project.object_id, self._user_id))

            count = db.query(ProjectAssignment).filter(ProjectAssignment.object_id.in_(assignments)).delete(synchronize_session='fetch')
            self.log.debug(('{0} project assignments deleted').format(count))
            self._result.append(count)
        else:
            self._result.append(0)