# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/blob/get_blob.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class GetBLOB(GetCommand):
    __domain__ = 'blob'
    __operation__ = 'get'

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)
        if self.mode == 2:
            raise CoilsException('Multi-get mode not supported for BLOB retrieval!')
        self.version = params.get('version', 0)
        self.sink = params.get('return', 'handle')

    def run(self, **params):
        db = self._ctx.db_session()
        query = db.query(Document).filter(Document.object_id.in_(self.object_ids))
        for blob in query.all():
            project = self._ctx.run_command('project::get', id=blob.project_id, access_check=False)
            if project is not None:
                ds = blob_manager_for_project(project)

        return