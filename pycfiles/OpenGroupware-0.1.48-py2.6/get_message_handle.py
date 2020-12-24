# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/get_message_handle.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand
from utility import filename_for_message_text

class GetMessageHandle(Command):
    __domain__ = 'message'
    __operation__ = 'get-handle'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        message = params.get('object', params.get('message', None))
        if message:
            self.uuid = message.uuid
        else:
            self.uuid = params.get('uuid', None)
        return

    def run(self):
        self._result = None
        if self.uuid:
            message_file_path = ('{0}/wf/m/{1}').format(Backend.store_root(), str(self.uuid))
            handle = BLOBManager.Open(filename_for_message_text(self.uuid), 'rb', encoding='binary')
            self.log.debug(('Opened file {0} for reading.').format(message_file_path))
            self._result = handle
        else:
            raise CoilsException('No message or UUID provided to message::get-handle')
        return