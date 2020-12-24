# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/get_attachments.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand
from command import AttachmentCommand

class GetAttachments(GetCommand, AttachmentCommand):
    __domain__ = 'object'
    __operation__ = 'get-attachments'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.related_id = params.get('object').object_id

    def run(self):
        db = self._ctx.db_session()
        query = db.query(Attachment).filter(Attachment.related_id == self.related_id)
        self.set_multiple_result_mode()
        self.set_return_value(query.all())