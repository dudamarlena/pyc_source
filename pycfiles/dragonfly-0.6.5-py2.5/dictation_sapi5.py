# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\engines\dictation_sapi5.py
# Compiled at: 2009-03-30 02:12:07
"""
Dictation container for the SAPI5 engine.

"""
from ..log import get_log
from .dictation_base import DictationContainerBase

class Sapi5DictationContainer(DictationContainerBase):

    def __init__(self, words):
        DictationContainerBase.__init__(self, words=words)

    def format(self):
        """ Format and return this dictation. """
        return (' ').join(self._words)