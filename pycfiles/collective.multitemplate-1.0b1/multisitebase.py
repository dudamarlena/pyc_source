# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/multisitepanel/browser/multisitebase.py
# Compiled at: 2010-08-24 06:30:58
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from plone.memoize import instance
from zope.security import checkPermission

class MultisiteBase(BrowserView):
    __module__ = __name__

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.messages = IStatusMessage(self.request)

    def back_link(self):
        return dict(label=_('Up to Multisite Panel'), url=self.context.absolute_url())

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    @property
    def zopeRoot(self):
        return self.context.restrictedTraverse('/')

    @property
    @instance.memoize
    def sitesList(self):
        ret = []
        sitesList = self.context.ZopeFind(self.zopeRoot, obj_metatypes=['Plone Site'], search_sub=1)
        for (siteId, siteApp) in sitesList:
            if checkPermission('cmf.ManagePortal', siteApp):
                ret.append((siteId, siteApp))

        return ret