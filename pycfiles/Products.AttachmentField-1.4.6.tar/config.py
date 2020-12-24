# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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