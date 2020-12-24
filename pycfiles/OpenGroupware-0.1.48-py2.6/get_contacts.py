# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/project/get_contacts.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class GetProjectContacts(GetCommand):
    __domain__ = 'project'
    __operation__ = 'get-contacts'

    def __init__(self):
        GetCommand.__init__(self)

    def parse_parameters(self, **params):
        if 'id' in params:
            self.project_id = int(params['id'])
        elif 'project' in params:
            self.project_id = params['project'].object_id
        elif 'object' in params:
            self.project_id = params['object'].object_id
        else:
            raise CoilsException('No project or project id provided to project::get-contacts')

    def run(self, **params):
        self.access_check = False
        self.mode = RETRIEVAL_MODE_MULTIPLE
        db = self._ctx.db_session()
        query = db.query(ProjectAssignment).filter(and_(ProjectAssignment.parent_id == self.project_id, ProjectAssignment.child_id != None))
        object_ids = [ int(entity.child_id) for entity in query.all() ]
        self.set_return_value(self._ctx.run_command('contact::get', ids=object_ids))
        return