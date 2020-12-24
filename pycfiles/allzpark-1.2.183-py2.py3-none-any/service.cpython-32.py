# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/security_rbac/service.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jan 21, 2013\n\n@package: security RBAC\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nContains the service setups.\n'
from ..security.service import binders
from .populate import NAME_ROOT
from ally.container import support, ioc
from ally.container.bind import intercept
from ally.container.impl.proxy import IProxyHandler
from security.api.right import IRightService
from security.rbac.api.rbac import IRoleService
from security.rbac.core.impl.proxy_assign import AssignRoleToRigh
from ally.support.util import ref

@ioc.entity
def proxyAssignRoleToRigh() -> IProxyHandler:
    b = AssignRoleToRigh()
    b.roleService = support.entityFor(IRoleService)
    b.roleName = NAME_ROOT
    return b


@ioc.before(binders)
def updateBindersForAssignToRole():
    binders().append(intercept(ref(IRightService).insert, handlers=proxyAssignRoleToRigh))