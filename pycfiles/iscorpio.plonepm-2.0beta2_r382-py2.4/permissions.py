# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/permissions.py
# Compiled at: 2009-09-03 11:41:06
import logging
from AccessControl import ModuleSecurityInfo
from AccessControl import Permissions
try:
    from Products.CMFCore import permissions as CMFCorePermissions
except:
    from Products.CMFCore import CMFCorePermissions

import Products.Archetypes.public as atapi, config
log = logging.getLogger('PlonePM permissions')

def initialize():
    permissions = {}
    types = atapi.listTypes(config.PROJECTNAME)
    for atype in types:
        permission = '%s: Add %s' % (config.PROJECTNAME, atype['portal_type'])
        permissions[atype['portal_type']] = permission
        CMFCorePermissions.setDefaultRoles(permission, ('Manager', 'Owner'))

    return permissions