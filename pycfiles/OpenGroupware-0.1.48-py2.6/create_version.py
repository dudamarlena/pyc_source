# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/blob/create_version.py
# Compiled at: 2012-10-12 07:02:39
import shutil
from coils.foundation import *
from coils.core import *
from coils.core.logic import CreateCommand
from command import BLOBCommand

class CreateVersion(CreateCommand, BLOBCommand):
    __domain__ = 'document'
    __operation__ = 'new-version'

    def prepare(self, ctx, **params):
        self.keymap = {}
        self.entity = DocumentVersion
        CreateCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'document' in params:
            self._document = params.get('document')
        else:
            raise CoilsException('Request to create a version with no document.')
        self._rfile = params.get('handle', None)
        return

    def run(self):
        if self._document.project_id is not None:
            self._document.version_count += 1
            self.save()
            manager = self.get_manager(self._document)
            self.store_to_version(manager, self._document, self._rfile)
            self.store_to_self(manager, self._document, self._rfile)
        else:
            raise NotImplementedException('Non-project documents not yet supported')
        self._result = self.obj
        return