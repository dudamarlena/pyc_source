# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\accessible_output\speech\speaker.py
# Compiled at: 2010-10-23 22:06:20
from accessible_output.output import OutputError
import outputs

class Speaker(object):
    """main speaker class which handles all speech outputs.
  Instantiate this class and call its output method with the text to be spoken and an optional boolean argument
  to govern interruption.  Pass in a SpeechOutput class to be used as default output."""

    def __init__(self, speaker=None):
        self.speaker = speaker
        self.outputs = []
        for s in outputs.__all__:
            try:
                self.outputs.append(getattr(outputs, s)())
            except OutputError:
                pass

        self.outputs.sort(key=lambda x: x.priority, reverse=True)

    def say(self, text='', interrupt=0):
        """Speak text through either the provided output or the first available one."""
        outputs = []
        if self.speaker:
            outputs = [
             self.speaker]
        outputs.extend(self.outputs)
        for s in outputs:
            if s.canSpeak():
                s.speak(text, interrupt)
                return

    def silence(self):
        for s in self.outputs:
            if s.canSpeak():
                s.silence()
                return

    def output(self, *args, **kwargs):
        self.say(*args, **kwargs)