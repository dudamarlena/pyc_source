# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redturtle/maps/portlet/adapters.py
# Compiled at: 2009-01-06 06:49:26
from Products.ATContentTypes.interface import IATContentType
from Products.Maps.interfaces import IMap, IMarker
from zope.component import adapts
from zope.interface import implements

class BaseItem(object):
    __module__ = __name__
    adapts(IATContentType)
    implements(IMap)

    def __init__(self, context):
        self.context = context

    def getMarkers(self):
        results = []
        marker = IMarker(self.context, None)
        if marker:
            results.append(marker)
        return results