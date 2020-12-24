# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/langfallback/browser/views.py
# Compiled at: 2008-10-06 10:31:04
"""
"""
from zope.interface import Interface
from zope.interface import implements
from zope.component import getUtility
from Products.Five.browser import BrowserView
from Products.ATContentTypes.content.folder import ATFolder
from icsemantic.core.interfaces import IicSemanticManagementContentTypes, IContentTypesMultilingualPatcher

class MultiLanguages(BrowserView):
    """
    """
    __module__ = __name__

    def __init__(self, context, request):
        """
        """
        self.context = context
        self.request = request
        self.languages = []

    def __call__(self):
        """
        """
        return super(MultiLanguages, self).__call__()


class FixedLanguage(BrowserView):
    """
    """
    __module__ = __name__

    def __init__(self, context, request):
        """
        """
        self.context = context
        self.request = request
        self.languages = []

    def __call__(self):
        """
        """
        pass