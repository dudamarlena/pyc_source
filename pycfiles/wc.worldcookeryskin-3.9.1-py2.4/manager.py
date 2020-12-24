# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wc/worldcookeryskin/manager.py
# Compiled at: 2007-02-23 15:51:20
from zope.viewlet.manager import ViewletManagerBase

class SortingViewletManager(ViewletManagerBase):
    __module__ = __name__

    def sort(self, viewlets):
        return sorted(viewlets)