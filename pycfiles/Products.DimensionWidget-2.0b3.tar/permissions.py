# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/permissions.py
# Compiled at: 2009-04-26 22:17:24
from Products.CMFCore.permissions import setDefaultRoles
from Products.Archetypes.atapi import listTypes
from config import PROJECTNAME
EDIT_NORMATIVA_PERMISSION = 'DigestoContentTypes: Edit Normativa'
EDIT_NORMATIVA_METADATA_PERMISSION = 'DigestoContentTypes: Edit Normativa Metadata'