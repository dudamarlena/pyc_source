# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/utils/line_iterator.py
# Compiled at: 2016-04-20 00:05:45


class LineIterator(object):

    def __init__(self, path):
        self._path = path

    def __iter__(self):
        return (line.strip() for line in open(self._path).xreadlines())