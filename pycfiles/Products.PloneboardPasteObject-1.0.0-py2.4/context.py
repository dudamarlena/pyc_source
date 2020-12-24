# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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