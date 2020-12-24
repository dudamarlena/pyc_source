# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/blob/get_drawer.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class GetDrawer(GetCommand):
    __domain__ = 'drawer'
    __operation__ = 'get'
    mode = None

    def __init__(self):
        GetCommand.__init__(self)

    def run(self):
        db = self._ctx.db_session()
        if len(self.object_ids) == 0:
            query = db.query(Note).filter(and_(Folder.status != 'archived', Folder.company_id == self._ctx.account_id, Folder.folder_id == None, Folder.project_id == None))
        else:
            query = db.query(Note).filter(and_(Folder.object_id.in_(self.object_ids), Folder.status != 'archived', Folder.company_id == self._ctx.account_id, Folder.folder_id == None, Folder.project_id == None))
        self.set_return_value(self.add_comments(query.all()))
        return