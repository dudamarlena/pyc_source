# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\Protocol\AllOrNothing.py
# Compiled at: 2013-03-13 13:15:35
"""This file implements all-or-nothing package transformations.

An all-or-nothing package transformation is one in which some text is
transformed into message blocks, such that all blocks must be obtained before
the reverse transformation can be applied.  Thus, if any blocks are corrupted
or lost, the original message cannot be reproduced.

An all-or-nothing package transformation is not encryption, although a block
cipher algorithm is used.  The encryption key is randomly generated and is
extractable from the message blocks.

This class implements the All-Or-Nothing package transformation algorithm
described in:

Ronald L. Rivest.  "All-Or-Nothing Encryption and The Package Transform"
http://theory.lcs.mit.edu/~rivest/fusion.pdf

"""
__revision__ = '$Id$'
import operator, sys
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Util.py3compat import *

def isInt(x):
    test = 0
    try:
        test += x
    except TypeError:
        return 0

    return 1


class AllOrNothing:
    """Class implementing the All-or-Nothing package transform.

    Methods for subclassing:

        _inventkey(key_size):
            Returns a randomly generated key.  Subclasses can use this to
            implement better random key generating algorithms.  The default
            algorithm is probably not very cryptographically secure.

    """

    def __init__(self, ciphermodule, mode=None, IV=None):
        """AllOrNothing(ciphermodule, mode=None, IV=None)

        ciphermodule is a module implementing the cipher algorithm to
        use.  It must provide the PEP272 interface.

        Note that the encryption key is randomly generated
        automatically when needed.  Optional arguments mode and IV are
        passed directly through to the ciphermodule.new() method; they
        are the feedback mode and initialization vector to use.  All
        three arguments must be the same for the object used to create
        the digest, and to undigest'ify the message blocks.
        """
        self.__ciphermodule = ciphermodule
        self.__mode = mode
        self.__IV = IV
        self.__key_size = ciphermodule.key_size
        if not isInt(self.__key_size) or self.__key_size == 0:
            self.__key_size = 16

    __K0digit = bchr(105)

    def digest(self, text):
        """digest(text:string) : [string]

        Perform the All-or-Nothing package transform on the given
        string.  Output is a list of message blocks describing the
        transformed text, where each block is a string of bit length equal
        to the ciphermodule's block_size.
        """
        key = self._inventkey(self.__key_size)
        K0 = self.__K0digit * self.__key_size
        mcipher = self.__newcipher(key)
        hcipher = self.__newcipher(K0)
        block_size = self.__ciphermodule.block_size
        padbytes = block_size - len(text) % block_size
        text = text + b(' ') * padbytes
        s = divmod(len(text), block_size)[0]
        blocks = []
        hashes = []
        for i in range(1, s + 1):
            start = (i - 1) * block_size
            end = start + block_size
            mi = text[start:end]
            assert len(mi) == block_size
            cipherblock = mcipher.encrypt(long_to_bytes(i, block_size))
            mticki = bytes_to_long(mi) ^ bytes_to_long(cipherblock)
            blocks.append(mticki)
            hi = hcipher.encrypt(long_to_bytes(mticki ^ i, block_size))
            hashes.append(bytes_to_long(hi))

        i = i + 1
        cipherblock = mcipher.encrypt(long_to_bytes(i, block_size))
        mticki = padbytes ^ bytes_to_long(cipherblock)
        blocks.append(mticki)
        hi = hcipher.encrypt(long_to_bytes(mticki ^ i, block_size))
        hashes.append(bytes_to_long(hi))
        mtick_stick = bytes_to_long(key) ^ reduce(operator.xor, hashes)
        blocks.append(mtick_stick)
        return [ long_to_bytes(i, self.__ciphermodule.block_size) for i in blocks ]

    def undigest(self, blocks):
        """undigest(blocks : [string]) : string

        Perform the reverse package transformation on a list of message
        blocks.  Note that the ciphermodule used for both transformations
        must be the same.  blocks is a list of strings of bit length
        equal to the ciphermodule's block_size.
        """
        if len(blocks) < 2:
            raise ValueError, 'List must be at least length 2.'
        blocks = map(bytes_to_long, blocks)
        K0 = self.__K0digit * self.__key_size
        hcipher = self.__newcipher(K0)
        block_size = self.__ciphermodule.block_size
        hashes = []
        for i in range(1, len(blocks)):
            mticki = blocks[(i - 1)] ^ i
            hi = hcipher.encrypt(long_to_bytes(mticki, block_size))
            hashes.append(bytes_to_long(hi))

        key = blocks[(-1)] ^ reduce(operator.xor, hashes)
        mcipher = self.__newcipher(long_to_bytes(key, self.__key_size))
        parts = []
        for i in range(1, len(blocks)):
            cipherblock = mcipher.encrypt(long_to_bytes(i, block_size))
            mi = blocks[(i - 1)] ^ bytes_to_long(cipherblock)
            parts.append(mi)

        padbytes = int(parts[(-1)])
        text = b('').join(map(long_to_bytes, parts[:-1]))
        return text[:-padbytes]

    def _inventkey(self, key_size):
        from Crypto import Random
        return Random.new().read(key_size)

    def __newcipher(self, key):
        if self.__mode is None and self.__IV is None:
            return self.__ciphermodule.new(key)
        else:
            if self.__IV is None:
                return self.__ciphermodule.new(key, self.__mode)
            else:
                return self.__ciphermodule.new(key, self.__mode, self.__IV)

            return


if __name__ == '__main__':
    import sys, getopt, base64
    usagemsg = 'Test module usage: %(program)s [-c cipher] [-l] [-h]\n\nWhere:\n    --cipher module\n    -c module\n        Cipher module to use.  Default: %(ciphermodule)s\n\n    --aslong\n    -l\n        Print the encoded message blocks as long integers instead of base64\n        encoded strings\n\n    --help\n    -h\n        Print this help message\n'
    ciphermodule = 'AES'
    aslong = 0

    def usage(code, msg=None):
        if msg:
            print msg
        print usagemsg % {'program': sys.argv[0], 'ciphermodule': ciphermodule}
        sys.exit(code)


    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:l', ['cipher=', 'aslong'])
    except getopt.error as msg:
        usage(1, msg)

    if args:
        usage(1, 'Too many arguments')
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage(0)
        elif opt in ('-c', '--cipher'):
            ciphermodule = arg
        elif opt in ('-l', '--aslong'):
            aslong = 1

    module = __import__('Crypto.Cipher.' + ciphermodule, None, None, ['new'])
    x = AllOrNothing(module)
    print 'Original text:\n=========='
    print __doc__
    print '=========='
    msgblocks = x.digest(b(__doc__))
    print 'message blocks:'
    for i, blk in zip(range(len(msgblocks)), msgblocks):
        print '    %3d' % i,
        if aslong:
            print bytes_to_long(blk)
        else:
            print base64.encodestring(blk)[:-1]

    y = AllOrNothing(module)
    text = y.undigest(msgblocks)
    if text == b(__doc__):
        print 'They match!'
    else:
        print 'They differ!'