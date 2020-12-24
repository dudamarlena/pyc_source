# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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