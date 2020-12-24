# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/pdf/browser.py
# Compiled at: 2006-09-21 05:27:38
from zope.traversing.api import getName
from zope.component import getMultiAdapter
from zope.publisher.browser import BrowserPage
from worldcookery.pdf.interfaces import IPDFPresentation

class PDFView(BrowserPage):
    __module__ = __name__

    def __call__(self):
        filename = getName(self.context) + '.pdf'
        response = self.request.response
        response.setHeader('Content-Disposition', 'attachment; filename=%s' % filename)
        response.setHeader('Content-Type', 'application/pdf')
        return getMultiAdapter((self.context, self.request), IPDFPresentation)