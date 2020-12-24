# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/get_attachment.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand
from command import AttachmentCommand

class GetAttachment(GetCommand, AttachmentCommand):
    __domain__ = 'attachment'
    __operation__ = 'get'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.uuid = params.get('uuid', None)
        if self.uuid is None:
            raise CoilsException('attachment::get parameters do not identify an attachment.')
        return

    def run(self):
        db = self._ctx.db_session()
        query = db.query(Attachment).filter(Attachment.uuid == self.uuid)
        self.set_single_result_mode()
        self.set_return_value(query.all())