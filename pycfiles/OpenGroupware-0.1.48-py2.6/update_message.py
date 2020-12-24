# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/update_message.py
# Compiled at: 2012-10-12 07:02:39
import os, shutil
from coils.core import *
from shutil import copyfileobj
from utility import filename_for_message_text

class UpdateMessage(Command):
    __domain__ = 'message'
    __operation__ = 'set'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'object' in params:
            self.obj = params.get('object')
        else:
            raise CoilsException('Update of a message requires a message')
        if 'data' in params:
            self.source = 'data'
            self.data = params['data']
        elif 'filename' in params:
            self.source = 'handle'
            self.handle = os.open(params['filename'], 'rb')
        elif 'handle' in params:
            self.source = 'handle'
            self.handle = params['handle']
        else:
            raise CoilsException('No message data or source specified')
        self._mimetype = params.get('mimetype', self.obj.mimetype)
        self._label = params.get('label', self.obj.label)

    def run(self):
        self.obj.label = self._label
        self.obj.mimetype = self._mimetype
        self.obj.version = self.obj.version + 1
        self.obj.status = 'updated'
        self.obj.modified = self._ctx.get_utctime()
        try:
            text = BLOBManager.Create(filename_for_message_text(self.obj.uuid), encoding='binary')
            if self.source == 'data':
                text.write(self.data)
            if self.source == 'handle':
                self.handle.seek(0)
                shutil.copyfileobj(self.handle, text)
            BLOBManager.Close(text)
        except Exception, e:
            self.log.exception(e)
            raise CoilsException('Failure to allocate message contents')

        self.obj.size = BLOBManager.SizeOf(filename_for_message_text(self.obj.uuid))
        self._result = self.obj