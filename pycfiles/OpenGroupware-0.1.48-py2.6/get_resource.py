# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/schedular/get_resource.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.foundation import *
from coils.core import *
from coils.core.logic import GetCommand

class GetResource(GetCommand):
    __domain__ = 'resource'
    __operation__ = 'get'
    mode = None

    def __init__(self):
        GetCommand.__init__(self)

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)
        if 'name' in params or 'names' in params:
            self.query_by = 'name'
            if 'name' in params:
                self.mode = 1
                self.names = [params['name']]
            else:
                self.mode = 2
                self.names = params['names']
        elif 'appointment' in params:
            self.mode = 2
            self.query_by = 'appointment'
            self.appointment = params['appointment']
        elif 'email' in params:
            self.query_by = 'email'
            self.mode = 2
            self._email = params['email'].lower()

    def run(self):
        db = self._ctx.db_session()
        query = None
        self.log.debug(('Query mode is {0}').format(self.query_by))
        if self.query_by == 'name':
            if len(self.names):
                query = db.query(Resource).filter(and_(Resource.name.in_(self.names), Resource.status != 'archived'))
            else:
                query = None
        elif self.query_by == 'email':
            query = db.query(Resource).filter(Resource.email.ilike(self._email))
        elif self.query_by == 'appointment':
            if isinstance(self.appointment, Appointment):
                x = self.appointment.get_resource_names()
                if len(x) > 0:
                    query = db.query(Resource).filter(and_(Resource.name.in_(x), Resource.status != 'archived'))
                else:
                    self.set_return_value([])
                    return
            else:
                raise CoilsException('Provided entity is not an Appointment')
        elif self.query_by == 'object_id':
            query = db.query(Resource).filter(and_(Resource.object_id.in_(self.object_ids), Resource.status != 'archived'))
        else:
            self.mode = 2
            query = db.query(Resource).filter(Resource.status != 'archived')
        if query is None:
            self.set_return_value([])
        else:
            self.set_return_value(query.all())
        return