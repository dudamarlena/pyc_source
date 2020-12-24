# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/pip/pip/_vendor/progress/counter.py
# Compiled at: 2019-07-30 18:46:56
# Size of source mod 2**32: 1372 bytes
from __future__ import unicode_literals
from . import Infinite, Progress

class Counter(Infinite):

    def update(self):
        self.write(str(self.index))


class Countdown(Progress):

    def update(self):
        self.write(str(self.remaining))


class Stack(Progress):
    phases = (' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█')

    def update(self):
        nphases = len(self.phases)
        i = min(nphases - 1, int(self.progress * nphases))
        self.write(self.phases[i])


class Pie(Stack):
    phases = ('○', '◔', '◑', '◕', '●')