# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/libsixel/decoder.py
# Compiled at: 2018-06-04 01:16:45
from . import _sixel
from libsixel import *

class Decoder(object):

    def __init__(self):
        self._decoder = sixel_decoder_new()

    def __del__(self):
        sixel_decoder_unref(self._decoder)

    def setopt(self, flag, arg=None):
        sixel_decoder_setopt(self._decoder, flag, arg)

    def decode(self, infile=None):
        sixel_decoder_decode(self._decoder, infile)

    def test(self, infile=None, outfile=None):
        import threading
        if infile:
            self.setopt(SIXEL_OPTFLAG_INPUT, infile)
        if outfile:
            self.setopt(SIXEL_OPTFLAG_OUTPUT, outfile)
        t = threading.Thread(target=self.decode)
        t.daemon = True
        t.start()
        try:
            while t.is_alive():
                t.join(1)

        except KeyboardInterrupt:
            print '\x1b\\\x1b[Jcanceled.'


if __name__ == '__main__':
    import sys
    arg2 = '-' if len(sys.argv) < 3 else sys.argv[2]
    Decoder().test(arg1, arg2)