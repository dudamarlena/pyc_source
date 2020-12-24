# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/permissions.py
# Compiled at: 2009-04-26 22:17:24
from Products.CMFCore.permissions import setDefaultRoles
from Products.Archetypes.atapi import listTypes
from config import PROJECTNAME
EDIT_NORMATIVA_PERMISSION = 'DigestoContentTypes: Edit Normativa'
EDIT_NORMATIVA_METADATA_PERMISSION = 'DigestoContentTypes: Edit Normativa Metadata'