# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/delete_attachment.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from command import AttachmentCommand

class DeleteAttachment(Command, AttachmentCommand):
    __domain__ = 'attachment'
    __operation__ = 'delete'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.uuid = params.get('uuid', None)
        if self.uuid is None:
            raise CoilsException('attachment::delete parameters do not identify an attachment.')
        return

    def run(self):
        db = self._ctx.db_session()
        query = db.query(Attachment).filter(Attachment.uuid == self.uuid)
        attachments = self._ctx.access_manager.filter_by_access('r', query.all())
        if len(attachments) == 1:
            attachment = attachments[0]
            self._ctx.db_session().delete(attachment)
            BLOBManager.Delete(self.attachment_text_path(attachment))