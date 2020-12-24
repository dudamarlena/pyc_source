# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_vendor/progress/spinner.py
# Compiled at: 2019-09-10 15:18:29
from __future__ import unicode_literals
from . import Infinite
from .helpers import WriteMixin

class Spinner(WriteMixin, Infinite):
    message = b''
    phases = ('-', '\\', '|', '/')
    hide_cursor = True

    def update(self):
        i = self.index % len(self.phases)
        self.write(self.phases[i])


class PieSpinner(Spinner):
    phases = [
     b'◷', b'◶', b'◵', b'◴']


class MoonSpinner(Spinner):
    phases = [
     b'◑', b'◒', b'◐', b'◓']


class LineSpinner(Spinner):
    phases = [
     b'⎺', b'⎻', b'⎼', b'⎽', b'⎼', b'⎻']


class PixelSpinner(Spinner):
    phases = [
     b'⣾', b'⣷', b'⣯', b'⣟', b'⡿', b'⢿', b'⣻', b'⣽']