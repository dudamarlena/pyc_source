# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/sitestat/linksfinders/standard.py
# Compiled at: 2008-10-10 10:14:00
"""
Link finders for various content types
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
from zope.interface import implements
from zope.component import adapts
from iw.sitestat.interfaces import IFileLinksFinder
from iw.sitestat.config import PDF_MIMETYPES
from Products.Archetypes.interfaces import IBaseObject

class ATTypeLinksFinder(object):
    """Find links for most AT based types"""
    __module__ = __name__
    implements(IFileLinksFinder)
    adapts(IBaseObject)

    def __init__(self, context):
        self.context = context
        self.file_urls = []
        self.pdf_files_urls = []
        self._buildLinks()

    def fileURLs(self):
        return self.file_urls

    def pdfFileURLs(self):
        return self.pdf_files_urls

    def _buildLinks(self):
        context = self.context
        base_url = context.absolute_url()
        file_fields = [ f for f in context.Schema().fields() if f.type == 'file' ]
        for field in file_fields:
            if field.get_size(context) == 0:
                continue
            url = base_url + '/at_download/' + field.getName()
            if field.getContentType(context) in PDF_MIMETYPES:
                self.pdf_files_urls.append(url)
            else:
                self.file_urls.append(url)


from Products.ATContentTypes.interface.file import IATFile

class ATCTFileLinksFinder(object):
    """Find link in the File ATCT standard view"""
    __module__ = __name__
    implements(IFileLinksFinder)
    adapts(IATFile)

    def __init__(self, context):
        self.context = context
        self.file_urls = []
        self.pdf_files_urls = []
        self._buildLinks()

    def fileURLs(self):
        return self.file_urls

    def pdfFileURLs(self):
        return self.pdf_files_urls

    def _buildLinks(self):
        context = self.context
        url = context.absolute_url()
        field = context.Schema().getField('file')
        urls = [url, url + '/at_download/file']
        if field.getContentType(context) in PDF_MIMETYPES:
            self.pdf_files_urls = urls
        else:
            self.file_urls = urls