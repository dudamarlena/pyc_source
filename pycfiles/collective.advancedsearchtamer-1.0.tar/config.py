# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/ads/config.py
# Compiled at: 2009-01-02 03:03:18
from Products.CMFCore.permissions import setDefaultRoles
PROJECTNAME = 'collective.ads'
TOOL_TITLE = 'AdsAdmin'
try:
    from Products.CMFPlone.migrations import v2_1
except ImportError:
    HAS_PLONE21 = False
else:
    HAS_PLONE21 = True

DEFAULT_ADD_CONTENT_PERMISSION = 'Add portal content'
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
product_globals = globals()
DEPENDENCIES = []
PRODUCT_DEPENDENCIES = []
STYLESHEETS = []
JAVASCRIPTS = []
try:
    from collective.ads.AppConfig import *
except ImportError:
    pass