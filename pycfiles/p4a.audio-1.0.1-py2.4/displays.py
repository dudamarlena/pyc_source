# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/audio/browser/displays.py
# Compiled at: 2007-11-27 08:43:07
from zope import interface
from zope import component
from p4a.audio import interfaces
from Products.CMFDynamicViewFTI import interfaces as cmfdynifaces

class AudioContainerDynamicViews(object):
    """A IDynamicallyViewable adapter for audio containers."""
    __module__ = __name__
    interface.implements(cmfdynifaces.IDynamicallyViewable)
    component.adapts(interfaces.IAudioContainerEnhanced)

    def __init__(self, context):
        self.context = context

    def getAvailableViewMethods(self):
        """Get a list of registered view method names"""
        return [ view for (view, name) in self.getAvailableLayouts() ]

    def getDefaultViewMethod(self):
        """Get the default view method name"""
        return 'audio-container.html'

    def getAvailableLayouts(self):
        """Get the layouts registered for this object"""
        return (
         ('audio-container.html', 'Standard audio view'), ('audio-album.html', 'Album view'))