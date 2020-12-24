# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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