# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\accessible_output\speech\outputs\voiceover.py
# Compiled at: 2011-05-10 06:39:33
from main import OutputError, ScreenreaderSpeechOutput

class VoiceOver(ScreenreaderSpeechOutput):
    """Supports the VoiceOver screenreader on the Mac.

 Note that this will also output as a message to the braille display if VoiceOver is used with braille.
 Calling this module could cause VoiceOver to be started.
 """
    name = 'VoiceOver'

    def __init__(self, *args, **kwargs):
        super(VoiceOver, self).__init__(*args, **kwargs)
        try:
            from appscript import app
            self.app = app('VoiceOver')
        except ImportError:
            raise OutputError

    def speak(self, text, interupt=False):
        self.app.output(text)

    def canSpeak(self):
        return True and super(VoiceOver, self).canSpeak()