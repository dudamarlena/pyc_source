# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/config.py
# Compiled at: 2009-04-26 22:17:24
__author__ = 'Emanuel Sartor <emanuel@menttes.com>, Santiago Bruno <unknown>'
__docformat__ = 'plaintext'
from Products.CMFCore.permissions import setDefaultRoles
PROJECTNAME = 'DigestoContentTypes'
DEFAULT_ADD_CONTENT_PERMISSION = 'Add portal content'
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))
ADD_CONTENT_PERMISSIONS = {'Attachment': 'DigestoContentTypes: Add Attachment', 'Normativa': 'DigestoContentTypes: Add Normativa', 'Area': 'DigestoContentTypes: Add Area'}
setDefaultRoles('DigestoContentTypes: Add Attachment', ('Manager', 'Owner'))
setDefaultRoles('DigestoContentTypes: Add Normativa', ('Manager', 'Owner'))
setDefaultRoles('DigestoContentTypes: Add Area', ('Manager', 'Owner'))
product_globals = globals()
DEPENDENCIES = []
PRODUCT_DEPENDENCIES = []
PLACEFUL_WORKFLOW_POLICY = 'area_placeful_workflow'
ABBREVIATIONS_KEY = 'DigestoContentTypesAbbreviationsKey'
try:
    from Products.DigestoContentTypes.AppConfig import *
except ImportError:
    pass