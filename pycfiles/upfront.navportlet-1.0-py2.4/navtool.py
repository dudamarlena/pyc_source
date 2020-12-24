# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/upfront/navportlet/navtool.py
# Compiled at: 2010-10-14 13:06:21
from zope.interface import implements
from Products.CMFPlone.CatalogTool import CatalogTool
from interfaces import INavigationCatalogTool

class NavigationCatalog(CatalogTool):
    """ Catalog used by navigation portlet
    """
    __module__ = __name__
    implements(INavigationCatalogTool)
    id = 'nav_catalog'
    meta_type = 'Navigation Catalog'