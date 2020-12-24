# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/oZip/core/Compression/huffman.py
# Compiled at: 2014-08-28 14:37:25
from base import Compressor, Decompressor
from huffman_utils import *

class HuffmanCompressor(Compressor):

    def __init__(self):
        Compressor.__init__(self)

    def compress(self, data):
        """ Compress data using Huffman code """
        try:
            assert isinstance(data, str) or isinstance(data, unicode)
        except AssertionError as e:
            raise TypeError('Data should be string, but is %s.' % str(type(data)))

        code = create_tree(data)
        encoding = create_encode_dict(code)
        compressed = ('').join(encoding[val] for val in data)
        decode_dict = build_decode_dict(encoding)
        try:
            json_decode = json.dumps(decode_dict).replace(' ', '')
        except UnicodeDecodeError:
            json_decode = json.dumps(decode_dict, ensure_ascii=False).replace(' ', '')

        bin_json = ('').join(('{:016b}').format(int(bin(ord(i))[2:], 2)) for i in json_decode)
        prefix = ('{:032b}').format(len(bin_json))
        return ('').join([prefix, bin_json, compressed])


class HuffmanDecompressor(Decompressor):
    """ Decompress a Huffman-code-compressed data """

    def __init__(self):
        Decompressor.__init__(self)

    def decompress(self, data):
        try:
            assert isinstance(data, str) or isinstance(data, unicode)
        except AssertionError as e:
            raise TypeError('Data should be string, but is %s.' % str(type(data)))

        decode, start = get_decoding_dict(data)
        result = []
        prefix = ''
        for bit in data[start:]:
            prefix += bit
            if prefix not in decode:
                continue
            decoded = decode[prefix]
            if decoded == '':
                decoded = ' '
            result.append(decoded)
            prefix = ''

        try:
            assert prefix == ''
        except AssertionError as e:
            for i in range(8 - len(prefix)):
                prefix = '0' + prefix
                if prefix in decode:
                    result.append(decode[prefix])
                    prefix = ''
                    break

            if prefix != '':
                raise ValueError('Decompression process finished with leftovers.')

        return ('').join(result)