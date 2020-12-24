# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionZenoss/browser/quickstart.py
# Compiled at: 2011-01-11 16:22:56
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class FudgeQuickstart(BrowserView):
    """
    Creates the initial user and sets the admin password.
    """
    __module__ = __name__

    def noUserSetup(self):
        """
        Handles form submission for setting the admin password and creating
        an initial user.
        """
        self.context.dmd._rq = True
        self.request.RESPONSE.redirect(self.context.absolute_url())