# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cp1147/cp1147.py
# Compiled at: 2013-11-16 23:55:33
""" Python Character Mapping Codec cp1147 : EBCDIC France, Euro support
"""
import codecs

class Codec(codecs.Codec):

    def encode(self, input, errors='strict'):
        return codecs.charmap_encode(input, errors, encoding_table)

    def decode(self, input, errors='strict'):
        return codecs.charmap_decode(input, errors, decoding_table)


class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final=False):
        return codecs.charmap_encode(input, self.errors, encoding_table)[0]


class IncrementalDecoder(codecs.IncrementalDecoder):

    def decode(self, input, final=False):
        return codecs.charmap_decode(input, self.errors, decoding_table)[0]


class StreamWriter(Codec, codecs.StreamWriter):
    pass


class StreamReader(Codec, codecs.StreamReader):
    pass


def getregentry():
    return codecs.CodecInfo(name='cp1147', encode=Codec().encode, decode=Codec().decode, incrementalencoder=IncrementalEncoder, incrementaldecoder=IncrementalDecoder, streamreader=StreamReader, streamwriter=StreamWriter)


decoding_table = '\x00\x01\x02\x03\x9c\t\x86\x7f\x97\x8d\x8e\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x9d\x85\x08\x87\x18\x19\x92\x8f\x1c\x1d\x1e\x1f\x80\x81\x82\x83\x84\n\x17\x1b\x88\x89\x8a\x8b\x8c\x05\x06\x07\x90\x91\x16\x93\x94\x95\x96\x04\x98\x99\x9a\x9b\x14\x15\x9e\x1a \xa0âä@áãå\\ñ°.<(+!&{êë}íîïìß§$*);^-/ÂÄÀÁÃÅÇÑù,%_>?øÉÊËÈÍÎÏÌµ:£à\'="Øabcdefghi«»ðýþ±[jklmnopqrªºæ¸Æ€`¨stuvwxyz¡¿ÐÝÞ®¢#¥·©]¶¼½¾¬|¯~´×éABCDEFGHI\xadôöòóõèJKLMNOPQR¹ûü¦úÿç÷STUVWXYZ²ÔÖÒÓÕ0123456789³ÛÜÙÚ\x9f'
encoding_table = codecs.charmap_build(decoding_table)