# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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