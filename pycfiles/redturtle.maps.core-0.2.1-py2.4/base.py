# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redturtle/maps/core/browser/base.py
# Compiled at: 2009-04-02 06:28:59
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.ATContentTypes.interface import IATContentType, IATDocument, IATEvent, IATNewsItem, IATFile, IATImage, IATLink

class BaseView(BrowserView):
    __module__ = __name__
    __call__ = ViewPageTemplateFile('base.pt')
    security = ClassSecurityInfo()

    def __init__(self, context, request):
        self.context = context
        self.request = request

    security.declarePublic('getText')

    def getText(self):
        return self.context.getText()


InitializeClass(BaseView)