# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/PloneboardPasteObject/browser/menu.py
# Compiled at: 2010-04-08 06:18:05
from plone.memoize.instance import memoize
from plone.app.contentmenu.menu import FactoriesSubMenuItem

class PloneboardFactoriesSubMenuItem(FactoriesSubMenuItem):
    __module__ = __name__

    @memoize
    def _addingToParent(self):
        return True