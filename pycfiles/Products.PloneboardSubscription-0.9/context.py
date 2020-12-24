# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/PloneboardPasteObject/browser/context.py
# Compiled at: 2010-04-08 06:18:05
from plone.memoize.view import memoize
from Acquisition import aq_inner
from plone.app.layout.globals.context import ContextState

class PloneboardContextState(ContextState):
    """Information about the state of the current context
    """
    __module__ = __name__

    @memoize
    def folder(self):
        if self.is_folderish() and not self.is_default_page():
            return aq_inner(self.context)
        else:
            return self.parent()