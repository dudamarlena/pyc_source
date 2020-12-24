# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: encodings\utf_16_be.pyc
# Compiled at: 2011-03-08 12:39:38
""" Python 'utf-16-be' Codec

Written by Marc-Andre Lemburg (mal@lemburg.com).

(c) Copyright CNRI, All Rights Reserved. NO WARRANTY.

"""
import codecs
encode = codecs.utf_16_be_encode

def decode(input, errors='strict'):
    return codecs.utf_16_be_decode(input, errors, True)


class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final=False):
        return codecs.utf_16_be_encode(input, self.errors)[0]


class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    _buffer_decode = codecs.utf_16_be_decode


class StreamWriter(codecs.StreamWriter):
    encode = codecs.utf_16_be_encode


class StreamReader(codecs.StreamReader):
    decode = codecs.utf_16_be_decode


def getregentry():
    return codecs.CodecInfo(name='utf-16-be', encode=encode, decode=decode, incrementalencoder=IncrementalEncoder, incrementaldecoder=IncrementalDecoder, streamreader=StreamReader, streamwriter=StreamWriter)