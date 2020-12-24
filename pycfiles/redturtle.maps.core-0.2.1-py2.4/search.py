# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redturtle/maps/core/browser/search.py
# Compiled at: 2009-04-02 06:28:59
from Products.Maps.browser.map import BaseMapView
from Products.Maps.interfaces.map import IMapView, IMap
from zope.interface import implements

class MapSearch(BaseMapView):
    """
    Search results view class.
    """
    __module__ = __name__
    implements(IMapView)

    @property
    def enabled(self):
        if self.map is None:
            return False
        return True