# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/cipher/base.py
# Compiled at: 2015-08-31 08:17:33
__all__ = [
 '_InternalObj', 'MODE_CBC', 'MODE_CFB', 'MODE_CTR', 'MODE_EAX',
 'MODE_ECB', 'MODE_OFB', 'MODE_OPENPGP', 'MODE_PGP']
try:
    unicode
except NameError:
    unicode = str

class _InternalObj(object):
    block_size = None
    key_size = None
    segment_size = None
    counter = None
    _impl = None
    old_cipher = None
    IV = None
    mode = None
    count = None

    @classmethod
    def _create_impl(self, key):
        raise NotImplemented

    def _encrypt(self, bytes_):
        return self._impl.encrypt(bytes_)

    def _decrypt(self, bytes_):
        return self._impl.decrypt(bytes_)

    @classmethod
    def new(cls, key, mode=None, IV=None, counter=None, segment_size=0, *args, **kwargs):
        if mode is None:
            mode = MODE_ECB
        if mode < MODE_ECB or mode > MODE_CTR:
            raise ValueError('Unknown cipher feedback mode {0}'.format(mode))
        if mode == MODE_PGP:
            raise ValueError('MODE_PGP is not supported anymore')
        if len(key) not in cls.key_size:
            raise ValueError('Key must be 16, 24 or 32 bytes long, not {0}'.format(len(key)))
        if mode == MODE_ECB and IV:
            pass
        if mode == MODE_CTR and IV:
            raise ValueError('CTR mode needs counter parameter, not IV')
        if (IV is None or len(IV) != cls.block_size) and mode not in (MODE_ECB, MODE_CTR):
            raise ValueError('IV must be {0} bytes long'.format(cls.block_size))
        if mode == MODE_CFB:
            if segment_size == 0:
                segment_size = 8
            if segment_size < 1 or segment_size > cls.block_size * 8 or segment_size & 7 != 0:
                raise ValueError('Segment_size must be multiple of 8 (bits) between 1 and {0}. Got {1}.'.format(cls.block_size * 8, segment_size))
        if mode == MODE_CTR:
            if counter is None:
                raise TypeError("'counter' keyword parameter is required with CTR mode")
            if not callable(counter):
                raise ValueError("'counter' parameter must be a callable object")
        elif counter is not None:
            raise ValueError("'counter' parameter only useful with CTR mode")
        obj = cls()
        obj.segment_size = segment_size
        obj.counter = counter
        obj._impl = cls._create_impl(key)
        obj.key_size = len(key)
        obj.old_cipher = bytearray([0] * cls.block_size)
        obj.IV = IV
        if obj.IV is not None:
            if isinstance(IV, unicode):
                IV = IV.encode('ascii')
            obj.IV = bytearray(IV)
        obj.mode = mode
        obj.count = cls.block_size
        return obj

    def encrypt(self, plaintext):
        length = len(plaintext)
        plaintext = bytearray(plaintext)
        temp = bytearray([0] * self.block_size)
        result = bytearray([0] * length)
        i = 0
        if length % self.block_size and self.mode not in (MODE_CFB, MODE_OFB, MODE_CTR):
            raise ValueError('Input strings must be a multiple of {0} in length'.format(self.block_size))
        if self.mode == MODE_CFB and length % (self.segment_size // 8):
            raise ValueError('Input strings must be a multiple of the segment size {0} in length'.format(self.segment_size // 8))
        if self.mode == MODE_ECB:
            while i < length:
                result[i:i + self.block_size] = self._encrypt(bytes(plaintext[i:i + self.block_size]))
                i += self.block_size

        else:
            if self.mode == MODE_CBC:
                while i < length:
                    for j in range(self.block_size):
                        temp[j] = plaintext[(i + j)] ^ self.IV[j]

                    result[i:i + self.block_size] = bytearray(self._encrypt(bytes(temp)))
                    self.IV = result[i:i + self.block_size]
                    i += self.block_size

            else:
                if self.mode == MODE_CFB:
                    while i < length:
                        temp = bytearray(self._encrypt(bytes(self.IV)))
                        for j in range(0, self.segment_size // 8):
                            result[i + j] = temp[j] ^ plaintext[(i + j)]

                        if self.segment_size == self.block_size * 8:
                            self.IV = result[i:i + self.block_size]
                        else:
                            if self.segment_size % 8 == 0:
                                size = self.segment_size // 8
                                self.IV = self.IV[size:]
                                self.IV.extend(result[i:i + size])
                                if not len(self.IV) == self.block_size:
                                    raise AssertionError
                            else:
                                raise ValueError
                        i += self.segment_size // 8

                    self.count = abs(self.count - length % self.block_size)
                else:
                    if self.mode == MODE_OFB:
                        while i < length:
                            if length - i <= self.block_size - self.count:
                                for j in range(0, length - i):
                                    result[i + j] = self.IV[(self.count + j)] ^ plaintext[(i + j)]

                                self.count += length - i
                                i = length
                                continue
                            for j in range(0, self.block_size - self.count):
                                result[i + j] = self.IV[(self.count + j)] ^ plaintext[(i + j)]

                            i += self.block_size - self.count
                            self.count = self.block_size
                            self.IV = bytearray(self._encrypt(bytes(self.IV)))
                            self.count = 0

                    else:
                        if self.mode == MODE_CTR:
                            while i < length:
                                if length - i <= self.block_size - self.count:
                                    for j in range(0, length - i):
                                        self.IV[(self.count + j)] ^= plaintext[(i + j)]
                                        result[i + j] = self.IV[(self.count + j)]

                                    self.count += length - i
                                    i = length
                                    continue
                                for j in range(0, self.block_size - self.count):
                                    self.IV[(self.count + j)] ^= plaintext[(i + j)]
                                    result[i + j] = self.IV[(self.count + j)]

                                i += self.block_size - self.count
                                self.count = self.block_size
                                ctr = self.counter()
                                if not isinstance(ctr, (str, bytes, bytearray)):
                                    raise TypeError("CTR counter function didn't return a bytestring")
                                if len(ctr) != self.block_size:
                                    raise TypeError('CTR counter function returned bytestring not of length {0}'.format(self.block_size))
                                self.IV = bytearray(self._encrypt(bytes(ctr)))
                                self.count = 0

                        else:
                            raise RuntimeError("Unknown ciphertext feedback mode {0}; this shouldn't happen".format(self.mode))
        return bytes(result)

    def decrypt(self, ciphertext):
        ciphertext = bytearray(ciphertext)
        length = len(ciphertext)
        result = bytearray([0] * length)
        temp = bytearray([0] * self.block_size)
        i = 0
        if self.mode in (MODE_CTR, MODE_OFB):
            return self.encrypt(ciphertext)
        if length % self.block_size and self.mode != MODE_CFB:
            raise ValueError('Input strings must be a multiple of {0} in length'.format(self.block_size))
        if self.mode == MODE_CFB and length % (self.segment_size // 8):
            raise ValueError('Input strings must be a multiple of the segment size {0} in length'.format(self.segment_size // 8))
        if self.mode == MODE_ECB:
            while i < length:
                result[i:i + self.block_size] = bytearray(self._decrypt(bytes(ciphertext[i:i + self.block_size])))
                i += self.block_size

        else:
            if self.mode == MODE_CBC:
                while i < length:
                    self.old_cipher = self.IV[:]
                    temp = bytearray(self._decrypt(bytes(ciphertext[i:i + self.block_size])))
                    for j in range(0, self.block_size):
                        result[i + j] = temp[j] ^ self.IV[j]
                        self.IV[j] = ciphertext[(i + j)]

                    i += self.block_size

            else:
                if self.mode == MODE_CFB:
                    while i < length:
                        temp = bytearray(self._encrypt(bytes(self.IV)))
                        for j in range(0, self.segment_size // 8):
                            result[i + j] = temp[j] ^ ciphertext[(i + j)]

                        if self.segment_size == self.block_size * 8:
                            self.IV[:self.block_size] = ciphertext[i:i + self.block_size]
                        else:
                            if self.segment_size % 8 == 0:
                                size = self.segment_size // 8
                                self.IV = self.IV[size:]
                                self.IV.extend(ciphertext[i:i + size])
                                if not len(self.IV) == self.block_size:
                                    raise AssertionError
                            else:
                                raise ValueError
                        i += self.segment_size // 8

                    self.count = abs(self.count - length % self.block_size)
                else:
                    if self.mode == MODE_OFB:
                        i += self.segment_size // 8
                    else:
                        raise RuntimeError("Unknown ciphertext feedback mode {0}; this shouldn't happen".format(self.mode))
        return bytes(result)

    def sync(self):
        if self.mode == MODE_CFB:
            unused = self.block_size - self.count
            if unused == 0:
                return
            self.IV[unused:] = self.IV[:self.block_size - unused]
            self.IV[:unused] = self.old_cipher[self.block_size - unused:]
            assert len(self.IV) == self.block_size


MODE_ECB = 1
MODE_CBC = 2
MODE_CFB = 3
MODE_PGP = 4
MODE_OFB = 5
MODE_CTR = 6
MODE_OPENPGP = 7
MODE_EAX = 9