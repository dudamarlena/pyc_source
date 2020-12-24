# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/update_attachment.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *

class UpdateAttachment(Command):
    __domain__ = 'attachment'
    __operation__ = 'set'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'attachment' in params:
            self.attachment = params.get('attachment')
        else:
            raise CoilsException('Update of a message requires a message')
        if 'related' in params:
            self.related_id = params.get('related').object_id
        else:
            self.related_id = params.get('related_id', self.attachment.related_id)
        self.mimetype = params.get('mimetype', self.attachment.mimetype)
        self.webdav_uid = params.get('webdav_uid', self.webdav_uid)

    def run(self):
        self.attachment.webdav_uid = self.webdav_uid
        self.attachment.mimetype = self.mimetype
        self.attachment.related_id = self.related_id
        self._result = self.attachment