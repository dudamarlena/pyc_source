# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/project/get_root_folder.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class GetProjectRootFolder(GetCommand):
    __domain__ = 'project'
    __operation__ = 'get-root-folder'

    def __init__(self):
        GetCommand.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'id' in params:
            self.project_id = int(params['id'])
        elif 'project' in params:
            self.project_id = params['project'].object_id
        else:
            raise CoilsException('No project or project id provided to project::get-root-folder')

    def run(self, **params):
        self.mode = RETRIEVAL_MODE_SINGLE
        db = self._ctx.db_session()
        query = db.query(Folder).filter(and_(Folder.project_id == self.project_id, Folder.folder_id == None, Folder.status != 'archived'))
        self.set_return_value(query.all())
        return