# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/get_message.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class GetMessage(Command):
    __domain__ = 'message'
    __operation__ = 'get'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self._scope = params.get('scope', [])
        if 'uuid' in params:
            self.uuid = params['uuid']
        elif 'label' in params and ('process' in params or 'pid' in params):
            self.uuid = None
            self.label = params['label']
            if 'process' in params:
                self.pid = params['process'].object_id
            else:
                self.pid = int(params['pid'])
        else:
            raise CoilsException('message::get parameters do not identify a message.')
        return

    def run(self):
        db = self._ctx.db_session()
        if self.uuid is not None:
            query = db.query(Message).filter(Message.uuid == self.uuid)
            data = query.all()
        else:
            scopes = self._scope[:]
            scopes.reverse()
            scopes.append(None)
            for scope in scopes:
                self.log.debug(('Search for label {0} in scope {1}').format(self.label, scope))
                query = db.query(Message).filter(and_(Message.label == self.label, Message.process_id == self.pid, Message.scope == scope))
                data = query.all()
                if len(data) > 0:
                    break

            data = self._ctx.access_manager.filter_by_access('r', data)
            if len(data) > 0:
                self._result = data[0]
            else:
                self._result = None
            return