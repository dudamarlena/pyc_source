# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pn36swhz/pip/pip/_vendor/progress/bar.py
# Compiled at: 2020-02-14 17:24:54
# Size of source mod 2**32: 2854 bytes
from __future__ import unicode_literals
import sys
from . import Progress

class Bar(Progress):
    width = 32
    suffix = '%(index)d/%(max)d'
    bar_prefix = ' |'
    bar_suffix = '| '
    empty_fill = ' '
    fill = '#'

    def update(self):
        filled_length = int(self.width * self.progress)
        empty_length = self.width - filled_length
        message = self.message % self
        bar = self.fill * filled_length
        empty = self.empty_fill * empty_length
        suffix = self.suffix % self
        line = ''.join([message, self.bar_prefix, bar, empty, self.bar_suffix,
         suffix])
        self.writeln(line)


class ChargingBar(Bar):
    suffix = '%(percent)d%%'
    bar_prefix = ' '
    bar_suffix = ' '
    empty_fill = '∙'
    fill = '█'


class FillingSquaresBar(ChargingBar):
    empty_fill = '▢'
    fill = '▣'


class FillingCirclesBar(ChargingBar):
    empty_fill = '◯'
    fill = '◉'


class IncrementalBar(Bar):
    if sys.platform.startswith('win'):
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
        current = self.phases[phase] if phase > 0 else ''
        empty = self.empty_fill * max(0, nempty - len(current))
        suffix = self.suffix % self
        line = ''.join([message, self.bar_prefix, bar, current, empty,
         self.bar_suffix, suffix])
        self.writeln(line)


class PixelBar(IncrementalBar):
    phases = ('⡀', '⡄', '⡆', '⡇', '⣇', '⣧', '⣷', '⣿')


class ShadyBar(IncrementalBar):
    phases = (' ', '░', '▒', '▓', '█')