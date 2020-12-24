# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/delete_message.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from utility import filename_for_message_text

class DeleteMessage(Command):
    __domain__ = 'message'
    __operation__ = 'delete'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'uuid' in params:
            self.id_type = 'uuid'
            self.uuid = params['uuid']
        elif 'label' in params and ('process' in params or 'pid' in params):
            self.id_type = 'label'
            self.label = params['label']
            if 'process' in params:
                self.pid = params['process'].object_id
            else:
                self.pid = int(params['pid'])
        else:
            raise CoilsException('message::get parameters do not identify a message.')

    def run(self):
        db = self._ctx.db_session()
        if self.id_type == 'uuid':
            query = db.query(Message).filter(Message.uuid == self.uuid)
        else:
            query = db.query(Message).filter(and_(Message.label == self.label, Message.process_id == self.pid))
        data = self._ctx.access_manager.filter_by_access('r', query.all())
        for message in data:
            uuid = message.uuid
            self._ctx.db_session().delete(message)
            BLOBManager.Delete(filename_for_message_text(uuid))