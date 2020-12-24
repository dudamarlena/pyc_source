# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/upfront/navportlet/portlet.py
# Compiled at: 2010-10-13 15:04:43
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from plone.memoize.instance import memoize
from plone.app.portlets.portlets import navigation as base
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from Products.CMFPlone import PloneMessageFactory as _
from navtree import buildFolderTree

class Renderer(base.Renderer):
    """ Renderer that uses a custom navtree builder
    """
    __module__ = __name__

    @memoize
    def getNavTree(self, _marker=[]):
        context = aq_inner(self.context)
        queryBuilder = getMultiAdapter((context, self.data), INavigationQueryBuilder)
        strategy = getMultiAdapter((context, self.data), INavtreeStrategy)
        return buildFolderTree(context, obj=context, query=queryBuilder(), strategy=strategy)