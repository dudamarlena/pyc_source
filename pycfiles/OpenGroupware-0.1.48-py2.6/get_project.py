# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/project/get_project.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand
from coils.foundation import Project, Appointment, Contact, Enterprise

class GetProject(GetCommand):
    __domain__ = 'project'
    __operation__ = 'get'
    mode = None

    def __init__(self):
        GetCommand.__init__(self)

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)
        self._number = None
        self._name = None
        if 'number' in params:
            self._number = params.get('number')
        elif 'name' in params:
            self._name = params.get('name')
        return

    def run(self, **params):
        db = self._ctx.db_session()
        if self._number is None and self._name is None:
            query = db.query(Project).filter(and_(Project.object_id.in_(self.object_ids), Project.status != 'archived'))
        elif self._number is not None:
            self.set_single_result_mode()
            query = db.query(Project).filter(and_(Project.number == self._number, Project.status != 'archived'))
        elif self._name is not None:
            self.set_single_result_mode()
            query = db.query(Project).filter(and_(Project.name == self._name, Project.status != 'archived'))
        else:
            raise CoilsException('No criteria provided to project::get')
        self.set_return_value(query.all())
        return