# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/security/rbac/core/impl/proxy_assign.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 22, 2013\n\n@package: security - role based access control\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProxy that assignees all the created roles to a role.\n'
from ally.container.impl.proxy import IProxyHandler, Execution
from ally.container.ioc import injected
from security.rbac.api.rbac import IRoleService

@injected
class AssignRoleToRigh(IProxyHandler):
    """
    Implementation for a @see: IProxyHandler that assignees created rights to a role. The proxyed call need to return the right
    id to be assigned to the role.
    """
    roleService = IRoleService
    roleName = str

    def __init__(self):
        """
        Construct the role assign proxy.
        """
        assert isinstance(self.roleService, IRoleService), 'Invalid role service %s' % self.roleService
        assert isinstance(self.roleName, str), 'Invalid role name %s' % self.roleName
        self._roleId = None
        return

    def handle(self, execution):
        """
        @see: IProxyHandler.handle
        """
        assert isinstance(execution, Execution), 'Invalid execution %s' % execution
        if self._roleId is None:
            self._roleId = self.roleService.getByName(self.roleName).Id
        rightId = execution.invoke()
        self.roleService.assignRight(self._roleId, rightId)
        return rightId