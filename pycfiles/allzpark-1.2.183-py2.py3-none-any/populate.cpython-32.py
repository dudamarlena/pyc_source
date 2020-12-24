# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/security_rbac/populate.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jan 21, 2013\n\n@package: security RBAC\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nContains the setups for populating default data.\n'
from ally.container import support, app, ioc
from ally.internationalization import NC_
from security.rbac.api.rbac import IRoleService, Role, QRole
NAME_ROOT = NC_('security role', 'ROOT')

@ioc.entity
def rootRoleId():
    roleService = support.entityFor(IRoleService)
    assert isinstance(roleService, IRoleService)
    return roleService.getByName(NAME_ROOT).Id


@app.populate(priority=app.PRIORITY_FIRST)
def populateRootRole():
    roleService = support.entityFor(IRoleService)
    assert isinstance(roleService, IRoleService)
    roles = roleService.getAll(limit=1, q=QRole(name=NAME_ROOT))
    if not roles:
        rootRole = Role()
        rootRole.Name = NAME_ROOT
        rootRole.Description = NC_('security role', 'Default role that provides access to all available roles and rights')
        roleService.insert(rootRole)