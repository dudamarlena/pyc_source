# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zacharymunro-cape/Documents/har2jmx/har2jmx/harpy/harpy/header.py
# Compiled at: 2012-06-19 11:02:04


class Header(object):

    def __init__(self, j):
        self.raw = j
        self.name = self.raw['name']
        self.value = self.raw['value']
        if 'comment' in self.raw:
            self.comment = self.raw['comment']
        else:
            self.comment = ''