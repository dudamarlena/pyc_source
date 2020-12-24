# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/portlet/staticnav/nav_lib_old.py
# Compiled at: 2009-07-06 06:27:21
from Products.CMFCore.utils import getToolByName

def nav_init(context):
    urltool = getToolByName(context, 'portal_url')
    catalog = getToolByName(context, 'portal_catalog')
    print 'hello'
    return (
     urltool, catalog)