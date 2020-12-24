# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\droopy\filters.py
# Compiled at: 2011-10-18 15:02:28
from droopy import attr

class TextFilter(object):

    @attr
    def clear_text(self, d):
        return d.text.replace(':)', '.').replace(';)', '.').replace(':(', '.').replace(';(', '.').replace(':P', '.').replace(';P', '.').replace(':D', '.').replace(';D', '.').replace('-', ' ').replace('*', '').replace('–', ' ').replace('”', '').replace('„', '').replace('"', '')