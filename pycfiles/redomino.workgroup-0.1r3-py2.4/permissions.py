# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redomino/workgroup/permissions.py
# Compiled at: 2008-06-25 09:09:13
from Products.CMFCore.permissions import setDefaultRoles
MANAGE_WORKGROUP = 'redomino.workgroup: manage Workgroups'
setDefaultRoles(MANAGE_WORKGROUP, ('Manager', ))
ADD_MEMBER_AREA = 'redomino.workgroup: Add member area'
setDefaultRoles(ADD_MEMBER_AREA, ('Manager', 'Owner'))
ADD_PERMISSIONS = {'MemberArea': ADD_MEMBER_AREA}