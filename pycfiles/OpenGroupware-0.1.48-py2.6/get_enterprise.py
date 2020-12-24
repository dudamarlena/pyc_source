# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/enterprise/get_enterprise.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.foundation import *
from coils.logic.address import GetCompany

class GetEnterprise(GetCompany):
    __domain__ = 'enterprise'
    __operation__ = 'get'

    def __init__(self):
        GetCompany.__init__(self)

    def run(self, **params):
        db = self._ctx.db_session()
        if len(self.object_ids) == 0:
            self.set_return_value([])
            return
        query = db.query(Enterprise).filter(and_(Enterprise.object_id.in_(self.object_ids), Enterprise.status != 'archived'))
        data = query.all()
        self.log.debug(('Enterprise query by id retrieved {0} entries.').format(len(data)))
        self.set_return_value(data)