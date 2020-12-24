# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/helper/netstring.py
# Compiled at: 2012-07-12 07:18:13
from base64 import b64encode as enc
from base64 import b64decode as dec
try:
    import cPickle as pickle
except ImportError:
    import pickle

class NetStringDecodeError(Exception):
    """Represents an error related with netstring decoding."""
    pass


class NetString(object):

    def __init__(self, string, encoded=False):
        if not encoded:
            self.message = enc(string)
        else:
            self.message = string

    def __len__(self):
        return len(self.message)

    def __str__(self):
        return '%d:%s,' % (len(self), self.message)

    def __repr__(self):
        return str(self)

    @classmethod
    def from_buffer(self, buf):
        buf = buf.rstrip('\r\n')
        try:
            l = int(buf[0])
        except ValueError:
            raise NetStringDecodeError('Invalid length character: %c' % buf[0])

        if buf[(-1)] != ',':
            raise NetStringDecodeError('Invalid termination string: %c' % buf[(-1)])
        try:
            lenght, message = buf[:-1].split(':')
            if int(lenght) != len(message):
                raise NetStringDecodeError('Invalid declared length')
            return NetString(message, True)
        except ValueError:
            raise NetStringDecodeError("Malformed netstring: '%s'" % buf)

    def decode(self):
        return pickle.loads(dec(self.message))