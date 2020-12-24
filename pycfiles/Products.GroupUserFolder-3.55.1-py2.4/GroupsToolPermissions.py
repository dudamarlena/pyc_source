# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/GroupsToolPermissions.py
# Compiled at: 2008-05-20 04:51:58
"""
Basic usergroup tool.
"""
__version__ = '$Revision:  $'
__docformat__ = 'restructuredtext'
try:
    from Products.CMFCore.permissions import *
except ImportError:
    from Products.CMFCore.CMFCorePermissions import *

AddGroups = 'Add Groups'
setDefaultRoles(AddGroups, ('Manager', ))
ManageGroups = 'Manage Groups'
setDefaultRoles(ManageGroups, ('Manager', ))
ViewGroups = 'View Groups'
setDefaultRoles(ViewGroups, ('Manager', 'Owner', 'Member'))
DeleteGroups = 'Delete Groups'
setDefaultRoles(DeleteGroups, ('Manager', ))
SetGroupOwnership = 'Set Group Ownership'
setDefaultRoles(SetGroupOwnership, ('Manager', 'Owner'))