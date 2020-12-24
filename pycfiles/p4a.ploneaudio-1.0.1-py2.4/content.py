# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/ploneaudio/content.py
# Compiled at: 2007-11-27 08:53:02
from zope import interface
from p4a.audio import interfaces
from OFS.SimpleItem import SimpleItem

class AudioSupport(SimpleItem):
    """Simple persistent class that implements IAudioSupport.

      >>> support = AudioSupport('foo')
      >>> support.support_enabled
      True

    """
    __module__ = __name__
    interface.implements(interfaces.IAudioSupport)

    @property
    def support_enabled(self):
        return True