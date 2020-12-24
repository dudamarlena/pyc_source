# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\miniworldmaker\boards\processing_tools.py
# Compiled at: 2019-06-21 05:22:21
# Size of source mod 2**32: 253 bytes


class ProcessingTools:

    def __init__(self):
        self._fill_color = None

    @property
    def fill_color(self):
        return self._fill_color

    @fill_color.setter
    def fill_color(self, value):
        self._fill_color = value