# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/team/get_logins.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *

class GetLogins(Command):
    __domain__ = 'team'
    __operation__ = 'get-logins'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'team' in params:
            self.team = params.get('team')
        else:
            raise CoilsException('No team specified')

    def run(self):
        db = self._ctx.db_session()
        query = db.query(Contact.login).filter(Contact.object_id.in_([ x.child_id for x in self.team.members ]))
        data = query.all()
        self._result = []
        for tmp in data:
            self._result.append(tmp[0])