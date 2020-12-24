# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plonetheme/colorcontext/browser/classprovider.py
# Compiled at: 2010-09-15 08:23:40
from Products.Five import BrowserView
from urlparse import urlparse

class CSSClassProvider(BrowserView):

    def getColorClass(self, url):
        parsedURL = urlparse(url)
        path = parsedURL[2]
        result = path.replace('/', ' ')
        return result