# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plonetheme/hamnavoe/browser/splashimage.py
# Compiled at: 2008-09-27 12:33:26
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements
from interfaces import ISplashImage

class SplashImage(ViewletBase):
    __module__ = __name__
    implements(ISplashImage)
    render = ViewPageTemplateFile('splash-image.pt')

    def getSplashImage(self):
        portal = self.portal_state.portal()
        try:
            bannerimg = portal['banner.jpg']
        except:
            bannerimg = ''

        return bannerimg