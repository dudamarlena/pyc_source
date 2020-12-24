# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/permissions.py
# Compiled at: 2008-09-11 19:48:09
from Products.CMFCore.permissions import setDefaultRoles
ManageContentRelations = 'Relations: Manage content relations'
setDefaultRoles(ManageContentRelations, ('Manager', 'Owner'))