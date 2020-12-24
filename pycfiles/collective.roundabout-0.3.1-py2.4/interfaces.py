# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/roundabout/interfaces.py
# Compiled at: 2008-12-14 11:55:57
from zope import schema
from zope.interface import Interface

class IRoundAboutMapHotspot(Interface):
    """RoundAbout Map Hotspot"""
    __module__ = __name__


class IRoundAboutMap(Interface):
    """RoundAbout Map"""
    __module__ = __name__


class IRoundAboutImageHotspot(Interface):
    """RoundAbout Image Hotspot"""
    __module__ = __name__


class IRoundAboutImage(Interface):
    """RoundAbout Image"""
    __module__ = __name__


class IRoundAboutTour(Interface):
    """Container for RoundAbout images and maps."""
    __module__ = __name__