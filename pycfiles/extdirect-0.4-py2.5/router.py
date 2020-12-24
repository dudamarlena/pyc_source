# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/extdirect/zope/router.py
# Compiled at: 2009-09-20 13:59:59
from zope.publisher.browser import BrowserView
from extdirect.router import DirectRouter

class ZopeDirectRouter(DirectRouter):

    def __call__(self):
        try:
            body = self.request.bodyStream.getCacheStream().getvalue()
        except AttributeError:
            body = self.request.get('BODY')

        self.request.response.setHeader('Content-Type', 'application/json')
        return super(ZopeDirectRouter, self).__call__(body)