# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/blob/get_folder.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class GetFolder(GetCommand):
    __domain__ = 'folder'
    __operation__ = 'get'
    mode = None

    def __init__(self):
        GetCommand.__init__(self)

    def run(self):
        db = self._ctx.db_session()
        query = db.query(Folder).filter(and_(Folder.object_id.in_(self.object_ids), Folder.status != 'archived'))
        self.set_return_value(query.all())