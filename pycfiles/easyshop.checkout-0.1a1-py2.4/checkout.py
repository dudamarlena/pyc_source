# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/checkout/browser/checkout.py
# Compiled at: 2008-06-20 09:35:17
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import ICheckoutManagement

class CheckoutView(BrowserView):
    """
    """
    __module__ = __name__

    def checkout(self):
        """The start of the checkout process.
        """
        mtool = getToolByName(self.context, 'portal_membership')
        ICheckoutManagement(self.context).redirectToNextURL('AFTER_START')