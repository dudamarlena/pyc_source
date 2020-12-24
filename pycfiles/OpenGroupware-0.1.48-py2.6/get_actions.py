# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/project/get_actions.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class GetProjectTaskActions(GetCommand):
    __domain__ = 'project'
    __operation__ = 'get-task-actions'

    def __init__(self):
        GetCommand.__init__(self)

    def parse_parameters(self, **params):
        self._limit = params.get('limit', 150)
        if 'id' in params:
            self.project = self.get_by_id(params.get('id'))
        elif 'project' in params:
            self.project = params['project']
        else:
            self.project = None
        return

    def get_by_id(self, object_id):
        project = self._ctx.run_command('project::get', id=int(object_id))
        if project is None:
            raise CoilsException('Unable to retrieve task actions for specified project')
        return project

    def run(self, **params):
        self.access_check = False
        self.mode = RETRIEVAL_MODE_MULTIPLE
        db = self._ctx.db_session()
        if self.project is None:
            inner_query = db.query(Project.object_id).join(ProjectAssignment).filter(and_(ProjectAssignment.child_id.in_(self._ctx.context_ids), Project.status != 'archived')).subquery()
            query = db.query(TaskAction).join(Task, Task.notes).filter(Task.project_id.in_(inner_query)).order_by(TaskAction.date.desc()).limit(self._limit)
        else:
            print 'project actions'
            query = db.query(TaskAction).join(Task, Task.notes).filter(Task.project_id == self.project.object_id).order_by(TaskAction.date.desc()).limit(self._limit)
        self.set_return_value(query.all())
        return