# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/get_attachment_handle.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from command import AttachmentCommand

class GetAttachmentHandle(Command, AttachmentCommand):
    __domain__ = 'attachment'
    __operation__ = 'get-handle'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.attachment = params.get('attachment', None)
        if self.attachment is None:
            if 'uuid' in params:
                self.attachment = self._ctx.run_command('attachment::get', uuid=params.get('uuid'))
        if self.attachment is None:
            raise CoilsException('No attachment or UUID provided to message::get-text')
        return

    def run(self):
        self._result = BLOBManager.Open(self.attachment_text_path(self.attachment), 'rb', encoding='binary')