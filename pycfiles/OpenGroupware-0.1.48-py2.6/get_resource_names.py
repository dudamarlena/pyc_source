# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/schedular/get_resource_names.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.foundation import *
from coils.core import *
from coils.core.logic import GetCommand

class GetResourceNames(GetCommand):
    __domain__ = 'resource'
    __operation__ = 'get-names'
    mode = None

    def __init__(self):
        GetCommand.__init__(self)

    def run(self):
        db = self._ctx.db_session()
        if len(self.object_ids):
            query = db.query(Resource).filter(and_(Resource.object_id.in_(self.object_ids), Resource.status != 'archived'))
        else:
            query = db.query(Resource).filter(Resource.status != 'archived')
        if self.access_check:
            data = self._ctx.access_manager.filter_by_access('r', query.all())
        else:
            data = query.all()
        self._result = []
        if len(data) > 0:
            for r in data:
                self._result.append(r.name)