# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/blob/move_document.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.foundation import *
from command import BLOBCommand

class MoveDocument(SetCommand, BLOBCommand):
    __domain__ = 'document'
    __operation__ = 'move'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        SetCommand.parse_parameters(self, **params)
        self.obj = params.get('document', None)
        self.filename = params.get('to_filename', None)
        self.folder = params.get('to_folder', None)
        return

    def get_by_id(self, object_id, access_check):
        return self._ctx.run_command('document::get', id=object_id, access_check=access_check)

    def run(self):
        if self.obj.folder_id != self.folder.object_id:
            if self.obj.project_id != self.folder.project_id:
                raise NotImplementedException('Documents cannot be moved between projects')
                self.document.project_id = self.folder.project_id
                if self.folder.project:
                    self.increment_object_version(self.folder.project)
            self.obj.folder_id = self.folder.object_id
            self.folder.modified = self._ctx.get_utctime()
            self.increment_object_version(self.obj.folder)
            self.folder.status = 'updated'
        if self.filename:
            filename = self.filename.split('.')
            if len(filename) > 1:
                self.obj.extension = filename[(-1)]
                self.obj.name = ('.').join(filename[:-1])
            else:
                self.obj.extension = None
                self.obj.name = self.filename
        self.increment_version()
        self.set_result(self.obj)
        return