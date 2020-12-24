# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/libsixel/encoder.py
# Compiled at: 2018-06-04 01:16:45
from . import _sixel
from libsixel import *

class Encoder(object):

    def __init__(self):
        self._encoder = sixel_encoder_new()

    def __del__(self):
        sixel_encoder_unref(self._encoder)

    def setopt(self, flag, arg=None):
        sixel_encoder_setopt(self._encoder, flag, arg)

    def encode(self, filename='-'):
        sixel_encoder_encode(self._encoder, filename)

    def encode_bytes(self, buf, width, height, pixelformat, palette):
        sixel_encoder_encode_bytes(self._encoder, buf, width, height, pixelformat, palette)

    def test(self, filename):
        import threading
        self.setopt(SIXEL_OPTFLAG_COLORS, 16)
        self.setopt(SIXEL_OPTFLAG_DIFFUSION, 'atkinson')
        self.setopt(SIXEL_OPTFLAG_WIDTH, 200)
        t = threading.Thread(target=self.encode, args=[filename])
        t.daemon = True
        t.start()
        try:
            while t.is_alive():
                t.join(1)

        except KeyboardInterrupt:
            print '\x1b\\\x1b[Jcanceled.'


if __name__ == '__main__':
    import sys
    arg1 = '-' if len(sys.argv) < 2 else sys.argv[1]
    Encoder().test(arg1)