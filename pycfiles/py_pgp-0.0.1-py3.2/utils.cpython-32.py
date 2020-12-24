# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/utils.py
# Compiled at: 2015-08-31 10:09:30
import bz2, math, zlib
from Crypto.Cipher import blockalgo
from Crypto.Cipher import AES
from Crypto.Cipher import Blowfish
from Crypto.Cipher import DES3
from Crypto.Cipher import CAST
from Crypto.Hash import MD5
from Crypto.Hash import RIPEMD
from Crypto.Hash import SHA
from Crypto.Hash import SHA224
from Crypto.Hash import SHA256
from Crypto.Hash import SHA384
from Crypto.Hash import SHA512
from Crypto.PublicKey import DSA
from Crypto.PublicKey import ElGamal
from Crypto.PublicKey import RSA
from Crypto.Random import random
from Crypto.Signature import PKCS1_v1_5
from Crypto.Util.number import bytes_to_long
from Crypto.Util.number import GCD
from Crypto.Util.number import long_to_bytes
from pgp.cipher import aidea
from pgp.cipher import camellia
from pgp.cipher import twofish
from pgp.cipher import wrapper as syncable_cipher_wrapper
from pgp.exceptions import PublicKeyAlgorithmCannotSign
from pgp.exceptions import UnsupportedDigestAlgorithm
from pgp.exceptions import UnsupportedPublicKeyAlgorithm
from pgp.packets import constants
hash_lengths = {1: 16, 
 2: 20, 
 3: 20, 
 8: 32, 
 9: 48, 
 10: 64, 
 11: 28}
symmetric_cipher_block_lengths = {0: 0, 
 1: 8, 
 2: 8, 
 3: 8, 
 4: 8, 
 7: 16, 
 8: 16, 
 9: 16, 
 10: 16, 
 11: 16, 
 12: 16, 
 13: 16}
symmetric_cipher_key_lengths = {0: 0, 
 1: 16, 
 2: 24, 
 3: 16, 
 4: 16, 
 7: 16, 
 8: 24, 
 9: 32, 
 10: 16, 
 11: 16, 
 12: 24, 
 13: 32}

def sign_hash(pub_algorithm_type, secret_key, hash_, k=None):
    if pub_algorithm_type in (1, 3):
        sig_string = PKCS1_v1_5.new(secret_key).sign(hash_)
        return (
         bytes_to_long(sig_string),)
    else:
        if pub_algorithm_type == 20:
            if k is None:
                while 1:
                    k = random.StrongRandom().randint(1, secret_key.p - 1)
                    if GCD(k, secret_key.p - 1) == 1:
                        break

                print(k)
            sig_string = PKCS1_v1_5.EMSA_PKCS1_V1_5_ENCODE(hash_, secret_key.size())
            return secret_key.sign(sig_string, k)
        if pub_algorithm_type == 17:
            q = secret_key.q
            qbits = int(math.floor(float(math.log(q, 2)))) + 1
            qbytes = int(math.ceil(qbits / 8.0))
            if k is None:
                k = random.StrongRandom().randint(1, q - 1)
            digest = hash_.digest()[:qbytes]
            return secret_key.sign(bytes_to_long(digest), k)
        raise ValueError
        return


def verify_hash(pub_algorithm_type, public_key, hash_, values):
    if pub_algorithm_type in (1, 3):
        s = long_to_bytes(values[0])
        return PKCS1_v1_5.new(public_key).verify(hash_, s)
    if pub_algorithm_type == 20:
        sig_string = PKCS1_v1_5.EMSA_PKCS1_V1_5_ENCODE(hash_, public_key.size())
        return public_key.verify(sig_string, values)
    if pub_algorithm_type == 17:
        q = public_key.q
        qbits = int(math.floor(float(math.log(q, 2)))) + 1
        qbytes = int(math.ceil(qbits / 8.0))
        digest = hash_.digest()
        start = 0
        while digest[start] == b'\x00':
            start += 1

        digest = digest[start:start + qbytes]
        return public_key.verify(bytes_to_long(digest), values)
    raise ValueError


def get_hash_instance(type_):
    """Given a hash type code, returns a new hash instance for that
    type.
    """
    if type_ == 1:
        return MD5.new()
    else:
        if type_ == 2:
            return SHA.new()
        else:
            if type_ == 3:
                return RIPEMD.new()
            if type_ == 8:
                return SHA256.new()
            if type_ == 9:
                pass
            return SHA384.new()
        if type_ == 10:
            pass
        return SHA512.new()
    if type_ == 11:
        return SHA224.new()
    raise UnsupportedDigestAlgorithm(type_)


def get_public_key_constructor(type_):
    """Given a public key type code, returns a function which may be
    used to construct a new instance of that key.
    """
    if type_ == 1:
        return RSA.construct
    else:
        if type_ == 2:
            return RSA.construct
        if type_ == 3:
            return RSA.construct
        if type_ == 16:
            pass
        return ElGamal.construct
    if type_ == 17:
        return DSA.construct
    if type_ == 18:
        raise UnsupportedPublicKeyAlgorithm(18)
    else:
        if type_ == 19:
            raise UnsupportedPublicKeyAlgorithm(19)
        else:
            if type_ == 20:
                return ElGamal.construct
            if type_ == 21:
                raise PublicKeyAlgorithmCannotSign(21)
            else:
                if type_ == 105:
                    raise UnsupportedPublicKeyAlgorithm(105)
                else:
                    raise UnsupportedPublicKeyAlgorithm(type_)


class NoopCipher:

    def __init__(self, *args, **kwargs):
        pass

    def encrypt(self, block):
        return block

    def decrypt(self, block):
        return block


ECB = blockalgo.MODE_ECB
CBC = blockalgo.MODE_CBC
CFB = blockalgo.MODE_CFB
OFB = blockalgo.MODE_OFB
CTR = blockalgo.MODE_CTR
OPENPGP = blockalgo.MODE_OPENPGP

def get_symmetric_cipher(type_, key, mode, iv=None, segment_size=None, syncable=False):
    """
    """
    if mode == ECB:
        mode = blockalgo.MODE_ECB
    else:
        if mode == CBC:
            mode = blockalgo.MODE_CBC
        else:
            if mode == CFB:
                mode = blockalgo.MODE_CFB
            else:
                if mode == OFB:
                    mode = blockalgo.MODE_OFB
                else:
                    if mode == CTR:
                        mode = blockalgo.MODE_CTR
                    elif mode == OPENPGP:
                        mode = blockalgo.MODE_OPENPGP
    cipher = {0: NoopCipher, 
     1: aidea, 
     2: DES3, 
     3: CAST, 
     4: Blowfish, 
     7: AES, 
     8: AES, 
     9: AES, 
     10: twofish, 
     11: camellia, 
     12: camellia, 
     13: camellia}.get(type_, None)
    if segment_size is None and mode == blockalgo.MODE_CFB:
        segment_size = cipher.block_size * 8
    if syncable and cipher not in (aidea, twofish, camellia):
        try:
            return syncable_cipher_wrapper.new(cipher, bytes(key), mode, IV=bytes(iv), segment_size=segment_size)
        except TypeError:
            return syncable_cipher_wrapper.new(cipher, bytes(key.to_packet()), mode, iv=bytes(iv), segment_size=segment_size)

    try:
        return cipher.new(bytes(key), mode, IV=bytes(iv), segment_size=segment_size)
    except TypeError:
        return cipher.new(bytes(key.to_packet()), mode, iv=bytes(iv), segment_size=segment_size)

    return


class NoopCompression(object):

    def compress(self, data):
        return data

    def decompress(self, data):
        return data

    def flush(self):
        return b''


class ZlibCompression(object):

    def __init__(self, level):
        self._obj = None
        self._compress = None
        self._result = b''
        self.level = level
        return

    def compress(self, data):
        if self._result is None:
            raise ValueError
        if self._compress is False:
            raise ValueError
        if self._obj is None:
            self._compress = True
            self._obj = zlib.compressobj(self.level)
            self._result += self._obj.compress(data)
        return b''

    def decompress(self, data):
        if self._result is None:
            raise ValueError
        if self._compress is True:
            raise ValueError
        if self._obj is None:
            self._compress = False
            self._obj = zlib.decompressobj()
        self._result += self._obj.decompress(data)
        return b''

    def flush(self):
        if self._result is None:
            raise ValueError
        result = self._result
        result += self._obj.flush()
        self._result = None
        return result


_CompressionObj = zlib.compressobj().__class__
_DecompressionObj = zlib.decompressobj().__class__

class DeflateCompression(object):

    def __init__(self, level):
        self._obj = None
        self._compress = None
        self._result = b''
        self.level = level
        return

    def compress(self, data):
        if self._result is None:
            raise ValueError
        if self._compress is False:
            raise ValueError
        if self._obj is None:
            self._compress = True
            self._obj = zlib.compressobj(self.level)
        self._result += self._obj.compress(data)
        return b''

    def decompress(self, data):
        if self._result is None:
            raise ValueError
        if self._compress is True:
            raise ValueError
        if self._obj is None:
            self._compress = False
            self._obj = zlib.decompressobj()
            self._obj.decompress(b'x\x9c')
        self._result += self._obj.decompress(data)
        return b''

    def flush(self):
        if self._result is None:
            raise ValueError
        result = self._result
        result += self._obj.flush()
        self._result = None
        if self._compress:
            result = result[2:-4]
        return result


def get_compression_instance(type_, level=None):
    instance = None
    if type_ == 0:
        instance = NoopCompression()
    else:
        if type_ == 1:
            instance = DeflateCompression(level)
        else:
            if type_ == 2:
                instance = ZlibCompression(level)
            elif type_ == 3:
                instance = bz2.BZ2Compressor(level)
    return instance


def hash_key(data_to_hash, key_packet_data):
    """Adds key data to a hash for signature comparison."""
    key_length = len(key_packet_data)
    data_to_hash.append(153)
    data_to_hash.extend(int_to_2byte(key_length))
    data_to_hash.extend(key_packet_data)


def packet_type_from_first_byte(byte_):
    if byte_ & 127:
        return byte_ & 63
    return (byte_ & 63) >> 2


def hash_user_data(data_to_hash, target_type, target_packet_data, signature_version):
    """Adds user attribute & user id packets to a hash for signature
    comparison.
    """
    if target_type == 13:
        if signature_version >= 4:
            data_to_hash.append(180)
            data_to_hash.extend(int_to_4byte(len(target_packet_data)))
        data_to_hash.extend(target_packet_data)
    elif target_type == 17:
        if signature_version >= 4:
            data_to_hash.extend(bytearray([209]))
            data_to_hash.extend(int_to_4byte(len(target_packet_data)))
        data_to_hash.extend(target_packet_data)


def hash_packet_for_signature(packet_for_hash, signature_type, signature_version, hash_algorithm_type, signature_creation_time, pub_algorithm_type, public_key_packet=None, hashed_subpacket_data=None, fake_hash_algorithm_type=None):
    hash_ = get_hash_instance(hash_algorithm_type)
    data_to_hash = bytearray()
    public_key_packet_data = None
    if public_key_packet is not None:
        public_key_packet_data = public_key_packet.content
    packet_data_for_hash = packet_for_hash.content
    if signature_type in (constants.SIGNATURE_DIRECTLY_ON_A_KEY,
     constants.KEY_REVOCATION_SIGNATURE):
        assert public_key_packet_data is not None
        hash_key(data_to_hash, public_key_packet_data)
    else:
        if signature_type in (constants.SUBKEY_BINDING_SIGNATURE,
         constants.PRIMARY_KEY_BINDING_SIGNATURE,
         constants.SUBKEY_REVOCATION_SIGNATURE):
            assert public_key_packet_data is not None
            hash_key(data_to_hash, public_key_packet_data)
            hash_key(data_to_hash, packet_data_for_hash)
        else:
            if signature_type == constants.THIRD_PARTY_CONFIRMATION_SIGNATURE:
                data_to_hash.append(136)
                data_to_hash.append(len(packet_data_for_hash))
                data_to_hash.extend(packet_data_for_hash)
            else:
                if signature_type in (constants.SIGNATURE_OF_A_BINARY_DOCUMENT,
                 constants.SIGNATURE_OF_A_CANONICAL_TEXT_DOCUMENT):
                    data_to_hash.extend(packet_data_for_hash)
                else:
                    if signature_type == constants.STANDALONE_SIGNATURE:
                        pass
                    else:
                        if signature_type in (constants.GENERIC_CERTIFICATION,
                         constants.CASUAL_CERTIFICATION,
                         constants.PERSONA_CERTIFICATION,
                         constants.POSITIVE_CERTIFICATION,
                         constants.CERTIFICATION_REVOCATION_SIGNATURE):
                            assert public_key_packet_data is not None
                            hash_key(data_to_hash, public_key_packet_data)
                            hash_user_data(data_to_hash, packet_for_hash.type, packet_data_for_hash, signature_version)
                        elif signature_type == constants.TIMESTAMP_SIGNATURE:
                            data_to_hash.append(136)
                            data_to_hash.append(len(packet_data_for_hash))
                            data_to_hash.extend(packet_data_for_hash)
        if signature_version >= 4:
            data_to_hash.append(signature_version)
        data_to_hash.append(signature_type)
        if signature_version < 4:
            data_to_hash.extend(int_to_4byte(signature_creation_time))
        else:
            data_to_hash.append(pub_algorithm_type)
            data_to_hash.append(fake_hash_algorithm or hash_algorithm_type)
            hashed_subpacket_length = len(hashed_subpacket_data)
            data_to_hash.extend(int_to_2byte(hashed_subpacket_length))
            data_to_hash.extend(hashed_subpacket_data)
            data_to_hash.append(signature_version)
            data_to_hash.append(255)
            data_to_hash.extend(int_to_4byte(hashed_subpacket_length + 6))
    hash_ = get_hash_instance(hash_algorithm_type)
    hash_.update(data_to_hash)
    return hash_


def bytes_to_int(bytes_, offset, length):
    result = 0
    for i in range(length):
        shift = 8 * (length - i - 1)
        result += bytes_[(offset + i)] << shift

    return result


def byte_to_int(bytes_, offset):
    return bytes_to_int(bytes_, offset, 1)


def short_to_int(bytes_, offset):
    return bytes_to_int(bytes_, offset, 2)


def long_to_int(bytes_, offset):
    return bytes_to_int(bytes_, offset, 4)


def mpi_length(bytes_, offset):
    mpi_bit_length = short_to_int(bytes_, offset)
    return int(math.ceil(mpi_bit_length / 8.0))


def mpi_to_int(bytes_, offset):
    mpi_byte_length = mpi_length(bytes_, offset)
    offset += 2
    result = bytes_to_int(bytes_, offset, mpi_byte_length)
    offset += mpi_byte_length
    return (result, offset)


def int_to_bytes(i):
    bits_required = int(math.floor(float(math.log(i, 2)))) + 1
    bytes_required = int(math.ceil(bits_required / 8.0))
    result = bytearray([i >> j * 8 & 255 for j in range(bytes_required, 0, -1)])
    return result


def int_to_2byte(i):
    """Given an integer, return a bytearray of its short, unsigned
    representation, big-endian.
    """
    return bytearray([
     i >> 8 & 255,
     i & 255])


def int_to_4byte(i):
    """Given an integer, return a bytearray of its unsigned integer
    representation, big-endian.
    """
    return bytearray([
     i >> 24 & 255,
     i >> 16 & 255,
     i >> 8 & 255,
     i & 255])


def int_to_8byte(i):
    """Given an integer, return a bytearray of its unsigned integer
    representation, big-endian.
    """
    return bytearray([
     i >> 56 & 255,
     i >> 48 & 255,
     i >> 40 & 255,
     i >> 32 & 255,
     i >> 24 & 255,
     i >> 16 & 255,
     i >> 8 & 255,
     i & 255])


EXPBIAS = 6

def s2k_count_to_int(byte, offset=0):
    return 16 + (byte & 15) << (byte >> 4) + EXPBIAS


def int_to_s2k_count(i):
    if i < 1024:
        raise ValueError(i)
    if i > 65011712:
        raise ValueError(i)
    shift = int(math.floor(math.log(i, 2))) - 4
    if i & (1 << shift) - 1:
        raise ValueError(i)
    bits = i >> shift & 15
    return bytes([(shift - EXPBIAS << 4) + bits])


def int_to_hex(i, expected_size=None):
    fmt = '{:X}'
    if expected_size is not None:
        fmt = '{{:0{size}X}}'.format(size=expected_size)
    result = fmt.format(i)
    if expected_size is not None:
        result = result[-expected_size:]
    return result


def int_to_mpi(i):
    if i < 0:
        raise ValueError(i)
    elif i == 0:
        return bytearray([0, 0])
    bits_required = int(math.floor(float(math.log(i, 2)))) + 1
    bytes_required = int(math.ceil(bits_required / 8.0))
    result = bytearray() + int_to_2byte(bits_required)
    for b in range(bytes_required - 1, -1, -1):
        result.append(i >> b * 8 & 255)

    return result


MAX_PACKET_LENGTH = 4294967295

def old_packet_length_from_stream(fh):
    length_type = ord(fh.read(1)) & 3
    if length_type == 0:
        length = ord(fh.read(1))
    else:
        if length_type == 1:
            length = short_to_int(bytearray(fh.read(2)), 0)
        else:
            if length_type == 2:
                length = long_to_int(bytearray(fh.read(4)), 0)
            else:
                raise ValueError
    return length


def old_packet_length(data, offset):
    length_type = int(data[offset]) & 3
    offset += 1
    if length_type == 0:
        length = int(data[offset])
        offset += 1
    else:
        if length_type == 1:
            length = short_to_int(data, offset)
            offset += 2
        else:
            if length_type == 2:
                length = long_to_int(data, offset)
                offset += 4
            else:
                length = len(data) - offset
    return (
     offset, length)


def new_packet_length_from_stream(fh):
    length = ord(fh.read(1))
    partial = False
    if length < 192:
        pass
    else:
        if length < 224:
            length = (length - 192 << 8) + ord(fh.read(1)) + 192
        else:
            if length == 255:
                length = long_to_int(bytearray(fh.read(4)), 0)
            else:
                partial = True
                length = 1 << (length & 31)
    return (
     length, partial)


def new_packet_length(data, offset):
    length = int(data[offset])
    partial = False
    offset += 1
    if length < 192:
        pass
    else:
        if length < 224:
            length = (length - 192 << 8) + data[offset] + 192
            offset += 1
        else:
            if length == 255:
                length = long_to_int(data, offset)
                offset += 4
            else:
                partial = True
                length = 1 << (length & 31)
    return (
     offset, length, partial)


def new_packet_length_to_bytes(data_length, allow_partial):
    result = bytearray()
    remaining = 0
    if data_length < 192:
        result.append(data_length)
    else:
        if data_length < 8384:
            stored_length = data_length - 192
            result.append((stored_length >> 8) + 192)
            result.append(stored_length & 255)
        else:
            if data_length <= MAX_PACKET_LENGTH:
                result.append(255)
                result.append(data_length >> 24 & 255)
                result.append(data_length >> 16 & 255)
                result.append(data_length >> 8 & 255)
                result.append(data_length & 255)
            else:
                if allow_partial:
                    result.append(254)
                    remaining = data_length - 1073741824
                else:
                    raise ValueError('Cannot store data longer than {0} for subpackets or non-data packets.'.format(MAX_PACKET_LENGTH))
    return (
     result, remaining)


def old_packet_length_to_bytes(data_length):
    length_type = 0
    if data_length < 256:
        length_type = 0
        length_bytes = [data_length]
    else:
        if data_length < 65536:
            length_type = 1
            length_bytes = [data_length >> 8,
             data_length & 255]
        else:
            if data_length < 16777216:
                length_type = 2
                length_bytes = [data_length >> 24,
                 data_length >> 16 & 255,
                 data_length >> 8 & 255,
                 data_length & 255]
            else:
                length_type = 3
                length_bytes = []
    return (
     length_type, length_bytes)


def hex_to_bytes(hex_val, expected_length=None):
    result = bytearray()
    if expected_length is not None:
        result.extend([0] * expected_length)
    for i in range(int(len(hex_val) / 2)):
        idx = i * 2
        result.append(int(hex_val[idx:idx + 2], 16))

    if expected_length is not None:
        result = result[-expected_length:]
    return result


def bytearray_to_hex(arr, offset=0, expected=None):
    result = ''
    i = offset
    if expected is not None:
        assert not expected % 2, 'Must expect an even number of hex digits.'
        end = offset + expected / 2
    else:
        end = len(arr)
    while i < end:
        result += '{:02X}'.format(arr[i]).upper()
        i += 1

    if expected is not None:
        if len(result) < expected:
            result = '0' * len(result) - expected + result
        else:
            result = result[-1 * expected:]
    return result


def compare_packets(packet1, packet2):
    c = (packet1.raw > packet2.raw) - (packet1.raw < packet2.raw)
    if c:
        return c
    return (packet1.data > packet2.data) - (packet1.data < packet2.data)


def sort_key(packets):
    return sorted(packets, cmp=compare_packets)


def concat_key(packets):
    buf = bytearray()
    for packet in packets:
        packet_length = len(packet.data)
        buf.append(packet.raw)
        buf.extend([
         packet_length >> 24 & 255,
         packet_length >> 16 & 255,
         packet_length >> 8 & 255,
         packet_length & 255])
        buf.extend(packet.data)

    return buf


def hash_key_data(packets):
    canonical_key_data = concat_key(sort_key(packets))
    if not canonical_key_data:
        return bytes('')
    return bytearray(MD5.new(canonical_key_data).hexdigest())


def get_signature_values(signature_packet_data):
    """Get the actual public key signature values from the signature
    packet data.
    """
    data = signature_packet_data
    sig_version = data[0]
    offset = 1
    if sig_version in (2, 3):
        offset += 1
        offset += 1
        offset += 4
        offset += 8
        offset += 1
        offset += 1
        offset += 2
    elif sig_version >= 4:
        offset += 1
        offset += 1
        offset += 1
        length = short_to_int(data, offset)
        offset += 2
        offset += length
        length = short_to_int(data, offset)
        offset += 2
        offset += length
        offset += 2
    data_len = len(data)
    result = []
    while offset < data_len:
        mpi, offset = mpi_to_int(data, offset)
        result.append(mpi)

    return result


def key_packet_fingerprint(packet):
    if packet.version < 4:
        md5 = MD5.new()
        if packet.public_key_algorithm in (1, 2, 3):
            md5.update(int_to_bytes(packet.modulus_n))
            md5.update(int_to_bytes(packet.exponent_e))
        elif packet.public_key_algorithm in (16, 20):
            md5.update(int_to_bytes(packet.prime_p))
            md5.update(int_to_bytes(packet.group_generator_g))
        fingerprint = md5.hexdigest().upper()
    elif packet.version >= 4:
        sha1 = SHA.new()
        pubkey_data = packet.public_content
        pubkey_length = len(pubkey_data)
        seed_bytes = (
         153,
         pubkey_length >> 8 & 255,
         pubkey_length & 255)
        sha1.update(bytearray(seed_bytes))
        sha1.update(pubkey_data)
        fingerprint = sha1.hexdigest().upper()
    return fingerprint