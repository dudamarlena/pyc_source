# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/securitytool/permissiondetails.py
# Compiled at: 2010-10-22 19:01:08
from zope.app import zapi
from zope.app.apidoc.presentation import getViewInfoDictionary
from zope.interface import Interface, implements, providedBy
from zope.publisher.browser import TestRequest, applySkin
from zope.component import adapts
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.securitypolicy.interfaces import Allow, Unset, Deny
from z3c.securitytool.globalfunctions import *
from z3c.securitytool import interfaces
from z3c.securitytool.matrixdetails import MatrixDetails

class PermissionDetails(MatrixDetails):
    """Get permission details for a given principal and view.
    Includes the permissions set by the groups the principal belongs to.
    """
    __module__ = __name__
    implements(interfaces.IPermissionDetails)
    adapts(Interface)

    def __call__(self, principal_id, view_name, skin=IBrowserRequest):
        self.read_perm = 'zope.Public'
        self.view_name = view_name
        self.skin = skin
        request = TestRequest()
        applySkin(request, skin)
        pMatrix = {'permissions': [], 'permissionTree': [], 'roles': {}, 'roleTree': [], 'groups': {}}
        ifaces = tuple(providedBy(self.context))
        for iface in ifaces:
            for view_reg in getViews(iface, skin):
                if view_reg.name == view_name:
                    view = getView(self.context, view_reg, skin)
                    all_settings = [ {name: val} for (name, val) in settingsForObject(view) ]
                    self.read_perm = getViewInfoDictionary(view_reg)['read_perm'] or 'zope.Public'
                    (self.roleSettings, junk) = getSettingsForMatrix(view)
                    self.rolePermMap = self.roleSettings.get('rolePermissions', ())
                    self.updatePrincipalMatrix(pMatrix, principal_id, all_settings)
                    break

        principals = zapi.principals()
        principal = principals.getPrincipal(principal_id)
        if principal.groups:
            for group_id in principal.groups:
                gMatrix = {group_id: self(group_id, view_name, skin)}
                pMatrix['groups'].update(gMatrix)

            permList = [ x.items()[1][1] for x in pMatrix['permissions'] ]
            for matrix in gMatrix.values():
                for tmp in matrix['permissions']:
                    gPerm = tmp['permission']
                    if gPerm not in permList:
                        pMatrix['permissions'].append(tmp)

        self.orderRoleTree(pMatrix)
        return pMatrix

    def updateMatrixRoles(self, pMatrix, principal_id, name, item):
        """
        Updates the roles for the PermissionDetails class
        """
        for curRole in item.get('principalRoles', ()):
            if curRole['principal'] != principal_id:
                continue
            role = curRole['role']
            perm = roleProvidesPermission(self.rolePermMap, role, self.read_perm)
            if perm != 'Allow' and perm != 'Deny':
                continue
            parentList = item.get('parentList', None)
            if parentList:
                self.updateRoleTree(pMatrix, item, parentList, curRole)
            if curRole['setting'] == Deny:
                try:
                    del pMatrix['roles'][role]
                except:
                    pass

            else:
                self.updateRoles(pMatrix, item, role, curRole)

        return