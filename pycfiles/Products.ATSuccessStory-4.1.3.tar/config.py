# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/Plone-4.3.7-was-4.2.1/zeocluster/src/Products.ATSuccessStory/Products/ATSuccessStory/config.py
# Compiled at: 2015-12-17 03:21:31
__author__ = 'Franco Pellegrini <frapell@menttes.com>'
__docformat__ = 'plaintext'
from Products.CMFCore.permissions import setDefaultRoles
PROJECTNAME = 'ATSuccessStory'
DEFAULT_ADD_CONTENT_PERMISSION = 'Add portal content'
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
ADD_CONTENT_PERMISSIONS = {'ATSuccessStoryFolder': 'ATSuccessStory: Add ATSuccessStoryFolder', 
   'ATSuccessStory': 'ATSuccessStory: Add ATSuccessStory'}
setDefaultRoles('ATSuccessStory: Add ATSuccessStoryFolder', ('Manager', 'Owner'))
setDefaultRoles('ATSuccessStory: Add ATSuccessStory', ('Manager', 'Owner'))
product_globals = globals()
DEPENDENCIES = []
PRODUCT_DEPENDENCIES = []
try:
    from Products.ATSuccessStory.AppConfig import *
except ImportError:
    pass