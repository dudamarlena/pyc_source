# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/project/set_contacts.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.foundation import diff_id_lists, Contact, Enterprise, ProjectAssignment
from command import ProjectCommand

class SetProjectContacts(Command, ProjectCommand):
    __domain__ = 'project'
    __operation__ = 'set-contacts'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'project' in params:
            self._project_id = params.get('project').object_id
        elif 'project_id' in params:
            self._project_id = int(params.get('project_id'))
        else:
            raise CoilsException('No project specified for project::set-enterprises')
        self._contact_ids = []
        if 'contacts' in params:
            for assignment in params.get('contacts'):
                self._contact_ids.append(int(assignment.object_id))

        if 'contact_ids' in params:
            self._contact_ids = [ int(o) for o in params.get('contact_ids') ]

    def run(self):
        db = self._ctx.db_session()
        query = db.query(ProjectAssignment).filter(ProjectAssignment.parent_id == self._project_id)
        assigned_to = [ int(o.child_id) for o in query.all() ]
        print ('  Assigned: {0}').format(assigned_to)
        assigned_to = self._ctx.type_manager.filter_ids_by_type(assigned_to, 'Contact')
        print ('  Assigned: {0}').format(assigned_to)
        print ('  Enterprises: {0}').format(self._contact_ids)
        (inserts, deletes) = diff_id_lists(self._contact_ids, assigned_to)
        print ' ENTERPRISE ASSIGNMENTS '
        print ('  Insert: {0}').format(inserts)
        print ('  Delete: {0}').format(deletes)
        print
        assigned_to = None
        query = None
        if len(inserts) > 0:
            for contact_id in inserts:
                db.add(ProjectAssignment(self._project_id, contact_id))

        if len(deletes) > 0:
            db.query(ProjectAssignment).filter(and_(ProjectAssignment.child_id.in_(deletes), ProjectAssignment.parent_id == self._project_id)).delete(synchronize_session='fetch')
        return