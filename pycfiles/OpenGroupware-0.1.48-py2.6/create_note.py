# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/create_note.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime
from coils.foundation import *
from coils.core import *
from coils.core.logic import CreateCommand, COILS_NOTE_KEYMAP

class CreateNote(CreateCommand):
    __domain__ = 'note'
    __operation__ = 'new'

    def prepare(self, ctx, **params):
        self.keymap = COILS_NOTE_KEYMAP
        self.entity = Note
        CreateCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        CreateCommand.parse_parameters(self, **params)
        if 'text' in params:
            self.values['content'] = params['text']
        if 'title' in params:
            self.values['content'] = params['text']
        self._context = params.get('context', None)
        self._kind = params.get('kind', 'txt')
        return

    def run(self):
        CreateCommand.run(self)
        self.obj.content = self.values.get('content', '')
        if self._context is not None:
            if isinstance(self._context, Appointment):
                self.obj.appointment_id = self._context.object_id
            elif isinstance(self._context, Project):
                self.obj.project_id = self._context.object_id
            elif isinstance(self._context, Contact):
                self.obj.company_id = self._context.object_id
            elif isinstance(self._context, Enterprise):
                self.obj.company_id = self._context.object_id
        self.obj.kind = self._kind
        self.obj.created = datetime.now().replace(tzinfo=UniversalTimeZone())
        self.obj.modified = self.obj.created
        self.obj.creator_id = self._ctx.account_id
        handle = BLOBManager.Create(self.obj.get_path())
        handle.write(self.obj.content)
        self.obj.file_size = handle.tell()
        BLOBManager.Close(handle)
        self.save()
        return