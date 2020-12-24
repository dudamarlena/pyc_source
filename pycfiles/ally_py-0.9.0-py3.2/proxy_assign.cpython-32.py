# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/security/rbac/core/impl/proxy_assign.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Feb 22, 2013

@package: security - role based access control
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Proxy that assignees all the created roles to a role.
"""
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