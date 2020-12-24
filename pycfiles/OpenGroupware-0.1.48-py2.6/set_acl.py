# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/set_acl.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from get_access import NO_ACL_ENTITIES

class SetACL(Command):
    __domain__ = 'object'
    __operation__ = 'set-acl'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'object' in params or 'id' in params:
            if 'object' in params:
                self._object_id = params.get('object').object_id
                self.obj = params.get('object')
            else:
                self._object_id = int(params.get('id'))
                self.obj = None
        else:
            raise CoilsException('No object specified for ACL creation.')
        self._permissions = params.get('permissions', 'r')
        if self._permissions:
            self._permissions = self._permissions.lower().strip()
        else:
            self._permissions = None
        self._context_id = int(params.get('context_id', self._ctx.account_id))
        self._action = params.get('action', 'allowed').lower().strip()
        return

    def run(self, **params):
        if self.obj:
            kind = self.obj.__entityName__
        else:
            kind = self._ctx.type_manager.get_type(self._object_id)
        db = self._ctx.db_session()
        if kind == 'Project':
            if self._action != 'allowed':
                raise CoilsException('Access revocation not supported on Project entities.')
            acls = db.query(ProjectAssignment).filter(and_(ProjectAssignment.parent_id == self._object_id, ProjectAssignment.child_id == self._context_id)).all()
            if len(acls) == 0:
                db.add(ProjectAssignment(self._object_id, self._context_id, permissions=self._permissions, info=None))
                self.set_result(True)
            elif len(acls) == 1:
                acls[0].rights = self._permissions
                self.set_result(True)
            else:
                raise CoilsException('Inconsistency detected in ProjectAssignment data; multiple results.')
                self.set_result(False)
        elif kind == 'Unknown':
            self.set_result(False)
        else:
            acls = db.query(ACL).filter(and_(ACL.parent_id == self._object_id, ACL.action == self._action, ACL.context_id == self._context_id)).all()
            if acls:
                if len(acls) == 1:
                    if self._permissions:
                        acls[0].permissions = self._permissions
                    else:
                        db.delete(acls[0])
                    self.set_result(True)
                else:
                    raise CoilsException('Inconsistency detected in ACL data; multiple results.')
                    self.set_result(False)
            else:
                if self._permissions:
                    acl = ACL(self._object_id, self._context_id, permissions=self._permissions, action=self._action)
                    db.add(acl)
                self.set_result(True)
        return