# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\accessible_output\main_output.py
# Compiled at: 2011-05-28 04:47:20
from accessible_output import braille as b, speech as s

class Output(object):

    def __init__(self, braille=True, speech=True):
        self.braille = braille
        self.speech = speech
        self.braille_output = b.brailler.Brailler()
        self.speech_output = s.speaker.Speaker()

    def output(self, text):
        if self.braille:
            self.braille_output.braille(text)
        if self.speech:
            self.speech_output.say(text, interrupt=True)