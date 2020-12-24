# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/castle/browser.py
# Compiled at: 2010-08-09 05:35:03
from zope.publisher.browser import BrowserPage
from collective.castle import util

class LoginUrl(BrowserPage):
    __module__ = __name__

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return util.login_URL(self.context)


class Logout(BrowserPage):
    __module__ = __name__

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        util.logout(self.context, self.request)