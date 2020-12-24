# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\collective\threecolorstheme\permissions.py
# Compiled at: 2008-10-12 05:16:06
from Products.CMFCore.permissions import setDefaultRoles
from Products.Archetypes.public import listTypes
from config import PROJECTNAME
TYPE_ROLES = 'Manager'
permissions = {}

def wireAddPermissions():
    """Creates a list of add permissions for all types in this project
    
    Must be called **after** all types are registered!
    """
    global permissions
    all_types = listTypes(PROJECTNAME)
    for atype in all_types:
        permission = '%s: Add %s' % (PROJECTNAME, atype['portal_type'])
        setDefaultRoles(permission, TYPE_ROLES)
        permissions[atype['portal_type']] = permission

    return permissions