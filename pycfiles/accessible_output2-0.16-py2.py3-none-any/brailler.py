# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\accessible_output\braille\brailler.py
# Compiled at: 2010-10-23 22:06:19
from accessible_output.output import OutputError
import outputs

class Brailler(object):
    """main brailler class which handles all braille outputs.
  Instantiate this class and call its output method with the text to be brailled"""

    def __init__(self):
        self.outputs = []
        for s in outputs.__all__:
            try:
                self.outputs.append(getattr(outputs, s)())
            except OutputError:
                pass

    def braille(self, text=''):
        """Braille text through the first available brailler that can braille."""
        for s in self.outputs:
            if s.canBraille():
                s.braille(text)
                return

    def clear(self):
        for s in self.outputs:
            if s.canBraille():
                s.clear()
                return

    def output(self, *args, **kwargs):
        self.braille(*args, **kwargs)