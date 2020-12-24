# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/skin/manager.py
# Compiled at: 2006-09-21 05:27:37
from zope.viewlet.manager import ViewletManagerBase

class SortingViewletManager(ViewletManagerBase):
    __module__ = __name__

    def sort(self, viewlets):
        return sorted(viewlets)