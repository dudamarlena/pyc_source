# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/contact/set_projects.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.foundation import diff_id_lists, Contact, ProjectAssignment
from command import ContactCommand

class SetProjects(Command, ContactCommand):
    __domain__ = 'contact'
    __operation__ = 'set-projects'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'contact' in params:
            self._contact_id = params.get('contact').object_id
        elif 'contact_id' in params:
            self._contact_id = int(params.get('contact_id'))
        else:
            raise CoilsException('No contact specified for contact::set-enterprises')
        self._project_ids = []
        if 'projects' in params:
            for project in params.get('projects'):
                self._project_ids.append(int(project.object_id))

        if 'project_ids' in params:
            self._project_ids = [ int(o) for o in params.get('project_ids') ]

    def run(self):
        db = self._ctx.db_session()
        query = db.query(ProjectAssignment).filter(ProjectAssignment.child_id == self._contact_id)
        assigned_to = [ int(o.parent_id) for o in query.all() ]
        (inserts, deletes) = diff_id_lists(self._project_ids, assigned_to)
        assigned_to = None
        query = None
        if len(inserts) > 0:
            for project_id in inserts:
                db.add(ProjectAssignment(project_id, self._contact_id))

        if len(deletes) > 0:
            db.query(ProjectAssignment).filter(and_(ProjectAssignment.parent_id.in_(deletes), ProjectAssignment.child_id == self._contact_id)).delete(synchronize_session='fetch')
        return