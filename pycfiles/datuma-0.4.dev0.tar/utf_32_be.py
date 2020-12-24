# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/Cellar/python/2.7.13/Frameworks/Python.framework/Versions/2.7/lib/python2.7/encodings/utf_32_be.py
# Compiled at: 2016-12-19 04:17:02
"""
Python 'utf-32-be' Codec
"""
import codecs
encode = codecs.utf_32_be_encode

def decode(input, errors='strict'):
    return codecs.utf_32_be_decode(input, errors, True)


class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final=False):
        return codecs.utf_32_be_encode(input, self.errors)[0]


class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    _buffer_decode = codecs.utf_32_be_decode


class StreamWriter(codecs.StreamWriter):
    encode = codecs.utf_32_be_encode


class StreamReader(codecs.StreamReader):
    decode = codecs.utf_32_be_decode


def getregentry():
    return codecs.CodecInfo(name='utf-32-be', encode=encode, decode=decode, incrementalencoder=IncrementalEncoder, incrementaldecoder=IncrementalDecoder, streamreader=StreamReader, streamwriter=StreamWriter)