# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/sixel/sixel.py
# Compiled at: 2015-03-24 11:11:16
import sys, os, logging
try:
    from sixel_cimpl import SixelConverter
except ImportError, e:
    logging.exception(e)
    from .converter import SixelConverter

class SixelWriter:

    def __init__(self, f8bit=False, bodyonly=False):
        self.f8bit = f8bit
        self._bodyonly = bodyonly
        if f8bit:
            self.CSI = b'\x9b'
        else:
            self.CSI = '\x1b['

    def save_position(self, output):
        if not self._bodyonly:
            if os.isatty(output.fileno()):
                output.write('\x1b7')

    def restore_position(self, output):
        if not self._bodyonly:
            if os.isatty(output.fileno()):
                output.write('\x1b8')

    def move_x(self, n, fabsolute, output):
        if not self._bodyonly:
            output.write(self.CSI)
            if fabsolute:
                output.write('%d`' % n)
            elif n > 0:
                output.write('%dC' % n)
            elif n < 0:
                output.write('%dD' % -n)

    def move_y(self, n, fabsolute, output):
        if not self._bodyonly:
            output.write(self.CSI)
            if fabsolute:
                output.write('%dd' % n)
            elif n > 0:
                output.write('%dB' % n)
            elif n < 0:
                output.write('%dA' % n)

    def draw(self, filename, output=sys.stdout, absolute=False, x=None, y=None, w=None, h=None, ncolor=256, alphathreshold=0, chromakey=False, fast=True):
        try:
            filename.seek(0)
        except Exception:
            pass

        self.save_position(output)
        try:
            if x is not None:
                self.move_x(x, absolute, output)
            if y is not None:
                self.move_y(y, absolute, output)
            sixel_converter = SixelConverter(filename, self.f8bit, w, h, ncolor, alphathreshold=alphathreshold, chromakey=chromakey, fast=fast)
            sixel_converter.write(output, bodyonly=self._bodyonly)
        finally:
            self.restore_position(output)

        return