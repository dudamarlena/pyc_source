# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/appskin/batch.py
# Compiled at: 2013-09-27 06:12:12
from urllib import urlencode
from ztfy.appskin.layer import IAppLayer
from z3c.table.batch import BatchProvider
from zope.component import adapts
from zope.interface import Interface
from zope.traversing.browser.absoluteurl import absoluteURL

class AppskinBatchProvider(BatchProvider):
    """Custom ZTFY.appskin batch provider"""
    adapts(Interface, IAppLayer, Interface)

    def renderBatchLink(self, batch, cssClass=None):
        args = self.getQueryStringArgs()
        args[self.table.prefix + '-batchStart'] = batch.start
        args[self.table.prefix + '-batchSize'] = batch.size
        query = urlencode(sorted(args.items()))
        tableURL = absoluteURL(self.table, self.request)
        idx = batch.index + 1
        css = ' class="btn %s"' % cssClass
        cssClass = cssClass and css or ''
        return '<a href="%s?%s"%s>%s</a>' % (tableURL, query, cssClass, idx)