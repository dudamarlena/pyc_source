# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/sitestat/linksfinders/thirdparty/collage.py
# Compiled at: 2008-10-10 10:14:00
"""
Links finder for a Collage content
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.permissions import View as ViewPermission
from Products.Collage.interfaces import ICollage
from Products.ATContentTypes.interface.file import IATFile
from iw.sitestat.interfaces import IFileLinksFinder
from iw.sitestat.linksfinders import ATTypeLinksFinder
from iw.sitestat.utils import getSite

class CollageFileLinksFinder(object):
    __module__ = __name__
    implements(IFileLinksFinder)
    adapts(ICollage)

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
        """We gather URLs from all relevant subcontents"""
        for content in self._findFiles():
            finder = ATTypeLinksFinder(content)
            self.file_urls.extend(finder.fileURLs())
            self.pdf_files_urls.extend(finder.pdfFileURLs())

    def _findFiles(self):
        """Generator over relevant subobjects"""
        atfiles = []
        mtool = getSite().portal_membership
        for row in self.context.objectValues(spec='CollageRow'):
            for column in row.objectValues(spec='CollageColumn'):
                for content in column.objectValues():
                    if not mtool.checkPermission(ViewPermission, content):
                        continue
                    if IATFile.providedBy(content):
                        atfiles.append(content)

        return atfiles