# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/permissions.py
# Compiled at: 2008-09-11 19:48:09
from Products.CMFCore.permissions import setDefaultRoles
ManageContentRelations = 'Relations: Manage content relations'
setDefaultRoles(ManageContentRelations, ('Manager', 'Owner'))