# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/set_access.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from keymap import COILS_ACL_KEYMAP
from get_access import NO_ACL_ENTITIES
from coils.core.logic import RETRIEVAL_MODE_SINGLE, RETRIEVAL_MODE_MULTIPLE

class SetAccess(Command):
    __domain__ = 'object'
    __operation__ = 'set-access'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'object' in params or 'id' in params:
            if 'object' in params:
                self._id = params.get('object').object_id
                self._kind = params.get('object').__entityName__
            else:
                self._id = int(params.get('object').object_id)
                self._kind = None
        else:
            raise CoilsException('No object specified for ACL retrieval')
        self._acls = params.get('acls', [])
        return

    def run(self, **params):
        db = self._ctx.db_session()
        if self._kind is None:
            kind = self._ctx.type_manager.get_type(self._id)
        if self._kind in NO_ACL_ENTITIES:
            self.log.debug(('Cannot create ACLs on entity type {0}').format(kind))
            self._return = False
        else:
            self._acls = [ KVC.translate_dict(x, COILS_ACL_KEYMAP) for x in self._acls ]
            if self._kind == 'Project':
                acls = db.query(ProjectAssignment).filter(ProjectAssignment.parent_id == self._id).all()
                deletes = [ int(o.object_id) for o in acls ]
                for x in self._acls:
                    target_id = x.get('target_id', x.get('targetentityobjectid'))
                    operations = x.get('operations')
                    information = x.get('info', None)
                    for y in acls:
                        if target_id == y.child_id:
                            deletes.remove(y.object_id)
                            y.rights = operations
                            break
                    else:
                        db.add(ProjectAssignment(self._id, target_id, permissions=operations, info=information))

                if deletes:
                    for acl in acls:
                        if acl.object_id in deletes:
                            acl.permissions = None

            else:
                acls = db.query(ACL).filter(ACL.parent_id == self._id).all()
                deletes = [ int(o.object_id) for o in acls ]
                for x in self._acls:
                    target_id = x.get('target_id', x.get('targetentityobjectid'))
                    action = x.get('action', 'allowed')
                    operations = x.get('operations')
                    for y in acls:
                        if target_id == y.context_id and action == y.action:
                            deletes.remove(y.object_id)
                            y.permissions = operations
                            break
                    else:
                        db.add(ACL(self._id, target_id, permissions=operations, action=action))

                if deletes:
                    db.query(ACL).filter(ACL.object_id.in_(deletes)).delete(synchronize_session='fetch')
            self.set_result(True)
        return