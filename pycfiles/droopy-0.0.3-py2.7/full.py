# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\droopy\full.py
# Compiled at: 2011-10-20 12:08:01
from droopy import Droopy
from droopy.static import Static
from droopy.filters import TextFilter
from droopy.lang.polish import Polish
from droopy.lang.english import English
from droopy.readability import Readability

class FullDroopy(Droopy):

    def __init__(self, text):
        Droopy.__init__(self, text)
        self.add_processors(Static())
        self.add_processors(TextFilter())
        self.add_processors(Readability())


class FullPolishDroopy(FullDroopy):

    def __init__(self, text):
        FullDroopy.__init__(self, text)
        self.add_processors(Polish())


class FullEnglishDroopy(FullDroopy):

    def __init__(self, text):
        FullDroopy.__init__(self, text)
        self.add_processors(English())