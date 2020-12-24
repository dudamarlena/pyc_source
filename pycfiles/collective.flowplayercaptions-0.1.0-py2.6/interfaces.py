# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/collective/flowplayercaptions/interfaces.py
# Compiled at: 2011-01-02 18:51:59
from zope.interface import Interface

class IFlowplayerCaptionsLayer(Interface):
    """Marker interface for the collective.flowplayercaptions layer"""
    pass


class ICaptionsSource(Interface):
    """Marker interface for sorce that provides captions"""
    pass