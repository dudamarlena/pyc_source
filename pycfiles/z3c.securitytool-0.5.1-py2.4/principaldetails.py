# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/securitytool/principaldetails.py
# Compiled at: 2010-10-22 19:01:08
from zope.app import zapi
from zope.app.apidoc.presentation import getViewInfoDictionary
from zope.interface import Interface, implements, providedBy
from zope.publisher.browser import TestRequest, applySkin
from zope.component import adapts
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.securitypolicy.interfaces import Allow, Unset, Deny
from z3c.securitytool.globalfunctions import *
from z3c.securitytool.matrixdetails import MatrixDetails
from z3c.securitytool import interfaces

class PrincipalDetails(MatrixDetails):
    __module__ = __name__
    implements(interfaces.IPrincipalDetails)
    adapts(Interface)

    def __call__(self, principal_id, skin=IBrowserRequest):
        """Return all security settings (permissions, groups, roles)
           for all interfaces provided by this context for a
           `principal_id`, and of course we are only after browser views"""
        request = TestRequest()
        applySkin(request, skin)
        pMatrix = {'permissions': [], 'permissionTree': [], 'roles': {}, 'roleTree': [], 'groups': {}}
        ifaces = tuple(providedBy(self.context))
        for iface in ifaces:
            for view_reg in getViews(iface, IBrowserRequest):
                view = getView(self.context, view_reg, skin)
                if not view:
                    continue
                all_settings = [ {name: val} for (name, val) in settingsForObject(view) ]
                (self.roleSettings, junk) = getSettingsForMatrix(view)
                self.updatePrincipalMatrix(pMatrix, principal_id, all_settings)

        principals = zapi.principals()
        principal = principals.getPrincipal(principal_id)
        if principal.groups:
            for group_id in principal.groups:
                gMatrix = {group_id: self(group_id)}
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
        updates the MatrixRoles for the PrincipalDetails class
        """
        for curRole in item.get('principalRoles', ()):
            if curRole['principal'] != principal_id:
                continue
            role = curRole['role']
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