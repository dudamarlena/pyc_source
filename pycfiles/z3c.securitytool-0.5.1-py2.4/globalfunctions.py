# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/securitytool/globalfunctions.py
# Compiled at: 2010-10-22 19:01:08
from zope.app import zapi
from zope.publisher.interfaces import IRequest
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.component import adapts, getGlobalSiteManager
from zope.publisher.browser import TestRequest, applySkin
from zope.securitypolicy.interfaces import IPrincipalPermissionMap
from zope.securitypolicy.interfaces import IPrincipalRoleMap
from zope.securitypolicy.interfaces import IRolePermissionMap
from zope.securitypolicy.principalpermission import principalPermissionManager
from zope.securitypolicy.principalrole import principalRoleManager
from zope.securitypolicy.rolepermission import rolePermissionManager

def getViews(iface, reqType=IRequest):
    """Get all view registrations for a particular interface."""
    gsm = getGlobalSiteManager()
    for reg in gsm.registeredAdapters():
        if len(reg.required) == 2:
            if reg.required[1] is not None and reqType.isOrExtends(reg.required[1]) and (reg.required[0] is None or iface.isOrExtends(reg.required[0])):
                yield reg

    return


def hasPermissionSetting(settings):
    """Check recursively if a security mapping contains any permission
    setting.
    """
    if settings['permissions'] or settings['roles']:
        return True
    for setting in settings['groups'].values():
        if hasPermissionSetting(setting):
            return True

    return False


def principalDirectlyProvidesPermission(prinPermMap, principal_id, permission_id):
    """Return directly provided permission setting for a given principal and
    permission.
    """
    for prinPerm in prinPermMap:
        if prinPerm['principal'] == principal_id and prinPerm['permission'] == permission_id:
            return prinPerm['setting'].getName()


def roleProvidesPermission(rolePermMap, role_id, permission_id):
    """Return the permission setting for a given role and permission."""
    for rolePerm in rolePermMap:
        if rolePerm['role'] == role_id and rolePerm['permission'] == permission_id:
            return rolePerm['setting'].getName()


def principalRoleProvidesPermission(prinRoleMap, rolePermMap, principal_id, permission_id, role=None):
    """Return the role id and permission setting for a given principal and
    permission.
    """
    if role:
        for prinRole in prinRoleMap:
            if prinRole['principal'] == principal_id and prinRole['setting'].getName() == 'Allow' and role == prinRole['role']:
                role_id = prinRole['role']
                return (role_id,
                 roleProvidesPermission(rolePermMap, role_id, permission_id))

    for prinRole in prinRoleMap:
        if prinRole['principal'] == principal_id and prinRole['setting'].getName() == 'Allow':
            role_id = prinRole['role']
            return (role_id,
             roleProvidesPermission(rolePermMap, role_id, permission_id))

    return (None, None)


def renderedName(name):
    """The root folder is the only unlocated context object."""
    if name is None:
        return 'Root Folder'
    return name


def settingsForObject(ob):
    """Analysis tool to show all of the grants to a process
       This method was copied from zopepolicy.py in the zope.
       security policy package.  Also needed to add a parentList
       this just helps locate the object when we display it to the
       user.
    """
    result = []
    while ob is not None:
        data = {}
        principalPermissions = IPrincipalPermissionMap(ob, None)
        if principalPermissions is not None:
            settings = principalPermissions.getPrincipalsAndPermissions()
            data['principalPermissions'] = [ {'principal': pr, 'permission': p, 'setting': s} for (p, pr, s) in settings ]
        principalRoles = IPrincipalRoleMap(ob, None)
        if principalRoles is not None:
            settings = principalRoles.getPrincipalsAndRoles()
            data['principalRoles'] = [ {'principal': p, 'role': r, 'setting': s} for (r, p, s) in settings ]
        rolePermissions = IRolePermissionMap(ob, None)
        if rolePermissions is not None:
            settings = rolePermissions.getRolesAndPermissions()
            data['rolePermissions'] = [ {'permission': p, 'role': r, 'setting': s} for (p, r, s) in settings ]
        parent = getattr(ob, '__parent__', None)
        while parent is not None:
            if not data.has_key('parentList'):
                data['parentList'] = []
                thisName = getattr(ob, '__name__') or 'Root Folder'
                data['parentList'].append(thisName)
            if parent:
                name = getattr(parent, '__name__') or 'Root Folder'
                data['parentList'].append(name)
            parent = getattr(parent, '__parent__', None)

        result.append((getattr(ob, '__name__', '(no name)'), data))
        ob = getattr(ob, '__parent__', None)
        if data.has_key('parentList'):
            data['uid'] = data['parentList'][0] + '_' + str(len(data['parentList']))

    result[(-1)][1]['parentList'] = [
     'Root Folder']
    result[(-1)][1]['uid'] = 'Root Folder'
    result[(-1)][1]['name'] = 'Root Folder'
    data = {}
    result.append(('global settings', data))
    settings = principalPermissionManager.getPrincipalsAndPermissions()
    settings.sort()
    data['principalPermissions'] = [ {'principal': pr, 'permission': p, 'setting': s} for (p, pr, s) in settings ]
    settings = principalRoleManager.getPrincipalsAndRoles()
    data['principalRoles'] = [ {'principal': p, 'role': r, 'setting': s} for (r, p, s) in settings ]
    settings = rolePermissionManager.getRolesAndPermissions()
    data['rolePermissions'] = [ {'permission': p, 'role': r, 'setting': s} for (p, r, s) in settings ]
    data['parentList'] = [
     'global settings']
    data['uid'] = 'global settings'
    return result


def getSettingsForMatrix(viewInstance):
    """ Here we aggregate all the principal permissions into one object
        We need them all for our lookups to work properly in
        principalRoleProvidesPermission.
    """
    allSettings = {}
    permSetting = ()
    settingList = [ val for (name, val) in settingsForObject(viewInstance) ]
    for setting in settingList:
        for (key, val) in setting.items():
            if not allSettings.has_key(key):
                allSettings[key] = []
            allSettings[key].extend(val)

    settings = settingsForObject(viewInstance)
    settings.reverse()
    return (
     allSettings, settings)


def getView(context, view_reg, skin=IBrowserRequest):
    """Instantiate view from given registration and skin.
       Return `None` if the view isn't callable.
    """
    request = TestRequest()
    applySkin(request, skin)
    try:
        view_inst = view_reg.factory(context, request)
        if callable(view_inst):
            return view_inst
    except TypeError:
        pass


def mergePermissionsFromGroups(principals, matrix):
    """
    This method recursively looks through all the principals in the
    viewPermMatrix and inspects the inherited permissions from groups
    assigned to the  principal.
    """
    sysPrincipals = zapi.principals()
    for principal in principals:
        for group_id in principal.groups:
            group = sysPrincipals.getPrincipal(group_id)
            mergePermissionsFromGroups([ sysPrincipals.getPrincipal(x) for x in principal.groups ], matrix)
            if matrix.has_key(group_id):
                res = matrix[group_id]
                for item in res:
                    if item not in matrix[principal.id] or res[item] == 'Allow':
                        matrix[principal.id][item] = res[item]