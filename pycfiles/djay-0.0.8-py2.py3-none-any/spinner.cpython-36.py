# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/pip/pip/_vendor/progress/spinner.py
# Compiled at: 2019-07-30 18:46:56
# Size of source mod 2**32: 1380 bytes
from __future__ import unicode_literals
from . import Infinite

class Spinner(Infinite):
    phases = ('-', '\\', '|', '/')
    hide_cursor = True

    def update(self):
        i = self.index % len(self.phases)
        self.write(self.phases[i])


class PieSpinner(Spinner):
    phases = [
     '◷', '◶', '◵', '◴']


class MoonSpinner(Spinner):
    phases = [
     '◑', '◒', '◐', '◓']


class LineSpinner(Spinner):
    phases = [
     '⎺', '⎻', '⎼', '⎽', '⎼', '⎻']


class PixelSpinner(Spinner):
    phases = [
     '⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']