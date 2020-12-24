# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mdipierro/make_web2py/web2py/gluon/contrib/aes.py
# Compiled at: 2013-10-14 11:16:23
"""Simple AES cipher implementation in pure Python following PEP-272 API

Homepage: https://bitbucket.org/intgr/pyaes/

The goal of this module is to be as fast as reasonable in Python while still
being Pythonic and readable/understandable. It is licensed under the permissive
MIT license.

Hopefully the code is readable and commented enough that it can serve as an
introduction to the AES cipher for Python coders. In fact, it should go along
well with the Stick Figure Guide to AES:
http://www.moserware.com/2009/09/stick-figure-guide-to-advanced.html

Contrary to intuition, this implementation numbers the 4x4 matrices from top to
bottom for efficiency reasons::

  0  4  8 12
  1  5  9 13
  2  6 10 14
  3  7 11 15

Effectively it's the transposition of what you'd expect. This actually makes
the code simpler -- except the ShiftRows step, but hopefully the explanation
there clears it up.

"""
from array import array
MODE_ECB = 1
MODE_CBC = 2
block_size = 16
key_size = None

def new(key, mode=MODE_CBC, IV=None):
    if mode == MODE_ECB:
        return ECBMode(AES(key))
    else:
        if mode == MODE_CBC:
            if IV is None:
                raise ValueError('CBC mode needs an IV value!')
            return CBCMode(AES(key), IV)
        raise NotImplementedError
        return


class AES(object):
    block_size = 16

    def __init__(self, key):
        self.setkey(key)

    def setkey(self, key):
        """Sets the key and performs key expansion."""
        self.key = key
        self.key_size = len(key)
        if self.key_size == 16:
            self.rounds = 10
        elif self.key_size == 24:
            self.rounds = 12
        elif self.key_size == 32:
            self.rounds = 14
        else:
            raise ValueError('Key length must be 16, 24 or 32 bytes')
        self.expand_key()

    def expand_key(self):
        """Performs AES key expansion on self.key and stores in self.exkey"""
        exkey = array('B', self.key)
        if self.key_size == 16:
            extra_cnt = 0
        else:
            if self.key_size == 24:
                extra_cnt = 2
            else:
                extra_cnt = 3
            word = exkey[-4:]
            for i in xrange(1, 11):
                word = word[1:4] + word[0:1]
                for j in xrange(4):
                    word[j] = aes_sbox[word[j]]

                word[0] = word[0] ^ aes_Rcon[i]
                for z in xrange(4):
                    for j in xrange(4):
                        word[j] ^= exkey[(-self.key_size + j)]

                    exkey.extend(word)

                if len(exkey) >= (self.rounds + 1) * self.block_size:
                    break
                if self.key_size == 32:
                    for j in xrange(4):
                        word[j] = aes_sbox[word[j]] ^ exkey[(-self.key_size + j)]

                    exkey.extend(word)
                for z in xrange(extra_cnt):
                    for j in xrange(4):
                        word[j] ^= exkey[(-self.key_size + j)]

                    exkey.extend(word)

        self.exkey = exkey

    def add_round_key(self, block, round):
        """AddRoundKey step in AES. This is where the key is mixed into plaintext"""
        offset = round * 16
        exkey = self.exkey
        for i in xrange(16):
            block[i] ^= exkey[(offset + i)]

    def sub_bytes(self, block, sbox):
        """SubBytes step, apply S-box to all bytes

        Depending on whether encrypting or decrypting, a different sbox array
        is passed in.
        """
        for i in xrange(16):
            block[i] = sbox[block[i]]

    def shift_rows(self, b):
        """ShiftRows step. Shifts 2nd row to left by 1, 3rd row by 2, 4th row by 3

        Since we're performing this on a transposed matrix, cells are numbered
        from top to bottom::

          0  4  8 12   ->    0  4  8 12    -- 1st row doesn't change
          1  5  9 13   ->    5  9 13  1    -- row shifted to left by 1 (wraps around)
          2  6 10 14   ->   10 14  2  6    -- shifted by 2
          3  7 11 15   ->   15  3  7 11    -- shifted by 3
        """
        b[1], b[5], b[9], b[13] = (
         b[5], b[9], b[13], b[1])
        b[2], b[6], b[10], b[14] = (b[10], b[14], b[2], b[6])
        b[3], b[7], b[11], b[15] = (b[15], b[3], b[7], b[11])

    def shift_rows_inv(self, b):
        """Similar to shift_rows above, but performed in inverse for decryption."""
        b[5], b[9], b[13], b[1] = (
         b[1], b[5], b[9], b[13])
        b[10], b[14], b[2], b[6] = (b[2], b[6], b[10], b[14])
        b[15], b[3], b[7], b[11] = (b[3], b[7], b[11], b[15])

    def mix_columns(self, block):
        """MixColumns step. Mixes the values in each column"""
        mul_by_2 = gf_mul_by_2
        mul_by_3 = gf_mul_by_3
        for i in xrange(4):
            col = i * 4
            v0, v1, v2, v3 = (
             block[col], block[(col + 1)], block[(col + 2)],
             block[(col + 3)])
            block[col] = mul_by_2[v0] ^ v3 ^ v2 ^ mul_by_3[v1]
            block[col + 1] = mul_by_2[v1] ^ v0 ^ v3 ^ mul_by_3[v2]
            block[col + 2] = mul_by_2[v2] ^ v1 ^ v0 ^ mul_by_3[v3]
            block[col + 3] = mul_by_2[v3] ^ v2 ^ v1 ^ mul_by_3[v0]

    def mix_columns_inv(self, block):
        """Similar to mix_columns above, but performed in inverse for decryption."""
        mul_9 = gf_mul_by_9
        mul_11 = gf_mul_by_11
        mul_13 = gf_mul_by_13
        mul_14 = gf_mul_by_14
        for i in xrange(4):
            col = i * 4
            v0, v1, v2, v3 = (
             block[col], block[(col + 1)], block[(col + 2)],
             block[(col + 3)])
            block[col] = mul_14[v0] ^ mul_9[v3] ^ mul_13[v2] ^ mul_11[v1]
            block[col + 1] = mul_14[v1] ^ mul_9[v0] ^ mul_13[v3] ^ mul_11[v2]
            block[col + 2] = mul_14[v2] ^ mul_9[v1] ^ mul_13[v0] ^ mul_11[v3]
            block[col + 3] = mul_14[v3] ^ mul_9[v2] ^ mul_13[v1] ^ mul_11[v0]

    def encrypt_block(self, block):
        """Encrypts a single block. This is the main AES function"""
        self.add_round_key(block, 0)
        for round in xrange(1, self.rounds):
            self.sub_bytes(block, aes_sbox)
            self.shift_rows(block)
            self.mix_columns(block)
            self.add_round_key(block, round)

        self.sub_bytes(block, aes_sbox)
        self.shift_rows(block)
        self.add_round_key(block, self.rounds)

    def decrypt_block(self, block):
        """Decrypts a single block. This is the main AES decryption function"""
        self.add_round_key(block, self.rounds)
        for round in xrange(self.rounds - 1, 0, -1):
            self.shift_rows_inv(block)
            self.sub_bytes(block, aes_inv_sbox)
            self.add_round_key(block, round)
            self.mix_columns_inv(block)

        self.shift_rows_inv(block)
        self.sub_bytes(block, aes_inv_sbox)
        self.add_round_key(block, 0)


class ECBMode(object):
    """Electronic CodeBook (ECB) mode encryption.

    Basically this mode applies the cipher function to each block individually;
    no feedback is done. NB! This is insecure for almost all purposes
    """

    def __init__(self, cipher):
        self.cipher = cipher
        self.block_size = cipher.block_size

    def ecb(self, data, block_func):
        """Perform ECB mode with the given function"""
        if len(data) % self.block_size != 0:
            raise ValueError('Plaintext length must be multiple of 16')
        block_size = self.block_size
        data = array('B', data)
        for offset in xrange(0, len(data), block_size):
            block = data[offset:offset + block_size]
            block_func(block)
            data[offset:(offset + block_size)] = block

        return data.tostring()

    def encrypt(self, data):
        """Encrypt data in ECB mode"""
        return self.ecb(data, self.cipher.encrypt_block)

    def decrypt(self, data):
        """Decrypt data in ECB mode"""
        return self.ecb(data, self.cipher.decrypt_block)


class CBCMode(object):
    """Cipher Block Chaining (CBC) mode encryption. This mode avoids content leaks.

    In CBC encryption, each plaintext block is XORed with the ciphertext block
    preceding it; decryption is simply the inverse.
    """

    def __init__(self, cipher, IV):
        self.cipher = cipher
        self.block_size = cipher.block_size
        self.IV = array('B', IV)

    def encrypt(self, data):
        """Encrypt data in CBC mode"""
        block_size = self.block_size
        if len(data) % block_size != 0:
            raise ValueError('Plaintext length must be multiple of 16')
        data = array('B', data)
        IV = self.IV
        for offset in xrange(0, len(data), block_size):
            block = data[offset:offset + block_size]
            for i in xrange(block_size):
                block[i] ^= IV[i]

            self.cipher.encrypt_block(block)
            data[offset:(offset + block_size)] = block
            IV = block

        self.IV = IV
        return data.tostring()

    def decrypt(self, data):
        """Decrypt data in CBC mode"""
        block_size = self.block_size
        if len(data) % block_size != 0:
            raise ValueError('Ciphertext length must be multiple of 16')
        data = array('B', data)
        IV = self.IV
        for offset in xrange(0, len(data), block_size):
            ctext = data[offset:offset + block_size]
            block = ctext[:]
            self.cipher.decrypt_block(block)
            for i in xrange(block_size):
                block[i] ^= IV[i]

            data[offset:(offset + block_size)] = block
            IV = ctext

        self.IV = IV
        return data.tostring()


def galois_multiply(a, b):
    """Galois Field multiplicaiton for AES"""
    p = 0
    while b:
        if b & 1:
            p ^= a
        a <<= 1
        if a & 256:
            a ^= 27
        b >>= 1

    return p & 255


gf_mul_by_2 = array('B', [ galois_multiply(x, 2) for x in range(256) ])
gf_mul_by_3 = array('B', [ galois_multiply(x, 3) for x in range(256) ])
gf_mul_by_9 = array('B', [ galois_multiply(x, 9) for x in range(256) ])
gf_mul_by_11 = array('B', [ galois_multiply(x, 11) for x in range(256) ])
gf_mul_by_13 = array('B', [ galois_multiply(x, 13) for x in range(256) ])
gf_mul_by_14 = array('B', [ galois_multiply(x, 14) for x in range(256) ])
aes_sbox = array('B', ('637c777bf26b6fc53001672bfed7ab76ca82c97dfa5947f0add4a2af9ca472c0b7fd9326363ff7cc34a5e5f171d8311504c723c31896059a071280e2eb27b27509832c1a1b6e5aa0523bd6b329e32f8453d100ed20fcb15b6acbbe394a4c58cfd0efaafb434d338545f9027f503c9fa851a3408f929d38f5bcb6da2110fff3d2cd0c13ec5f974417c4a77e3d645d197360814fdc222a908846eeb814de5e0bdbe0323a0a4906245cc2d3ac629195e479e7c8376d8dd54ea96c56f4ea657aae08ba78252e1ca6b4c6e8dd741f4bbd8b8a703eb5664803f60e613557b986c11d9ee1f8981169d98e949b1e87e9ce5528df8ca1890dbfe6426841992d0fb054bb16').decode('hex'))
aes_inv_sbox = array('B', ('52096ad53036a538bf40a39e81f3d7fb7ce339829b2fff87348e4344c4dee9cb547b9432a6c2233dee4c950b42fac34e082ea16628d924b2765ba2496d8bd12572f8f66486689816d4a45ccc5d65b6926c704850fdedb9da5e154657a78d9d8490d8ab008cbcd30af7e45805b8b34506d02c1e8fca3f0f02c1afbd0301138a6b3a9111414f67dcea97f2cfcef0b4e67396ac7422e7ad3585e2f937e81c75df6e47f11a711d29c5896fb7620eaa18be1bfc563e4bc6d279209adbc0fe78cd5af41fdda8338807c731b11210592780ec5f60517fa919b54a0d2de57a9f93c99cefa0e03b4dae2af5b0c8ebbb3c83539961172b047eba77d626e169146355210c7d').decode('hex'))
aes_Rcon = array('B', ('8d01020408102040801b366cd8ab4d9a2f5ebc63c697356ad4b37dfaefc5913972e4d3bd61c29f254a943366cc831d3a74e8cb8d01020408102040801b366cd8ab4d9a2f5ebc63c697356ad4b37dfaefc5913972e4d3bd61c29f254a943366cc831d3a74e8cb8d01020408102040801b366cd8ab4d9a2f5ebc63c697356ad4b37dfaefc5913972e4d3bd61c29f254a943366cc831d3a74e8cb8d01020408102040801b366cd8ab4d9a2f5ebc63c697356ad4b37dfaefc5913972e4d3bd61c29f254a943366cc831d3a74e8cb8d01020408102040801b366cd8ab4d9a2f5ebc63c697356ad4b37dfaefc5913972e4d3bd61c29f254a943366cc831d3a74e8cb').decode('hex'))