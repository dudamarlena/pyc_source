# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/audio/media.py
# Compiled at: 2007-11-27 08:43:15
from zope import component
from zope import interface
from p4a.audio import interfaces
from p4a.common import feature
_marker = object()

class MediaActivator(object):
    """An adapter for seeing the activation status or toggling activation.
    """
    __module__ = __name__
    interface.implements(interfaces.IMediaActivator)
    component.adapts(interface.Interface)

    def __init__(self, context):
        self.context = context

    _audio_activated = feature.FeatureProperty(interfaces.IPossibleAudio, interfaces.IAudioEnhanced, 'context')
    _audio_container_activated = feature.FeatureProperty(interfaces.IPossibleAudioContainer, interfaces.IAudioContainerEnhanced, 'context')

    def media_activated(self, v=_marker):
        if v is _marker:
            if interfaces.IPossibleAudio.providedBy(self.context):
                return self._audio_activated
            elif interfaces.IPossibleAudioContainer.providedBy(self.context):
                return self._audio_container_activated
            return False
        if interfaces.IPossibleAudio.providedBy(self.context):
            self._audio_activated = v
        elif interfaces.IPossibleAudioContainer.providedBy(self.context):
            self._audio_container_activated = v

    media_activated = property(media_activated, media_activated)