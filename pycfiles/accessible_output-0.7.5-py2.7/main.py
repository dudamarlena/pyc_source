# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\accessible_output\speech\outputs\main.py
# Compiled at: 2010-10-23 22:06:20
from accessible_output.output import OutputError, AccessibleOutput
from accessible_output import priority

class SpeechOutput(AccessibleOutput):
    """Parent speech output class"""

    def __init__(self, *args, **kwargs):
        super(SpeechOutput, self).__init__(*args, **kwargs)

    def canSpeak(self):
        return True

    def output(self, *args, **kwargs):
        self.speak(*args, **kwargs)

    def silence(self):
        self.speak('', True)


class ScreenreaderSpeechOutput(SpeechOutput):

    def __init__(self, *args, **kwargs):
        if 'priority' not in kwargs:
            kwargs['priority'] = priority.screenreader
        super(ScreenreaderSpeechOutput, self).__init__(*args, **kwargs)