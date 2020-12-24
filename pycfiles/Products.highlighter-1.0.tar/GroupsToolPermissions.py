# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/GroupsToolPermissions.py
# Compiled at: 2008-05-20 04:51:58
__doc__ = '\nBasic usergroup tool.\n'
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