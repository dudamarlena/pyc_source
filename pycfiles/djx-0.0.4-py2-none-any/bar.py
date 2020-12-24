# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_vendor/progress/bar.py
# Compiled at: 2019-02-14 00:35:07
from __future__ import unicode_literals
import sys
from . import Progress
from .helpers import WritelnMixin

class Bar(WritelnMixin, Progress):
    width = 32
    message = b''
    suffix = b'%(index)d/%(max)d'
    bar_prefix = b' |'
    bar_suffix = b'| '
    empty_fill = b' '
    fill = b'#'
    hide_cursor = True

    def update(self):
        filled_length = int(self.width * self.progress)
        empty_length = self.width - filled_length
        message = self.message % self
        bar = self.fill * filled_length
        empty = self.empty_fill * empty_length
        suffix = self.suffix % self
        line = (b'').join([message, self.bar_prefix, bar, empty, self.bar_suffix,
         suffix])
        self.writeln(line)


class ChargingBar(Bar):
    suffix = b'%(percent)d%%'
    bar_prefix = b' '
    bar_suffix = b' '
    empty_fill = b'∙'
    fill = b'█'


class FillingSquaresBar(ChargingBar):
    empty_fill = b'▢'
    fill = b'▣'


class FillingCirclesBar(ChargingBar):
    empty_fill = b'◯'
    fill = b'◉'


class IncrementalBar(Bar):
    if sys.platform.startswith(b'win'):
        phases = (' ', '▌', '█')
    else:
        phases = (' ', '▏', '▎', '▍', '▌', '▋', '▊', '▉', '█')

    def update(self):
        nphases = len(self.phases)
        filled_len = self.width * self.progress
        nfull = int(filled_len)
        phase = int((filled_len - nfull) * nphases)
        nempty = self.width - nfull
        message = self.message % self
        bar = self.phases[(-1)] * nfull
        current = self.phases[phase] if phase > 0 else b''
        empty = self.empty_fill * max(0, nempty - len(current))
        suffix = self.suffix % self
        line = (b'').join([message, self.bar_prefix, bar, current, empty,
         self.bar_suffix, suffix])
        self.writeln(line)


class PixelBar(IncrementalBar):
    phases = ('⡀', '⡄', '⡆', '⡇', '⣇', '⣧', '⣷', '⣿')


class ShadyBar(IncrementalBar):
    phases = (' ', '░', '▒', '▓', '█')