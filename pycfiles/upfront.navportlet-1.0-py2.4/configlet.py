# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/upfront/navportlet/configlet.py
# Compiled at: 2010-10-13 15:04:43
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

class Configlet(BrowserView):
    __module__ = __name__
    label = _('Navigation Portlet')
    status = None

    def __call__(self, *args, **kwargs):
        if self.request.has_key('submit'):
            portal_catalog = getToolByName(self.context, 'portal_catalog')
            nav_catalog = getToolByName(self.context, 'nav_catalog')
            for brain in portal_catalog():
                obj = brain.getObject()
                obj.reindexObject()

            self.status = _('Content reindexed successfully.')
        return self.index()