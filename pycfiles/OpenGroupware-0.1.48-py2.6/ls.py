# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/blob/ls.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class ListFolder(GetCommand):
    __domain__ = 'folder'
    __operation__ = 'ls'
    mode = None

    def __init__(self):
        GetCommand.__init__(self)

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)
        if len(self.object_ids) == 0:
            if 'folder' in params:
                self.object_ids.append(params['folder'].object_id)
            else:
                raise CoilsException('No folder specified to list')
        self._name = params.get('name', None)
        return

    def run(self):
        db = self._ctx.db_session()
        self.set_multiple_result_mode()
        contents = []
        if self._name is None:
            query = db.query(Document).filter(and_(Document.folder_id.in_(self.object_ids), Folder.status != 'archived'))
        else:
            filename = ('.').join(self._name.split('.')[:-1])
            extension = self._name.split('.')[-1:][0]
            query = db.query(Document).filter(and_(Document.folder_id.in_(self.object_ids), Document.name == filename, Document.extension == extension, Document.status != 'archived'))
        result = query.all()
        contents.extend(result)
        if self._name is None:
            query = db.query(Folder).filter(and_(Folder.folder_id.in_(self.object_ids), Folder.status != 'archived'))
        else:
            query = db.query(Folder).filter(and_(Folder.folder_id.in_(self.object_ids), Folder.name == self._name, Folder.status != 'archived'))
        result = query.all()
        contents.extend(result)
        self.set_return_value(contents)
        return