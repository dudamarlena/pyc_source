# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/get_message_text.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand
from utility import filename_for_message_text

class GetMessageText(Command):
    __domain__ = 'message'
    __operation__ = 'get-text'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self._scope = params.get('scope', [])
        if 'object' in params:
            self._uuid = params['object'].uuid
        elif 'uuid' in params:
            self._uuid = params.get('uuid', None)
        elif 'label' in params and 'process' in params:
            self._uuid = None
            self._label = params.get('label')
            self._process = params.get('process')
        return

    def run(self):
        if self._uuid is None:
            pid = self._process.object_id
            db = self._ctx.db_session()
            scopes = self._scope[:]
            scopes.reverse()
            scopes.append(None)
            for scope in scopes:
                self.log.debug(('Search for label {0} in scope {0}').format(self._label, scope))
                query = db.query(Message).filter(and_(Message.label == self._label, Message.process_id == pid, Message.scope == scope))
                data = query.all()
                if len(data) > 0:
                    self._uuid = data[0].uuid
                    break

        if self._uuid is None:
            raise CoilsException(('message::get-text found no message for label "{0}"').format(self._label))
        handle = BLOBManager.Open(filename_for_message_text(self._uuid), 'rb')
        self._result = handle.read()
        BLOBManager.Close(handle)
        return