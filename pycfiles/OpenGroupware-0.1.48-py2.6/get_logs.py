# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/get_logs.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import RETRIEVAL_MODE_SINGLE, RETRIEVAL_MODE_MULTIPLE
NO_LOG_ENTITIES = [
 'Format']

class GetLogs(Command):
    __domain__ = 'object'
    __operation__ = 'get-logs'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.object_ids = []
        if 'id' in params or 'ids' in params:
            if 'id' in params:
                self.mode = RETRIEVAL_MODE_SINGLE
                self.object_ids.append(int(params['id']))
            elif 'ids' in params:
                self.mode = RETRIEVAL_MODE_MULTIPLE
                for object_id in params['ids']:
                    self.object_ids.append(int(object_id))

        elif 'object' in params or 'objects' in params:
            if 'object' in params:
                self.mode = RETRIEVAL_MODE_SINGLE
                self.object_ids.append(int(params.get('object').object_id))
            elif 'objects' in params:
                self.mode = RETRIEVAL_MODE_MULTIPLE
                for o in params.get('objects'):
                    self.object_ids.append(int(o.object_id))

        else:
            raise CoilsException('No object specified for log retrieval')

    def run(self, **params):
        self.access_check = False
        objects = self._ctx.type_manager.group_ids_by_type(self.object_ids)
        db = self._ctx.db_session()
        array = {}
        for object_id in self.object_ids:
            array[object_id] = []

        for kind in objects:
            if kind not in NO_LOG_ENTITIES:
                print ('getting logs for objects {0}').format(self.object_ids)
                query = db.query(AuditEntry).filter(AuditEntry.context_id.in_(objects[kind])).order_by(AuditEntry.datetime)
                logs = query.all()
                for log in logs:
                    array[log.context_id].append(log)

        if self.mode == RETRIEVAL_MODE_SINGLE:
            self._result = array[self.object_ids[0]]
        else:
            self._result = array