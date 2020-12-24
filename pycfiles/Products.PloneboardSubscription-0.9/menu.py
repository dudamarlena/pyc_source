# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/PloneboardPasteObject/browser/menu.py
# Compiled at: 2010-04-08 06:18:05
from plone.memoize.instance import memoize
from plone.app.contentmenu.menu import FactoriesSubMenuItem

class PloneboardFactoriesSubMenuItem(FactoriesSubMenuItem):
    __module__ = __name__

    @memoize
    def _addingToParent(self):
        return True