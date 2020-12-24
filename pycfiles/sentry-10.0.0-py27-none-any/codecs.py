# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/digests/codecs.py
# Compiled at: 2019-08-16 12:27:40
from __future__ import absolute_import
import zlib
from sentry.utils.compat import pickle

class Codec(object):

    def encode(self, value):
        raise NotImplementedError

    def decode(self, value):
        raise NotImplementedError


class CompressedPickleCodec(Codec):

    def encode(self, value):
        return zlib.compress(pickle.dumps(value))

    def decode(self, value):
        return pickle.loads(zlib.decompress(value))