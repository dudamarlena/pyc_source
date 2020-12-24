# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/getpaid/pagseguro/browser/getpaidthankyou.py
# Compiled at: 2009-04-20 19:03:51
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class GetpaidPagseguroThankyouView(BrowserView):
    """Class for overriding getpaid-thank-you view for pagseguro purchases
    """
    __module__ = __name__

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getInvoice(self):
        if self.request.has_key('Referencia'):
            return self.request['Referencia']
        else:
            return
        return

    def getURL(self):
        portalurl = getToolByName(self.context, 'portal_url').getPortalObject().absolute_url()
        if self.getInvoice() is not None:
            return '%s/@@getpaid-order/%s' % (portalurl, self.getInvoice())
        else:
            return ''
        return