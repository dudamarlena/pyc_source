# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/audio/browser/support.py
# Compiled at: 2007-11-27 08:43:07
from zope import component
from zope import interface
from zope import schema
from p4a.audio import interfaces

class IContextualAudioSupport(interfaces.IBasicAudioSupport):
    __module__ = __name__
    can_activate_audio = schema.Bool(title='Can Activate Audio', readonly=True)
    can_deactivate_audio = schema.Bool(title='Can Deactivate Audio', readonly=True)


class Support(object):
    """A view that returns certain information regarding p4acal status.
    """
    __module__ = __name__
    interface.implements(IContextualAudioSupport)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def support_enabled(self):
        """Check to make sure an IAudioSupport utility is available and
        if so, query it to determine if support is enabled.
        """
        support = component.queryUtility(interfaces.IAudioSupport)
        if support is None:
            return False
        return support.support_enabled

    @property
    def _basic_can(self):
        if not self.support_enabled:
            return False
        if not interfaces.IAnyAudioCapable.providedBy(self.context):
            return False
        return True

    @property
    def can_activate_audio(self):
        if not self._basic_can:
            return False
        mediaconfig = component.getMultiAdapter((self.context, self.request), name='media-config.html')
        return not mediaconfig.media_activated

    @property
    def can_deactivate_audio(self):
        if not self._basic_can:
            return False
        mediaconfig = component.getMultiAdapter((self.context, self.request), name='media-config.html')
        return mediaconfig.media_activated