# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nilsimsa/__init__.py
# Compiled at: 2016-04-10 08:46:46
"""
Purpose: Class and helper functions to compute and compare nilsimsa digests.

The Nilsimsa hash is a locality senstive hash function, generally
similar documents will have similar Nilsimsa digests.
The hamming distance between the digests can be used to approximate
the similarity between documents.
For further information consult http://en.wikipedia.org/wiki/Nilsimsa_Hash
and the references (particularly Damiani et al.)

Implementation details:
Nilsimsa class takes in a data paramater that can be an iterator over chunks of text or a text string.
Calling the methods hexdigest() and digest() give the nilsimsa
digest of the input data.
The helper function compare_digests takes in two digests and computes the Nilsimsa score.

This software is released under an MIT/X11 open source license.

Copyright 2012-2014 Diffeo, Inc.
"""
import sys
if sys.version_info[0] >= 3:
    PY3 = True
    text_type = str
    range_ = range
else:
    PY3 = False
    text_type = unicode
    range_ = xrange

def is_iterable_non_string(obj):
    return hasattr(obj, '__iter__') and not isinstance(obj, (bytes, text_type))


TRAN = [ ord(x) for x in b'\x02\xd6\x9eo\xf9\x1d\x04\xab\xd0"\x16\x1f\xd8s\xa1\xac;pb\x96\x1en\x8f9\x9d\x05\x14J\xa6\xbe\xae\x0e\xcf\xb9\x9c\x9a\xc7h\x13\xe1-\xa4\xebQ\x8ddkP#\x80\x03A\xec\xbbq\xccz\x86\x7f\x98\xf26^\xee\x8e\xceO\xb82\xb6_Y\xdc\x1b1L{\xf0c\x01l\xba\x07\xe8\x12wI<\xdaF\xfe/y\x1c\x9b0\xe3\x00\x06~.\x0f83!\xad\xa5T\xca\xa7)\xfcZGi}\xc5\x95\xb5\xf4\x0b\x90\xa3\x81m%U5\xf5ut\n&\xbf\x19\\\x1a\xc6\xff\x99]\x84\xaaf>\xafx\xb3 C\xc1\xed$\xea\xe6?\x18\xf3\xa0BW\x08S`\xc3\xc0\x83@\x82\xd7\t\xbdD*g\xa8\x93\xe0\xc2V\x9f\xd9\xdd\x85\x15\xb4\x8a\'(\x92v\xde\xef\xf8\xb2\xb7\xc9=E\x94K\x11\re\xd54\x8b\x91\x0c\xfa\x87\xe9|[\xb1M\xe5\xd4\xcb\x10\xa2\x17\x89\xbc\xdb\xb0\xe2\x97\x88R\xf7H\xd3a,:+\xd1\x8c\xfb\xf1\xcd\xe4j\xe7\xa9\xfd\xc47\xc8\xd2\xf6\xdfXrN'
       ]
POPC = [ ord(x) for x in '\x00\x01\x01\x02\x01\x02\x02\x03\x01\x02\x02\x03\x02\x03\x03\x04\x01\x02\x02\x03\x02\x03\x03\x04\x02\x03\x03\x04\x03\x04\x04\x05\x01\x02\x02\x03\x02\x03\x03\x04\x02\x03\x03\x04\x03\x04\x04\x05\x02\x03\x03\x04\x03\x04\x04\x05\x03\x04\x04\x05\x04\x05\x05\x06\x01\x02\x02\x03\x02\x03\x03\x04\x02\x03\x03\x04\x03\x04\x04\x05\x02\x03\x03\x04\x03\x04\x04\x05\x03\x04\x04\x05\x04\x05\x05\x06\x02\x03\x03\x04\x03\x04\x04\x05\x03\x04\x04\x05\x04\x05\x05\x06\x03\x04\x04\x05\x04\x05\x05\x06\x04\x05\x05\x06\x05\x06\x06\x07\x01\x02\x02\x03\x02\x03\x03\x04\x02\x03\x03\x04\x03\x04\x04\x05\x02\x03\x03\x04\x03\x04\x04\x05\x03\x04\x04\x05\x04\x05\x05\x06\x02\x03\x03\x04\x03\x04\x04\x05\x03\x04\x04\x05\x04\x05\x05\x06\x03\x04\x04\x05\x04\x05\x05\x06\x04\x05\x05\x06\x05\x06\x06\x07\x02\x03\x03\x04\x03\x04\x04\x05\x03\x04\x04\x05\x04\x05\x05\x06\x03\x04\x04\x05\x04\x05\x05\x06\x04\x05\x05\x06\x05\x06\x06\x07\x03\x04\x04\x05\x04\x05\x05\x06\x04\x05\x05\x06\x05\x06\x06\x07\x04\x05\x05\x06\x05\x06\x06\x07\x05\x06\x06\x07\x06\x07\x07\x08'
       ]

class Nilsimsa(object):
    """
    computes the nilsimsa has of an input data block, which can be an
    iterator over chunks, with each chunk corresponding to a block of text
    """

    def __init__(self, data=None):
        self._digest = None
        self.num_char = 0
        self.acc = [0] * 256
        self.window = []
        if data:
            if is_iterable_non_string(data):
                for chunk in data:
                    self.process(chunk)

            elif isinstance(data, (bytes, text_type)):
                self.process(data)
            else:
                raise TypeError(('Excpected string, iterable or None, got {}').format(type(data)))
        return

    def tran_hash(self, a, b, c, n):
        """implementation of the tran53 hash function"""
        return (TRAN[(a + n & 255)] ^ TRAN[b] * (n + n + 1)) + TRAN[(c ^ TRAN[n])] & 255

    def process(self, chunk):
        """
        computes the hash of all of the trigrams in the chunk using a window
        of length 5
        """
        self._digest = None
        if isinstance(chunk, text_type):
            chunk = chunk.encode('utf-8')
        for char in chunk:
            self.num_char += 1
            if PY3:
                c = char
            else:
                c = ord(char)
            if len(self.window) > 1:
                self.acc[self.tran_hash(c, self.window[0], self.window[1], 0)] += 1
            if len(self.window) > 2:
                self.acc[self.tran_hash(c, self.window[0], self.window[2], 1)] += 1
                self.acc[self.tran_hash(c, self.window[1], self.window[2], 2)] += 1
            if len(self.window) > 3:
                self.acc[self.tran_hash(c, self.window[0], self.window[3], 3)] += 1
                self.acc[self.tran_hash(c, self.window[1], self.window[3], 4)] += 1
                self.acc[self.tran_hash(c, self.window[2], self.window[3], 5)] += 1
                self.acc[self.tran_hash(self.window[3], self.window[0], c, 6)] += 1
                self.acc[self.tran_hash(self.window[3], self.window[2], c, 7)] += 1
            if len(self.window) < 4:
                self.window = [
                 c] + self.window
            else:
                self.window = [
                 c] + self.window[:3]

        return

    def compute_digest(self):
        """
        using a threshold (mean of the accumulator), computes the nilsimsa digest
        """
        num_trigrams = 0
        if self.num_char == 3:
            num_trigrams = 1
        else:
            if self.num_char == 4:
                num_trigrams = 4
            elif self.num_char > 4:
                num_trigrams = 8 * self.num_char - 28
            threshold = num_trigrams / 256.0
            digest = [
             0] * 32
            for i in range(256):
                if self.acc[i] > threshold:
                    digest[(i >> 3)] += 1 << (i & 7)

        self._digest = digest[::-1]

    @property
    def digest(self):
        """
        returns the digest, if it has not been computed, calls compute_digest
        """
        if self._digest is None:
            self.compute_digest()
        return self._digest

    def hexdigest(self):
        """
        computes the hex of the digest
        """
        return ('').join('%02x' % i for i in self.digest)

    def __str__(self):
        """convenience function"""
        return self.hexdigest()

    def from_file(self, fname):
        """read in a file and compute digest"""
        f = open(fname, 'rb')
        data = f.read()
        self.update(data)
        f.close()

    def compare(self, digest_2, is_hex=False):
        """
        returns difference between the nilsimsa digests between the current
        object and a given digest
        """
        if is_hex:
            digest_2 = convert_hex_to_ints(digest_2)
        bit_diff = 0
        for i in range(len(self.digest)):
            bit_diff += POPC[(self.digest[i] ^ digest_2[i])]

        return 128 - bit_diff


def convert_hex_to_ints(hexdigest):
    return [ int(hexdigest[i:i + 2], 16) for i in range(0, 63, 2) ]


def compare_digests(digest_1, digest_2, is_hex_1=True, is_hex_2=True, threshold=None):
    """
    computes bit difference between two nilsisa digests
    takes params for format, default is hex string but can accept list
    of 32 length ints
    Optimized method originally from https://gist.github.com/michelp/6255490

    If `threshold` is set, and the comparison will be less than
    `threshold`, then bail out early and return a value just below the
    threshold.  This is a speed optimization that accelerates
    comparisons of very different items; e.g. tests show a ~20-30% speed
    up.  `threshold` must be an integer in the range [-128, 128].

    """
    if threshold is not None:
        threshold -= 128
        threshold *= -1
    if is_hex_1 and is_hex_2:
        bits = 0
        for i in range_(0, 63, 2):
            bits += POPC[(255 & int(digest_1[i:i + 2], 16) ^ int(digest_2[i:i + 2], 16))]
            if threshold is not None and bits > threshold:
                break

        return 128 - bits
    else:
        if is_hex_1:
            digest_1 = convert_hex_to_ints(digest_1)
        if is_hex_2:
            digest_2 = convert_hex_to_ints(digest_2)
        bit_diff = 0
        for i in range(len(digest_1)):
            bit_diff += POPC[(255 & digest_1[i] ^ digest_2[i])]
            if threshold is not None and bit_diff > threshold:
                break

        return 128 - bit_diff
        return