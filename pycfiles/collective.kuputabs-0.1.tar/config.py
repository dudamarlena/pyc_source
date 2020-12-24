# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/kssinline/config.py
# Compiled at: 2008-10-02 13:12:27
__author__ = 'Hedley Roos <hedley@upfrontsystems.co.za>'
__docformat__ = 'plaintext'
from Products.CMFCore.permissions import setDefaultRoles
PROJECTNAME = 'collective.kssinline'
DEFAULT_ADD_CONTENT_PERMISSION = 'Add portal content'
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
product_globals = globals()
DEPENDENCIES = []
PRODUCT_DEPENDENCIES = []
try:
    from collective.kssinline.AppConfig import *
except ImportError:
    pass