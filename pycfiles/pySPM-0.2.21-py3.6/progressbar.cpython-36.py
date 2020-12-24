# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pySPM\utils\progressbar.py
# Compiled at: 2019-05-21 08:54:40
# Size of source mod 2**32: 880 bytes
import sys

class Progressbar:

    def __init__(self, iterator=None, total=None, length=80):
        self.it = iterator
        if total is None:
            if iterator is not None:
                try:
                    self.total = len(iterator)
                except Exception as e:
                    self.total = None

        self.length = length

    def __iter__(self):
        self.elapsed = 0
        self.update()
        for x in self.it:
            yield x
            self.elapsed += 1
            self.update()

    def __repr__(self):
        if self.total is not None:
            p = int(self.length * self.elapsed / self.total)
            tot = self.total
        else:
            p = 0
            tot = '???'
        return '|' + '=' * p + ' ' * (self.length - p) + '| ({}/{})'.format(self.elapsed, tot)

    def update(self):
        sys.stderr.write(self.__repr__() + '\r')