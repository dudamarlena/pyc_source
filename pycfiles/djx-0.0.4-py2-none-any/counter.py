# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_vendor/progress/counter.py
# Compiled at: 2019-02-14 00:35:07
from __future__ import unicode_literals
from . import Infinite, Progress
from .helpers import WriteMixin

class Counter(WriteMixin, Infinite):
    message = b''
    hide_cursor = True

    def update(self):
        self.write(str(self.index))


class Countdown(WriteMixin, Progress):
    hide_cursor = True

    def update(self):
        self.write(str(self.remaining))


class Stack(WriteMixin, Progress):
    phases = (' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█')
    hide_cursor = True

    def update(self):
        nphases = len(self.phases)
        i = min(nphases - 1, int(self.progress * nphases))
        self.write(self.phases[i])


class Pie(Stack):
    phases = ('○', '◔', '◑', '◕', '●')