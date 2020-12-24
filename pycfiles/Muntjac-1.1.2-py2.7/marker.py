# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/google_maps/overlay/marker.py
# Compiled at: 2013-04-04 15:36:36


class IMarker(object):
    """@author: Henri Muurimaa
    @author: Richard Lincoln"""

    def getId(self):
        raise NotImplementedError

    def isVisible(self):
        raise NotImplementedError

    def getLatLng(self):
        raise NotImplementedError

    def getIconUrl(self):
        raise NotImplementedError

    def getIconAnchor(self):
        raise NotImplementedError

    def getTitle(self):
        raise NotImplementedError

    def getInfoWindowContent(self):
        raise NotImplementedError

    def isDraggable(self):
        raise NotImplementedError