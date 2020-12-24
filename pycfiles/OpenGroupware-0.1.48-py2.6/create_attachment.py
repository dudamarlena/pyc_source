# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/create_attachment.py
# Compiled at: 2012-10-12 07:02:39
import shutil
from sqlalchemy import *
from coils.core import *
from keymap import COILS_ATTACHMENT_KEYMAP
from command import AttachmentCommand

class CreateAttachment(Command, AttachmentCommand):
    __domain__ = 'attachment'
    __operation__ = 'new'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.values = {}
        self.values['mimetype'] = params.get('mimetype', 'application/octet-stream')
        self.values['context_id'] = params.get('context_id', self._ctx.account_id)
        if 'entity' in params:
            self.values['related_id'] = params.get('entity').object_id
        else:
            self.values['related_id'] = params.get('related_id', None)
        self.values['kind'] = params.get('kind', None)
        self.values['expiration'] = params.get('expiration', None)
        self.values['webdav_uid'] = params.get('name', None)
        if 'data' in params:
            self.in_ = None
            self.data_ = params['data']
        elif 'filename' in params:
            self.in_ = open(params['filename'], 'rb')
        elif 'handle' in params:
            self.in_ = params['handle']
        else:
            raise CoilsException('No attachment data or source specified')
        return

    def run(self):
        db = self._ctx.db_session()
        attachment = Attachment()
        attachment.take_values(self.values, COILS_ATTACHMENT_KEYMAP)
        attachment.created = self._ctx.get_utctime()
        attachment.uuid = self.generate_attachment_id()
        try:
            close_input = False
            out_ = BLOBManager.Open(self.attachment_text_path(attachment), 'w', encoding='binary', create=True)
            if not self.in_:
                self.in_ = BLOBManager.ScratchFile()
                close_input = True
                if self.data_:
                    self.in_.write(self.data_)
            self.in_.seek(0)
            (attachment.checksum, attachment.size) = self.write(self.in_, out_)
            BLOBManager.Close(out_)
            if close_input:
                BLOBManager.Close(self.in_)
        except Exception, e:
            self.log.exception(e)
            raise CoilsException('Failure to allocate attachment contents')

        self._ctx.db_session().add(attachment)
        self._result = attachment