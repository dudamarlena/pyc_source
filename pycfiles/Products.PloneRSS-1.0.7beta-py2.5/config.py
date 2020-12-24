# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/PloneRSS/config.py
# Compiled at: 2008-10-21 05:47:03
__author__ = 'unknown <unknown>'
__docformat__ = 'plaintext'
from Products.CMFCore.permissions import setDefaultRoles
PROJECTNAME = 'PloneRSS'
DEFAULT_ADD_CONTENT_PERMISSION = 'Add portal content'
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
ADD_CONTENT_PERMISSIONS = {'rss_manager': 'rss: Add rss_manager', 
   'rss_feed': 'PloneRSS: Add rss_feed', 
   'rss_item': 'rss: Add rss_item', 
   'rss_instance': 'PloneRSS: Add rss_instance', 
   'rss_history': 'rss: Add rss_item'}
setDefaultRoles('rss: Add rss_manager', '("Manager",)')
setDefaultRoles('PloneRSS: Add rss_feed', ('Manager', 'Owner'))
setDefaultRoles('rss: Add rss_item', '("Manager",)')
setDefaultRoles('PloneRSS: Add rss_instance', ('Manager', 'Owner'))
product_globals = globals()
DEPENDENCIES = []
PRODUCT_DEPENDENCIES = []
try:
    from Products.PloneRSS.AppConfig import *
except ImportError:
    pass