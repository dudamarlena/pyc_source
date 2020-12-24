# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/sitestat/linksfinders/thirdparty/simplealias.py
# Compiled at: 2008-10-10 10:14:00
"""
Links finder for a SimpleAlias content
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
from zope.interface import implements
from zope.component import adapts, queryAdapter
from iw.sitestat.interfaces import IFileLinksFinder
from Products.SimpleAlias.interfaces import IAlias

class SimpleAliasFileLinksFinder(object):
    __module__ = __name__
    implements(IFileLinksFinder)
    adapts(IAlias)

    def __init__(self, context):
        target = context.getAlias()
        if target:
            self.links_finder = queryAdapter(target, IFileLinksFinder)
        else:
            self.links_finder = None
        return

    def fileURLs(self):
        if self.links_finder:
            return self.links_finder.fileURLs()
        else:
            return []

    def pdfFileURLs(self):
        if self.links_finder:
            return self.links_finder.pdfFileURLs()
        else:
            return []