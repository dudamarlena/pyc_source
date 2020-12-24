# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/yaco/applyfun/browser.py
# Compiled at: 2008-06-16 04:17:34
from Products.Five import BrowserView
from yaco.applyfun.httplogger import HTTPLogger

class HTTPLoggingBrowserView(BrowserView):
    __module__ = __name__

    def __init__(self, context, request):
        super(HTTPLoggingBrowserView, self).__init__(context, request)
        self.logger = HTTPLogger(context=context, REQUEST=request)

    def context():

        def get(self):
            return self._context[0]

        def set(self, context):
            self._context = [context]

        return property(get, set)

    context = context()