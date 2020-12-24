# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/project/unassign_company.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import and_
from coils.core import *
from coils.foundation import Contact, ProjectAssignment

class UnassignCompanyFromProject(Command):
    __domain__ = 'project'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'project' in params:
            self._project_id = parans.get('project').object_id
        elif 'project_id' in params:
            self._project_id = int(params.get('project_id'))
        else:
            raise CoilsException('No project specified for project::assign-contact')

    def run(self):
        db = self._ctx.db_session()
        query = db.query(ProjectAssignment).filter(and_(ProjectAssignment.parent_id == self._project_id, ProjectAssignment.child_id == self._company_id))
        result = query.all()
        if result:
            db.delete(result[0])
            self.set_result_value(True)
        else:
            self.set_result_value(False)


class UnassignContactFromProject(UnassignCompanyFromProject):
    __operation__ = 'unassign-contact'

    def parse_parameters(self, **params):
        AssignCompanyToProject.parse_parameters(self, **params)
        if 'contact' in params:
            self._company_id = params.get('contact').object_id
        elif 'contact_id' in params:
            self._company_id = int(params.get('contact_id'))
        else:
            raise CoilsException('No contact specified for project::unassign-contact')


class UnassignEnterpriseFromProject(UnassignCompanyFromProject):
    __operation__ = 'unassign-enterprise'

    def parse_parameters(self, **params):
        AssignCompanyToProject.parse_parameters(self, **params)
        if 'enterprise' in params:
            self._company_id = params.get('enterprise').object_id
        elif 'enterprise_id' in params:
            self._company_id = int(params.get('enterprise_id'))
        else:
            raise CoilsException('No enterprise specified for project::unassign-enterprise')