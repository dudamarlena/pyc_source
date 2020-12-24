# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plonetheme/hamnavoe/browser/hmve.py
# Compiled at: 2008-09-27 12:33:26
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements
from interfaces import ISplashImage, IStrapline

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


class Strapline(ViewletBase):
    __module__ = __name__
    implements(IStrapline)
    render = ViewPageTemplateFile('strapline.pt')

    def getStrapline(self):
        portal = self.portal_state.portal()
        try:
            strp = portal['strapline']()
        except:
            try:
                strp = portal.Title()
            except:
                strp = ''

        return strp