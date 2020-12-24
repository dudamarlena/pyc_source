# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/security/rbac/core/impl/rbac_support.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 27, 2013\n\n@package: security - role based access control\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nSQL Alchemy based implementation for the rbac support API.\n'
from ..spec import IRbacSupport
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.support.sqlalchemy.session import SessionSupport
from security.meta.right import RightMapped
from security.meta.right_type import RightTypeMapped
from security.rbac.core.spec import IRbacService

@injected
@setup(IRbacSupport, name='rbacSupport')
class RbacSupportAlchemy(SessionSupport, IRbacSupport):
    """
    Implementation for @see: IRbacSupport
    """
    rbacService = IRbacService
    wire.entity('rbacService')

    def __init__(self):
        assert isinstance(self.rbacService, IRbacService), 'Invalid rbac service %s' % self.rbacService

    def iterateTypeAndRightsNames(self, rbacId):
        """
        @see: IRbacSupport.iterateTypeAndRightsNames
        """
        sql = self.session().query(RightMapped.Name, RightTypeMapped.Name).join(RightTypeMapped)
        sql = self.rbacService.rightsForRbacSQL(rbacId, sql=sql)
        sql = sql.order_by(RightTypeMapped.Name, RightMapped.Name)
        current = names = None
        for name, typeName in sql.all():
            if current != typeName:
                if current is not None:
                    yield (current, names)
                current = typeName
                names = []
            names.append(name)

        if current is not None:
            yield (current, names)
        return