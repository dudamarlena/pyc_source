# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/team/delete_team.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from sqlalchemy.orm import *
from coils.core import *
from coils.core.logic import DeleteCommand

class DeleteTeam(DeleteCommand):
    __domain__ = 'team'
    __operation__ = 'delete'

    def delete_membership(self):
        members = self.obj.members
        for assignment in members:
            self.delete_object_info(assignment)
            self._ctx.db_session().delete(assignment)

    def run(self):
        if self._ctx.is_admin:
            self.delete_membership()
            DeleteCommand.run(self)
        else:
            raise CoilsException('Team deletion requires administrative privileges')