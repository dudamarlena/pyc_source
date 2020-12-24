# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/securitytool/securitytool.py
# Compiled at: 2010-10-22 19:01:08
from copy import deepcopy
from pprint import pprint
from zope.app import zapi
from zope.app.apidoc.presentation import getViewInfoDictionary
from zope.i18nmessageid import ZopeMessageFactory as _
from zope.interface import Interface, implements, providedBy
from zope.publisher.browser import TestRequest, applySkin
from zope.publisher.interfaces import IRequest
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.securitypolicy.interfaces import Allow, Unset, Deny
from z3c.securitytool.permissiondetails import *
from z3c.securitytool.principaldetails import *
from z3c.securitytool.globalfunctions import *
from z3c.securitytool import interfaces

class SecurityChecker(object):
    """ Workhorse of the security tool package"""
    __module__ = __name__
    implements(interfaces.ISecurityChecker)
    adapts(Interface)

    def __init__(self, context):
        self.context = context

    def getPermissionSettingsForAllViews(self, interfaces, skin=IBrowserRequest, selectedPermission=None):
        """ retrieves permission settings for all views"""
        request = TestRequest()
        self.selectedPermission = selectedPermission
        applySkin(request, skin)
        self.viewMatrix = {}
        self.viewPermMatrix = {}
        self.viewRoleMatrix = {}
        self.views = {}
        self.permissions = set()
        for iface in interfaces:
            for view_reg in getViews(iface, skin):
                viewInstance = getView(self.context, view_reg, skin)
                if viewInstance:
                    self.populateMatrix(viewInstance, view_reg)

        self.aggregateMatrices()
        return [self.viewMatrix, self.views, self.permissions]

    def aggregateMatrices(self):
        """
        This method is used to aggregate the two matricies together.
        There is a role matrix and a permission matrix. The reason for
        the role matrix is that we can have lower level assignments to
        override higher level assingments seperately from the direct
        assignments of permissions. We need to merge these together to
        have a complete matrix, When there is a conflict between
        permissions and role-permissions  permissions will always win.
        """
        for item in self.viewRoleMatrix:
            if not self.viewMatrix.has_key(item):
                self.viewMatrix[item] = {}
            for viewSetting in self.viewRoleMatrix[item]:
                val = self.viewRoleMatrix[item][viewSetting] and 'Allow' or '--'
                self.viewMatrix[item].update({viewSetting: val})

        for item in self.viewPermMatrix:
            if not self.viewMatrix.has_key(item):
                self.viewMatrix[item] = {}
            for viewSetting in self.viewPermMatrix[item]:
                self.viewMatrix[item].update({viewSetting: self.viewPermMatrix[item][viewSetting]})

        principals = zapi.principals()
        getPrin = principals.getPrincipal
        viewPrins = [ getPrin(prin) for prin in self.viewMatrix ]
        tmpMatrix = deepcopy(self.viewMatrix)
        mergePermissionsFromGroups(viewPrins, tmpMatrix)
        for prinItem in tmpMatrix:
            for item in tmpMatrix[prinItem]:
                if not self.viewMatrix[prinItem].has_key(item):
                    self.viewMatrix[prinItem][item] = tmpMatrix[prinItem][item]

    def getReadPerm(self, view_reg):
        """ Helper method which returns read_perm and view name"""
        info = getViewInfoDictionary(view_reg)
        read_perm = info['read_perm']
        if read_perm == None:
            read_perm = 'zope.Public'
        self.permissions.add(read_perm)
        name = info['name']
        return (
         name, read_perm)

    def populateMatrix(self, viewInstance, view_reg):
        """ populates the matrix used for the securityMatrix view"""
        (self.name, read_perm) = self.getReadPerm(view_reg)
        if self.selectedPermission and self.selectedPermission != read_perm:
            return
        self.views[self.name] = read_perm
        (allSettings, settings) = getSettingsForMatrix(viewInstance)
        rolePermMap = allSettings.get('rolePermissions', ())
        self.populateViewRoleMatrix(rolePermMap, settings, read_perm)
        prinPermissions = allSettings.get('principalPermissions', [])
        self.populatePermissionMatrix(read_perm, prinPermissions)

    def populateViewRoleMatrix(self, rolePermMap, settings, read_perm):
        """
        This method is responsible for populating the viewRoleMatrix
        of the security matrix this will be merged with the permissionMatrix
        after both are fully populated.
        """
        for (name, setting) in settings:
            principalRoles = setting.get('principalRoles', [])
            for role in principalRoles:
                principal = role['principal']
                if not self.viewRoleMatrix.has_key(principal):
                    self.viewRoleMatrix[principal] = {}
                if read_perm == 'zope.Public':
                    permSetting = (
                     role, 'Allow')
                elif role['setting'] == Deny:
                    try:
                        del self.viewRoleMatrix[principal][self.name][role['role']]
                        continue
                    except KeyError:
                        pass

                else:
                    permSetting = principalRoleProvidesPermission(principalRoles, rolePermMap, principal, read_perm, role['role'])
                if permSetting[1]:
                    self.viewRoleMatrix[principal].setdefault(self.name, {})
                    self.viewRoleMatrix[principal][self.name].update({role['role']: permSetting[1]})

    def populatePermissionMatrix(self, read_perm, principalPermissions):
        """ This method populates the principal permission section of
            the view matrix, it is half responsible for the 'Allow' and
            'Deny' on the securityMatrix.html page. The other half belongs
            to the role permissions (viewRoleMatrix).
        """
        matrix = self.viewPermMatrix
        principalPermissions.reverse()
        for prinPerm in principalPermissions:
            if prinPerm['permission'] != read_perm:
                continue
            principal_id = prinPerm['principal']
            setting = prinPerm['setting'].getName()
            if matrix.setdefault(principal_id, {self.name: setting}) == {self.name: setting}:
                continue
            else:
                matrix[principal_id][self.name] = setting