# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/s2k.py
# Compiled at: 2015-08-31 08:17:33
import math
from pgp import utils

class SimpleS2K(object):
    """This directly hashes the string to produce the key data."""
    mode = 0

    @classmethod
    def from_bytes(cls, symmetric_algorithm, data, offset=0):
        hash_algorithm = data[offset]
        offset += 1
        return (cls(hash_algorithm, symmetric_algorithm), offset)

    def __init__(self, hash_algorithm, symmetric_algorithm, *args, **kwargs):
        self.hash_algorithm = hash_algorithm
        self.symmetric_algorithm = symmetric_algorithm
        self.salt = bytearray()
        self.count = None
        return

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.hash_algorithm == other.hash_algorithm and self.symmetric_algorithm == other.symmetric_algorithm and self.salt == other.salt and self.count == other.count

    def __bytes__(self):
        return bytes(bytearray([self.mode, self.hash_algorithm]) + bytearray(self.salt))

    def to_key(self, passphrase):
        required_length = utils.symmetric_cipher_key_lengths.get(self.symmetric_algorithm)
        hash_length = utils.hash_lengths.get(self.hash_algorithm)
        pass_ = 0
        result = bytearray()
        len2 = len(passphrase) + 8
        count = self.count
        if count is None:
            count = len2
        while pass_ * hash_length < required_length:
            hash_ = utils.get_hash_instance(self.hash_algorithm)
            hash_.update(bytearray([0] * pass_))
            for i in range(math.ceil(count / float(len2))):
                to_write = min(len2, count - len2 * i)
                hash_.update((bytes(self.salt) + bytes(passphrase))[:to_write])

            result.extend(bytearray(hash_.digest()))
            pass_ += 1

        return result[:required_length]


class SaltedS2K(SimpleS2K):
    mode = 1

    @classmethod
    def from_bytes(cls, symmetric_algorithm, data, offset=0):
        hash_algorithm = data[offset]
        offset += 1
        salt = data[offset:offset + 8]
        offset += 8
        return (cls(hash_algorithm, symmetric_algorithm, salt), offset)

    def __init__(self, hash_algorithm, symmetric_algorithm, salt, *args, **kwargs):
        SimpleS2K.__init__(self, hash_algorithm, symmetric_algorithm)
        self.salt = salt


class IteratedAndSaltedS2K(SaltedS2K):
    mode = 3

    @classmethod
    def from_bytes(cls, symmetric_algorithm, data, offset=0):
        hash_algorithm = data[offset]
        offset += 1
        salt = data[offset:offset + 8]
        offset += 8
        count = utils.s2k_count_to_int(data[offset])
        offset += 1
        return (cls(hash_algorithm, symmetric_algorithm, salt, count), offset)

    def __init__(self, hash_algorithm, symmetric_algorithm, salt, count):
        SaltedS2K.__init__(self, hash_algorithm, symmetric_algorithm, salt)
        self.count = count

    def __bytes__(self):
        result = SaltedS2K.__bytes__(self)
        result += utils.int_to_s2k_count(self.count)
        return result


class GnuPGS2K(SimpleS2K):

    @classmethod
    def from_bytes(cls, symmetric_algorithm, data, offset=0):
        serial_number = None
        serial_len = None
        hash_algorithm = data[offset]
        offset += 1
        gnu = data[offset:offset + 3]
        offset += 3
        if gnu != bytearray(b'GNU'):
            raise ValueError("S2K parsing error: expected 'GNU', got %s" % gnu)
        mode = data[offset]
        mode += 1000
        offset += 1
        if mode == 1001:
            pass
        else:
            if mode == 1002:
                serial_len = data[offset]
                offset += 1
                if serial_len < 0:
                    raise ValueError('Unexpected serial number length: %d' % serial_len)
                serial_number = utils.bytearray_to_hex(data, offset, serial_len)
                offset += serial_len
            else:
                raise ValueError('Unsupported GnuPG S2K extension, encountered mode %d' % mode)
            return (
             cls(hash_algorithm, mode, symmetric_algorithm, serial_number, serial_len), offset)

    def __init__(self, hash_algorithm, mode, symmetric_algorithm, serial_number=None, serial_number_length=None):
        SimpleS2K.__init__(self, hash_algorithm, symmetric_algorithm)
        self.mode = mode
        self.serial_number = serial_number
        self.serial_number_length = serial_number_length

    def __eq__(self, other):
        return super(GnuPGS2K, self).__eq__(other) and self.mode == other.mode and self.serial_number == other.serial_number and self.serial_number_length == other.serial_number_length

    def to_key(self, passphrase):
        pass

    def __bytes__(self):
        result = bytearray([
         self.hash_algorithm] + b'GNU' + [
         self.mode - 1000])
        if self.mode == 1002 and self.serial_number is not None:
            result.append(self.serial_number_length)
            result.extend(utils.hex_to_bytes(self.serial_number, self.serial_number_length))
        return bytes(result)


S2K_TYPES = {0: SimpleS2K, 
 1: SaltedS2K, 
 3: IteratedAndSaltedS2K, 
 101: GnuPGS2K}

def parse_s2k_bytes(cipher, data, offset=0):
    s2k_type = data[offset]
    offset += 1
    s2k_cls = S2K_TYPES.get(s2k_type, None)
    if s2k_cls is None:
        raise ValueError
    s2k, offset = s2k_cls.from_bytes(cipher, data, offset)
    return (s2k, offset)