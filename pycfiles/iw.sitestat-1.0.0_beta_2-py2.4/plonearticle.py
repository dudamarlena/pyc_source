# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/sitestat/linksfinders/thirdparty/plonearticle.py
# Compiled at: 2008-10-10 10:14:00
"""
Links finder for a PloneArticle content
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
from zope.interface import implements
from zope.component import adapts
from OFS.Image import File as OFSFile
from iw.sitestat.interfaces import IFileLinksFinder
from iw.sitestat.config import PDF_MIMETYPES
from Products.PloneArticle.interfaces import IPloneArticle

class PloneArticleFileLinksFinder(object):
    __module__ = __name__
    implements(IFileLinksFinder)
    adapts(IPloneArticle)

    def __init__(self, context):
        self.context = context
        self.file_urls = []
        self.pdf_file_urls = []
        self._buildLinks()

    def fileURLs(self):
        return self.file_urls

    def pdfFileURLs(self):
        return self.pdf_file_urls

    def _buildLinks(self):
        filesfield = self.context.getField('files')
        proxies = filesfield.get(self.context)
        for proxy in proxies:
            url = proxy.absolute_url()
            ffield = proxy.getPrimaryField()
            accessor = ffield.getAccessor(proxy)
            data = accessor()
            content_type = data.getContentType()
            if content_type in PDF_MIMETYPES:
                self.pdf_file_urls.append(url)
            else:
                self.file_urls.append(url)