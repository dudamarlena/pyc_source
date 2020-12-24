# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/blob/update_document.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime
from coils.foundation import *
from coils.core import *
from coils.core.logic import UpdateCommand
from keymap import COILS_DOCUMENT_KEYMAP
from command import BLOBCommand

class UpdateDocument(UpdateCommand, BLOBCommand):
    __domain__ = 'document'
    __operation__ = 'set'

    def prepare(self, ctx, **params):
        self.keymap = COILS_DOCUMENT_KEYMAP
        self.entity = Document
        UpdateCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        UpdateCommand.parse_parameters(self, **params)
        self._folder = params.get('folder', None)
        self._project = params.get('project', None)
        self._appointment = params.get('appointment', None)
        self._company = params.get('contact', params.get('enterprise', None))
        self._name = params.get('name', None)
        self._annotation = params.get('annotation', None)
        self._input = params.get('handle', None)
        return

    def run(self):
        UpdateCommand.run(self)
        if self._name is not None:
            self.obj.extension = self._name.split('.')[(-1)]
            self.obj.name = ('.').join(self._name.split('.')[:-1])
        self.obj.modified = self._ctx.get_utctime()
        self.obj.status = 'updated'
        self.set_context(self.obj, folder=self._folder, project=self._project, company=self._company, appointment=self._appointment)
        if self._input:
            self.obj.version_count += 1
            manager = self.get_manager(self.obj)
            self.store_to_version(manager, self.obj, self._input)
            self.store_to_self(manager, self.obj, self._input)
        self.set_result(self.obj)
        return