# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/securitytool/matrixdetails.py
# Compiled at: 2010-10-22 19:01:08
from zope.app import zapi
from zope.securitypolicy.interfaces import Allow, Unset, Deny

class MatrixDetails(object):
    """
    This is the super class of PrincipalDetails and PermissionDetails
    """
    __module__ = __name__

    def __init__(self, context):
        """
        init method for the super class
        """
        self.context = context

    def updatePrincipalMatrix(self, pMatrix, principal_id, settings):
        """ this method recursively populates the principal permissions
            dict  (MatrixDetails)
        """
        principals = zapi.principals()
        principal = principals.getPrincipal(principal_id)
        for setting in settings:
            for (name, item) in setting.items():
                self.updateMatrixRoles(pMatrix, principal_id, name, item)
                self.updateMatrixPermissions(pMatrix, principal_id, item)

    def updateMatrixPermissions(self, pMatrix, principal_id, item):
        """ Here we get all the permissions for the given principal
            on the item passed.
        """
        for prinPerms in item.get('principalPermissions', ()):
            if principal_id != prinPerms['principal']:
                continue
            curPerm = prinPerms['permission']
            if getattr(self, 'read_perm', curPerm) != curPerm:
                continue
            if item.get('parentList', None):
                self.updatePermissionTree(pMatrix, item, prinPerms)
            mapping = {'permission': prinPerms['permission'], 'setting': prinPerms['setting']}
            dup = [ perm for perm in pMatrix['permissions'] if perm['permission'] == mapping['permission'] ]
            if dup:
                continue
            pMatrix['permissions'].append(mapping)

        return

    def orderRoleTree(self, pMatrix):
        try:
            roleTree = pMatrix['roleTree']
            globalSettings = roleTree.pop(0)
            roleTree.append(globalSettings)
        except IndexError:
            pass

    def updateRoleTree(self, pMatrix, item, parentList, curRole):
        """
        This method is responsible for poplating the roletree.
        """
        roleTree = pMatrix['roleTree']
        key = item.get('uid')
        keys = [ x.keys()[0] for x in roleTree ]
        if key in keys:
            listIdx = keys.index(key)
        else:
            roleTree.append({key: {}})
            listIdx = -1
        roleTree[listIdx][key]['parentList'] = parentList
        roleTree[listIdx][key]['name'] = item.get('name')
        roleTree[listIdx][key].setdefault('roles', [])
        if curRole not in roleTree[listIdx][key]['roles']:
            roleTree[listIdx][key]['roles'].append(curRole)

    def updateRoles(self, pMatrix, item, role, curRole):
        if curRole['setting'] == Allow:
            roles = pMatrix['roles']
            rolePerms = self.roleSettings['rolePermissions']
            if not roles.has_key(role):
                roles[role] = []
            for rolePerm in rolePerms:
                if rolePerm['role'] == role:
                    mapping = {'permission': rolePerm['permission'], 'setting': rolePerm['setting'].getName()}
                    if mapping not in roles[role]:
                        roles[role].append(mapping)

    def updatePermissionTree(self, pMatrix, item, prinPerms):
        """ method responsible for creating permission tree """
        permissionTree = pMatrix['permissionTree']
        key = item.get('uid')
        keys = [ x.keys()[0] for x in permissionTree ]
        if key in keys:
            listIdx = keys.index(key)
        else:
            permissionTree.append({key: {}})
            listIdx = -1
        permissionTree[listIdx][key]['parentList'] = item.get('parentList')
        permissionTree[listIdx][key]['name'] = item.get('name')
        permissionTree[listIdx][key].setdefault('permissions', [])
        if prinPerms not in permissionTree[listIdx][key]['permissions']:
            permissionTree[listIdx][key]['permissions'].append(prinPerms)