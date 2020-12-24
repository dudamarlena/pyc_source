# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/sitestat/interfaces/linksfinder.py
# Compiled at: 2008-10-10 10:13:59
"""
Interfaces for finding file links on content objects.
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
from zope.interface import Interface

class IFileLinksFinder(Interface):
    """Interface for adapters that find URLs for files in the context
    view. Developers that implement me should not worry too much
    providing too many URLs: The ones that don't show in the page are
    ignored."""
    __module__ = __name__

    def fileURLs():
        """Sequence of URLs to files (PDF excluded) published by the
        context object in its view"""
        pass

    def pdfFileURLs():
        """Sequence of URLs to PDF files published by the context
        object in its view"""
        pass