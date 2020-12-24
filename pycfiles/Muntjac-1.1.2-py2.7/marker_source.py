# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/google_maps/overlay/marker_source.py
# Compiled at: 2013-04-04 15:36:36


class IMarkerSource(object):

    def getMarkers(self):
        raise NotImplementedError

    def addMarker(self, newMarker):
        raise NotImplementedError

    def registerEvents(self, map_):
        raise NotImplementedError

    def getMarkerJSON(self):
        raise NotImplementedError

    def getMarker(self, markerId):
        raise NotImplementedError