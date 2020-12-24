# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/Projects/chris/various/pdfminer/venv/lib/python2.7/site-packages/pdfminer/runlength.py
# Compiled at: 2015-10-31 16:12:15
import six

def rldecode(data):
    """
    RunLength decoder (Adobe version) implementation based on PDF Reference
    version 1.4 section 3.3.4:
        The RunLengthDecode filter decodes data that has been encoded in a
        simple byte-oriented format based on run length. The encoded data
        is a sequence of runs, where each run consists of a length byte
        followed by 1 to 128 bytes of data. If the length byte is in the
        range 0 to 127, the following length + 1 (1 to 128) bytes are
        copied literally during decompression. If length is in the range
        129 to 255, the following single byte is to be copied 257 - length
        (2 to 128) times during decompression. A length value of 128
        denotes EOD.
    """
    decoded = ''
    i = 0
    while i < len(data):
        length = six.indexbytes(data, i)
        if length == 128:
            break
        if length >= 0 and length < 128:
            for j in range(i + 1, i + 1 + (length + 1)):
                decoded += six.int2byte(six.indexbytes(data, j))

            i = i + 1 + (length + 1)
        if length > 128:
            run = six.int2byte(six.indexbytes(data, i + 1)) * (257 - length)
            decoded += run
            i = i + 1 + 1

    return decoded