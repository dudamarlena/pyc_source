# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/Goban/browser/gamefolder.py
# Compiled at: 2008-05-06 12:38:24
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class GameFolderView(BrowserView):
    """
    """
    __module__ = __name__
    __call__ = ViewPageTemplateFile('gamefolder.pt')

    def batchListing(self):
        """
        """
        return self.context.getFolderContents({'portal_type': 'Go Game'}, batch=True, b_size=20, full_objects=True)