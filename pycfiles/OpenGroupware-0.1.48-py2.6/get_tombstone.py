# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/get_tombstone.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *

class GetTombstone(GetCommand):
    __domain__ = 'object'
    __operation__ = 'get-tombstone'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.object_ids = []
        if 'id' in params:
            self.set_single_result_mode()
            self.object_ids.append(int(params['id']))
        elif 'ids' in params:
            self.set_multiple_result_mode()
            self.object_ids.extend([ int(x) for x in params['ids'] ])
        else:
            raise CoilsException('No id or ids specified for object::get-tombstone')

    def run(self):
        self.disable_access_check()
        db = self._ctx.db_session()
        query = db.query(AuditEntry).filter(and_(AuditEntry.context_id.in_(self.object_ids), AuditEntry.action == '99_delete'))
        result = query.all()
        print result
        self.set_return_value(result)