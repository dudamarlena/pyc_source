# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/securitytool/interfaces.py
# Compiled at: 2010-10-22 19:01:08
from zope.interface import Interface

class ISecurityChecker(Interface):
    __module__ = __name__

    def getPermissionSettingsForAllViews(self, interfaces, skin, selectedPermission=None):
        """ gets the permission settings for all views"""
        pass

    def aggregateMatrices(self):
        """ aggregates the two matricies together """
        pass

    def getReadPerm(self, view_reg):
        """ gets the read permission for the view """
        pass

    def populateMatrix(self, viewInstance, view_reg):
        """ workhorse of the SecurityChecker class """
        pass

    def updateRolePermissionSetting(self, permSetting, principal, role, name):
        """ updates the permission settings """
        pass

    def populatePermissionMatrix(self, read_perm, principalPermissions):
        """ populates the permission matrix """
        pass


class IPrincipalDetails(Interface):
    __module__ = __name__

    def updateMatrixPermissions(item):
        """ method to update the permissions """
        pass

    def updateMatrixRoles(name, item):
        """ method to up date the matrix roles """
        pass


class IPermissionDetails(Interface):
    __module__ = __name__

    def updateMatrixPermissions(item):
        """ method to update the permissions """
        pass

    def updateMatrixRoles(name, item):
        """ method to up date the matrix roles """
        pass


class IMatrixDetails(Interface):
    __module__ = __name__

    def principalPermissions(principal_id, skin):
        """ main workhorse of the class """
        pass

    def orderRoleTree(self):
        """ This is an ordering method for the roleTree """
        pass

    def updatePrincipalMatrix(settings):
        """ this is called to update the roles and permissions"""
        pass

    def updateRoles(item, role, curRole):
        """ method to update the roles """
        pass

    def updateRoleTree(item, parentList, curRole):
        """ method to update the matrix roletree """
        pass

    def updatePermissionTree(item, prinPerms):
        """ method to update the permission tree """
        pass