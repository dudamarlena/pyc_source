# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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