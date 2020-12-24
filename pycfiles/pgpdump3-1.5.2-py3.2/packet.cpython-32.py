# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgpdump/packet.py
# Compiled at: 2015-08-26 06:45:04
from datetime import datetime, timedelta
import hashlib
from math import ceil, log
import re, zlib
from .utils import PgpdumpException, get_int2, get_int4, get_mpi, get_key_id, get_hex_data, get_int_bytes, pack_data

class Packet(object):
    """The base packet object containing various fields pulled from the packet
    header as well as a slice of the packet data."""

    def __init__(self, raw, name, new, data, original_data):
        self.raw = raw
        self.name = name
        self.new = new
        self.length = len(data)
        self.data = data
        self.original_data = original_data
        self.parse()

    def parse(self):
        """Perform any parsing necessary to populate fields on this packet.
        This method is called as the last step in __init__(). The base class
        method is a no-op; subclasses should use this as required."""
        return 0

    def __repr__(self):
        new = 'old'
        if self.new:
            new = 'new'
        return '<%s: %s (%d), %s, length %d>' % (
         self.__class__.__name__, self.name, self.raw, new, self.length)


class AlgoLookup(object):
    """Mixin class containing algorithm lookup methods."""
    pub_algorithms = {1: 'RSA Encrypt or Sign', 
     2: 'RSA Encrypt-Only', 
     3: 'RSA Sign-Only', 
     16: 'ElGamal Encrypt-Only', 
     17: 'DSA Digital Signature Algorithm', 
     18: 'Elliptic Curve', 
     19: 'ECDSA', 
     20: 'Formerly ElGamal Encrypt or Sign', 
     21: 'Diffie-Hellman'}
    oids = {b'2B81040023': ('NIST P-521', 521), 
     b'2B81040022': ('NIST P-384', 384), 
     b'2A8648CE3D030107': ('NIST P-256', 256), 
     b'2B240303020801010D': ('Brainpool P512 r1', 512), 
     b'2B240303020801010B': ('Brainpool P384 r1', 384), 
     b'2B2403030208010107': ('Brainpool P256 r1', 256), 
     b'2B06010401DA470F01': ('Curve 25519', None)}

    @classmethod
    def lookup_pub_algorithm(cls, alg):
        if 100 <= alg <= 110:
            return 'Private/Experimental algorithm'
        return cls.pub_algorithms.get(alg, 'Unknown')

    @classmethod
    def lookup_oid(cls, oid):
        return cls.oids.get(oid, ('Unknown', None))

    hash_algorithms = {1: 'MD5', 
     2: 'SHA1', 
     3: 'RIPEMD160', 
     8: 'SHA256', 
     9: 'SHA384', 
     10: 'SHA512', 
     11: 'SHA224'}

    @classmethod
    def lookup_hash_algorithm(cls, alg):
        if alg in (4, 5, 6, 7):
            return 'Reserved'
        if 100 <= alg <= 110:
            return 'Private/Experimental algorithm'
        return cls.hash_algorithms.get(alg, 'Unknown')

    sym_algorithms = {0: ('Plaintext or unencrypted', 0), 
     1: ('IDEA', 8), 
     2: ('Triple-DES', 8), 
     3: ('CAST5', 8), 
     4: ('Blowfish', 8), 
     5: ('Reserved', 8), 
     6: ('Reserved', 8), 
     7: ('AES with 128-bit key', 16), 
     8: ('AES with 192-bit key', 16), 
     9: ('AES with 256-bit key', 16), 
     10: ('Twofish with 256-bit key', 16), 
     11: ('Camellia with 128-bit key', 16), 
     12: ('Camellia with 192-bit key', 16), 
     13: ('Camellia with 256-bit key', 16)}

    @classmethod
    def _lookup_sym_algorithm(cls, alg):
        return cls.sym_algorithms.get(alg, ('Unknown', 0))

    @classmethod
    def lookup_sym_algorithm(cls, alg):
        return cls._lookup_sym_algorithm(alg)[0]

    @classmethod
    def lookup_sym_algorithm_iv(cls, alg):
        return cls._lookup_sym_algorithm(alg)[1]


class SignatureSubpacket(object):
    """A signature subpacket containing a type, type name, some flags, and the
    contained data."""
    CRITICAL_BIT = 128
    CRITICAL_MASK = 127

    def __init__(self, raw, hashed, data):
        self.raw = raw
        self.subtype = raw & self.CRITICAL_MASK
        self.hashed = hashed
        self.critical = bool(raw & self.CRITICAL_BIT)
        self.length = len(data)
        self.data = data

    subpacket_types = {2: 'Signature Creation Time', 
     3: 'Signature Expiration Time', 
     4: 'Exportable Certification', 
     5: 'Trust Signature', 
     6: 'Regular Expression', 
     7: 'Revocable', 
     9: 'Key Expiration Time', 
     10: 'Placeholder for backward compatibility', 
     11: 'Preferred Symmetric Algorithms', 
     12: 'Revocation Key', 
     16: 'Issuer', 
     20: 'Notation Data', 
     21: 'Preferred Hash Algorithms', 
     22: 'Preferred Compression Algorithms', 
     23: 'Key Server Preferences', 
     24: 'Preferred Key Server', 
     25: 'Primary User ID', 
     26: 'Policy URI', 
     27: 'Key Flags', 
     28: "Signer's User ID", 
     29: 'Reason for Revocation', 
     30: 'Features', 
     31: 'Signature Target', 
     32: 'Embedded Signature'}

    @property
    def name(self):
        if self.subtype in (0, 1, 8, 13, 14, 15, 17, 18, 19):
            return 'Reserved'
        return self.subpacket_types.get(self.subtype, 'Unknown')

    def __repr__(self):
        extra = ''
        if self.hashed:
            extra += 'hashed, '
        if self.critical:
            extra += 'critical, '
        return '<%s: %s, %slength %d>' % (
         self.__class__.__name__, self.name, extra, self.length)


class SignaturePacket(Packet, AlgoLookup):

    def __init__(self, *args, **kwargs):
        self.sig_version = None
        self.raw_sig_type = None
        self.raw_pub_algorithm = None
        self.raw_hash_algorithm = None
        self.raw_creation_time = None
        self.creation_time = None
        self.raw_expiration_time = None
        self.expiration_time = None
        self.key_id = None
        self.hash2 = None
        self.subpackets = []
        self.sig_data = None
        super(SignaturePacket, self).__init__(*args, **kwargs)
        return

    def parse(self):
        self.sig_version = self.data[0]
        offset = 1
        if self.sig_version in (2, 3):
            if self.data[offset] != 5:
                raise PgpdumpException('Invalid v3 signature packet')
            offset += 1
            self.raw_sig_type = self.data[offset]
            offset += 1
            self.raw_creation_time = get_int4(self.data, offset)
            self.creation_time = datetime.utcfromtimestamp(self.raw_creation_time)
            offset += 4
            self.key_id = get_key_id(self.data, offset)
            offset += 8
            self.raw_pub_algorithm = self.data[offset]
            offset += 1
            self.raw_hash_algorithm = self.data[offset]
            offset += 1
            self.hash2 = self.data[offset:offset + 2]
            offset += 2
        else:
            if self.sig_version == 4:
                self.raw_sig_type = self.data[offset]
                offset += 1
                self.raw_pub_algorithm = self.data[offset]
                offset += 1
                self.raw_hash_algorithm = self.data[offset]
                offset += 1
                length = get_int2(self.data, offset)
                offset += 2
                self.parse_subpackets(offset, length, True)
                offset += length
                length = get_int2(self.data, offset)
                offset += 2
                self.parse_subpackets(offset, length, False)
                offset += length
                self.hash2 = self.data[offset:offset + 2]
                offset += 2
                self.sig_data, offset = get_mpi(self.data, offset)
            else:
                raise PgpdumpException('Unsupported signature packet, version %d' % self.sig_version)
        return offset

    def parse_subpackets(self, outer_offset, outer_length, hashed=False):
        offset = outer_offset
        while offset < outer_offset + outer_length:
            sub_offset, sub_len, sub_part = new_tag_length(self.data, offset)
            sub_len -= 1
            offset += sub_offset
            subtype = self.data[offset]
            offset += 1
            sub_data = self.data[offset:offset + sub_len]
            if len(sub_data) != sub_len:
                raise PgpdumpException('Unexpected subpackets length: expected %d, got %d' % (
                 sub_len, len(sub_data)))
            subpacket = SignatureSubpacket(subtype, hashed, sub_data)
            if subpacket.subtype == 2:
                self.raw_creation_time = get_int4(subpacket.data, 0)
                self.creation_time = datetime.utcfromtimestamp(self.raw_creation_time)
            else:
                if subpacket.subtype == 3:
                    self.raw_expiration_time = get_int4(subpacket.data, 0)
                elif subpacket.subtype == 16:
                    self.key_id = get_key_id(subpacket.data, 0)
            offset += sub_len
            self.subpackets.append(subpacket)

        if self.raw_expiration_time:
            self.expiration_time = self.creation_time + timedelta(seconds=self.raw_expiration_time)

    sig_types = {0: 'Signature of a binary document', 
     1: 'Signature of a canonical text document', 
     2: 'Standalone signature', 
     16: 'Generic certification of a User ID and Public Key packet', 
     17: 'Persona certification of a User ID and Public Key packet', 
     18: 'Casual certification of a User ID and Public Key packet', 
     19: 'Positive certification of a User ID and Public Key packet', 
     24: 'Subkey Binding Signature', 
     25: 'Primary Key Binding Signature', 
     31: 'Signature directly on a key', 
     32: 'Key revocation signature', 
     40: 'Subkey revocation signature', 
     48: 'Certification revocation signature', 
     64: 'Timestamp signature', 
     80: 'Third-Party Confirmation signature'}

    @property
    def sig_type(self):
        return self.sig_types.get(self.raw_sig_type, 'Unknown')

    @property
    def pub_algorithm(self):
        return self.lookup_pub_algorithm(self.raw_pub_algorithm)

    @property
    def hash_algorithm(self):
        return self.lookup_hash_algorithm(self.raw_hash_algorithm)

    def __repr__(self):
        return '<%s: %s, %s, length %d>' % (
         self.__class__.__name__, self.pub_algorithm,
         self.hash_algorithm, self.length)


class PublicKeyPacket(Packet, AlgoLookup):

    def __init__(self, *args, **kwargs):
        self.pubkey_version = None
        self.fingerprint = None
        self.key_id = None
        self.raw_creation_time = None
        self.creation_time = None
        self.raw_days_valid = None
        self.expiration_time = None
        self.raw_pub_algorithm = None
        self.pub_algorithm_type = None
        self.modulus = None
        self.modulus_bitlen = None
        self.exponent = None
        self.prime = None
        self.group_order = None
        self.group_gen = None
        self.key_value = None
        self.bitlen = None
        self.raw_oid = None
        self.raw_oid_length = None
        self.oid = None
        super(PublicKeyPacket, self).__init__(*args, **kwargs)
        return

    def parse(self):
        self.pubkey_version = self.data[0]
        offset = 1
        if self.pubkey_version in (2, 3):
            self.raw_creation_time = get_int4(self.data, offset)
            self.creation_time = datetime.utcfromtimestamp(self.raw_creation_time)
            offset += 4
            self.raw_days_valid = get_int2(self.data, offset)
            offset += 2
            if self.raw_days_valid > 0:
                self.expiration_time = self.creation_time + timedelta(days=self.raw_days_valid)
            self.raw_pub_algorithm = self.data[offset]
            offset += 1
            offset = self.parse_key_material(offset)
            md5 = hashlib.md5()
            if self.pub_algorithm_type == 'rsa':
                key_id = ('%X' % self.modulus)[-8:].zfill(8)
                self.key_id = key_id.encode('ascii')
                md5.update(get_int_bytes(self.modulus))
                md5.update(get_int_bytes(self.exponent))
            else:
                if self.pub_algorithm_type == 'elg':
                    key_id = ('%X' % self.prime)[-8:].zfill(8)
                    self.key_id = key_id.encode('ascii')
                    md5.update(get_int_bytes(self.prime))
                    md5.update(get_int_bytes(self.group_gen))
                else:
                    raise PgpdumpException('Invalid non-RSA v%d public key' % self.pubkey_version)
            self.fingerprint = md5.hexdigest().upper().encode('ascii')
        else:
            if self.pubkey_version == 4:
                sha1 = hashlib.sha1()
                seed_bytes = (153, self.length >> 8 & 255, self.length & 255)
                sha1.update(pack_data(bytearray(seed_bytes)))
                sha1.update(pack_data(self.data))
                self.fingerprint = sha1.hexdigest().upper().encode('ascii')
                self.key_id = self.fingerprint[24:]
                self.raw_creation_time = get_int4(self.data, offset)
                self.creation_time = datetime.utcfromtimestamp(self.raw_creation_time)
                offset += 4
                self.raw_pub_algorithm = self.data[offset]
                offset += 1
                offset = self.parse_key_material(offset)
            else:
                raise PgpdumpException('Unsupported public key packet, version %d' % self.pubkey_version)
        return offset

    def parse_key_material(self, offset):
        if self.raw_pub_algorithm in (1, 2, 3):
            self.pub_algorithm_type = 'rsa'
            self.modulus, offset = get_mpi(self.data, offset)
            self.exponent, offset = get_mpi(self.data, offset)
            self.modulus_bitlen = int(ceil(log(self.modulus, 2)))
            self.bitlen = self.modulus_bitlen
        else:
            if self.raw_pub_algorithm == 17:
                self.pub_algorithm_type = 'dsa'
                self.prime, offset = get_mpi(self.data, offset)
                self.group_order, offset = get_mpi(self.data, offset)
                self.group_gen, offset = get_mpi(self.data, offset)
                self.key_value, offset = get_mpi(self.data, offset)
                self.bitlen = int(ceil(log(self.key_value, 2)))
            else:
                if self.raw_pub_algorithm in (16, 20):
                    self.pub_algorithm_type = 'elg'
                    self.prime, offset = get_mpi(self.data, offset)
                    self.group_gen, offset = get_mpi(self.data, offset)
                    self.key_value, offset = get_mpi(self.data, offset)
                else:
                    if self.raw_pub_algorithm == 18:
                        self.pub_algorithm_type = 'ecc'
                        offset = self.parse_oid_data(offset)
                    else:
                        if self.raw_pub_algorithm == 19:
                            self.pub_algorithm_type = 'ecdsa'
                            offset = self.parse_oid_data(offset)
                        else:
                            if self.raw_pub_algorithm == 22:
                                self.pub_algorithm_type = 'curve25519'
                                offset = self.parse_oid_data(offset)
                            else:
                                if 100 <= self.raw_pub_algorithm <= 110:
                                    pass
                                else:
                                    raise PgpdumpException('Unsupported public key algorithm %d' % self.raw_pub_algorithm)
        return offset

    def parse_oid_data(self, offset):
        oid_length = self.data[offset]
        offset += 1
        oid = get_hex_data(self.data, offset, oid_length)
        offset += oid_length
        self.raw_oid = oid
        self.raw_oid_length = oid_length
        oid_value = self.lookup_oid(self.raw_oid)
        self.oid = oid_value[0]
        self.bitlen = oid_value[1]
        return offset

    @property
    def pub_algorithm(self):
        return self.lookup_pub_algorithm(self.raw_pub_algorithm)

    def __repr__(self):
        return '<%s: 0x%s, %s, length %d>' % (
         self.__class__.__name__, self.key_id.decode('ascii'),
         self.pub_algorithm, self.length)


class PublicSubkeyPacket(PublicKeyPacket):
    """A Public-Subkey packet (tag 14) has exactly the same format as a
    Public-Key packet, but denotes a subkey."""
    pass


class SecretKeyPacket(PublicKeyPacket):
    s2k_types = {0: ('Simple S2K', 2), 
     1: ('Salted S2K', 10), 
     2: ('Reserved value', 0), 
     3: ('Iterated and Salted S2K', 11), 
     101: ('GnuPG S2K', 6)}

    def __init__(self, *args, **kwargs):
        self.s2k_id = None
        self.s2k_type = None
        self.s2k_cipher = None
        self.s2k_hash = None
        self.s2k_iv = None
        self.checksum = None
        self.serial_number = None
        self.exponent_d = None
        self.prime_p = None
        self.prime_q = None
        self.multiplicative_inverse = None
        self.exponent_x = None
        super(SecretKeyPacket, self).__init__(*args, **kwargs)
        return

    @classmethod
    def lookup_s2k(cls, s2k_type_id):
        return cls.s2k_types.get(s2k_type_id, ('Unknown', 0))

    def parse(self):
        offset = super(SecretKeyPacket, self).parse()
        self.s2k_id = self.data[offset]
        offset += 1
        if self.s2k_id == 0:
            offset = self.parse_private_key_material(offset)
            self.checksum = get_int2(self.data, offset)
            offset += 2
        elif self.s2k_id in (254, 255):
            cipher_id = self.data[offset]
            offset += 1
            self.s2k_cipher = self.lookup_sym_algorithm(cipher_id)
            offset_before_s2k = offset
            s2k_type_id = self.data[offset]
            offset += 1
            name, s2k_length = self.lookup_s2k(s2k_type_id)
            self.s2k_type = name
            has_iv = True
        if s2k_type_id == 0:
            hash_id = self.data[offset]
            offset += 1
            self.s2k_hash = self.lookup_hash_algorithm(hash_id)
        else:
            if s2k_type_id == 1:
                hash_id = self.data[offset]
                offset += 1
                self.s2k_hash = self.lookup_hash_algorithm(hash_id)
                offset += 8
            else:
                if s2k_type_id == 2:
                    pass
                else:
                    if s2k_type_id == 3:
                        hash_id = self.data[offset]
                        offset += 1
                        self.s2k_hash = self.lookup_hash_algorithm(hash_id)
                        offset += 8
                        offset += 1
                    else:
                        if 100 <= s2k_type_id <= 110:
                            hash_id = self.data[offset]
                            offset += 1
                            self.s2k_hash = self.lookup_hash_algorithm(hash_id)
                            gnu = self.data[offset:offset + 3]
                            offset += 3
                            if gnu != bytearray(b'GNU'):
                                raise PgpdumpException("S2K parsing error: expected 'GNU', got %s" % gnu)
                            mode = self.data[offset]
                            mode += 1000
                            offset += 1
                            if mode == 1001:
                                has_iv = False
                            else:
                                if mode == 1002:
                                    has_iv = False
                                    serial_len = self.data[offset]
                                    if serial_len < 0:
                                        raise PgpdumpException('Unexpected serial number length: %d' % serial_len)
                                    self.serial_number = get_hex_data(self.data, offset + 1, serial_len)
                                else:
                                    raise PgpdumpException('Unsupported GnuPG S2K extension, encountered mode %d' % mode)
                        else:
                            raise PgpdumpException('Unsupported public key algorithm %d' % s2k_type_id)
            if s2k_length != offset - offset_before_s2k:
                raise PgpdumpException('Error parsing string-to-key specifier, mismatched length')
            if has_iv:
                s2k_iv_len = self.lookup_sym_algorithm_iv(cipher_id)
                self.s2k_iv = self.data[offset:offset + s2k_iv_len]
                offset += s2k_iv_len
            return offset

    def parse_private_key_material(self, offset):
        if self.raw_pub_algorithm in (1, 2, 3):
            self.pub_algorithm_type = 'rsa'
            self.exponent_d, offset = get_mpi(self.data, offset)
            self.prime_p, offset = get_mpi(self.data, offset)
            self.prime_q, offset = get_mpi(self.data, offset)
            self.multiplicative_inverse, offset = get_mpi(self.data, offset)
        else:
            if self.raw_pub_algorithm == 17:
                self.pub_algorithm_type = 'dsa'
                self.exponent_x, offset = get_mpi(self.data, offset)
            else:
                if self.raw_pub_algorithm in (16, 20):
                    self.pub_algorithm_type = 'elg'
                    self.exponent_x, offset = get_mpi(self.data, offset)
                else:
                    if 100 <= self.raw_pub_algorithm <= 110:
                        pass
                    else:
                        raise PgpdumpException('Unsupported public key algorithm %d' % self.raw_pub_algorithm)
        return offset


class SecretSubkeyPacket(SecretKeyPacket):
    """A Secret-Subkey packet (tag 7) has exactly the same format as a
    Secret-Key packet, but denotes a subkey."""
    pass


class UserIDPacket(Packet):
    """A User ID packet consists of UTF-8 text that is intended to represent
    the name and email address of the key holder. By convention, it includes an
    RFC 2822 mail name-addr, but there are no restrictions on its content."""

    def __init__(self, *args, **kwargs):
        self.user = None
        self.user_name = None
        self.user_email = None
        super(UserIDPacket, self).__init__(*args, **kwargs)
        return

    user_re = re.compile('^([^<]+)? ?<([^>]*)>?')

    def parse(self):
        self.user = self.data.decode('utf8', 'replace')
        matches = self.user_re.match(self.user)
        if matches:
            if matches.group(1):
                self.user_name = matches.group(1).strip()
            if matches.group(2):
                self.user_email = matches.group(2).strip()
        return self.length

    def __repr__(self):
        return '<%s: %r (%r), length %d>' % (
         self.__class__.__name__, self.user_name, self.user_email,
         self.length)


class UserAttributePacket(Packet):

    def __init__(self, *args, **kwargs):
        self.raw_image_format = None
        self.image_format = None
        self.image_data = None
        super(UserAttributePacket, self).__init__(*args, **kwargs)
        return

    def parse(self):
        offset = sub_offset = sub_len = 0
        while offset + sub_len < self.length:
            sub_offset, sub_len, sub_part = new_tag_length(self.data, offset)
            sub_len -= 1
            offset += sub_offset
            sub_type = self.data[offset]
            offset += 1
            if sub_type == 1:
                hdr_size = self.data[offset] + (self.data[(offset + 1)] << 8)
                hdr_version = self.data[(offset + 2)]
                self.raw_image_format = self.data[(offset + 3)]
                offset += hdr_size
                self.image_data = self.data[offset:]
                if self.raw_image_format == 1:
                    self.image_format = 'jpeg'
                else:
                    self.image_format = 'unknown'
                    continue

        return self.length


class TrustPacket(Packet):

    def __init__(self, *args, **kwargs):
        self.trust = None
        super(TrustPacket, self).__init__(*args, **kwargs)
        return

    def parse(self):
        """GnuPG public keyrings use a 2-byte trust value that appears to be
        integer values into some internal enumeration."""
        if self.length == 2:
            self.trust = get_int2(self.data, 0)
            return 2
        return 0


class PublicKeyEncryptedSessionKeyPacket(Packet, AlgoLookup):

    def __init__(self, *args, **kwargs):
        self.session_key_version = None
        self.key_id = None
        self.raw_pub_algorithm = None
        self.pub_algorithm = None
        super(PublicKeyEncryptedSessionKeyPacket, self).__init__(*args, **kwargs)
        return

    def parse(self):
        self.session_key_version = self.data[0]
        if self.session_key_version == 3:
            self.key_id = get_key_id(self.data, 1)
            self.raw_pub_algorithm = self.data[9]
            self.pub_algorithm = self.lookup_pub_algorithm(self.raw_pub_algorithm)
        else:
            raise PgpdumpException('Unsupported encrypted session key packet, version %d' % self.session_key_version)
        return 10

    def __repr__(self):
        return '<%s: 0x%s (%s), length %d>' % (
         self.__class__.__name__, self.key_id, self.pub_algorithm,
         self.length)


class CompressedDataPacket(Packet):

    def __init__(self, *args, **kwargs):
        self.decompressed_data = None
        self.raw_compression_algo = None
        super(CompressedDataPacket, self).__init__(*args, **kwargs)
        return

    def parse(self):
        offset = super(CompressedDataPacket, self).parse()
        self.raw_compression_algo = self.data[offset]
        offset += 1
        if self.raw_compression_algo == 1:
            self.decompressed_data = zlib.decompress(self.data[offset:offset + self.length], -zlib.MAX_WBITS)
        return self.length

    def __repr__(self):
        return '<%s: Algo %s, length %s>' % (
         self.__class__.__name__, self.raw_compression_algo, self.length)


TAG_TYPES = {0: ('Reserved', None), 
 1: (
     'Public-Key Encrypted Session Key Packet',
     PublicKeyEncryptedSessionKeyPacket), 
 2: (
     'Signature Packet', SignaturePacket), 
 3: ('Symmetric-Key Encrypted Session Key Packet', None), 
 4: ('One-Pass Signature Packet', None), 
 5: (
     'Secret Key Packet', SecretKeyPacket), 
 6: (
     'Public Key Packet', PublicKeyPacket), 
 7: (
     'Secret Subkey Packet', SecretSubkeyPacket), 
 8: (
     'Compressed Data Packet', CompressedDataPacket), 
 9: ('Symmetrically Encrypted Data Packet', None), 
 10: ('Marker Packet', None), 
 11: ('Literal Data Packet', None), 
 12: (
      'Trust Packet', TrustPacket), 
 13: (
      'User ID Packet', UserIDPacket), 
 14: (
      'Public Subkey Packet', PublicSubkeyPacket), 
 17: (
      'User Attribute Packet', UserAttributePacket), 
 18: ('Symmetrically Encrypted and MDC Packet', None), 
 19: ('Modification Detection Code Packet', None), 
 60: ('Private', None), 
 61: ('Private', None), 
 62: ('Private', None), 
 63: ('Private', None)}

def new_tag_length(data, start):
    """Takes a bytearray of data as input, as well as an offset of where to
    look. Returns a derived (offset, length, partial) tuple.
    Reference: http://tools.ietf.org/html/rfc4880#section-4.2.2
    """
    first = data[start]
    offset = length = 0
    partial = False
    if first < 192:
        offset = 1
        length = first
    else:
        if first < 224:
            offset = 2
            length = (first - 192 << 8) + data[(start + 1)] + 192
        else:
            if first == 255:
                offset = 5
                length = get_int4(data, start + 1)
            else:
                offset = 1
                length = 1 << (first & 31)
                partial = True
    return (
     offset, length, partial)


def old_tag_length(data, start):
    """Takes a bytearray of data as input, as well as an offset of where to
    look. Returns a derived (offset, length) tuple."""
    offset = length = 0
    temp_len = data[start] & 3
    if temp_len == 0:
        offset = 1
        length = data[(start + 1)]
    else:
        if temp_len == 1:
            offset = 2
            length = get_int2(data, start + 1)
        else:
            if temp_len == 2:
                offset = 4
                length = get_int4(data, start + 1)
            elif temp_len == 3:
                length = len(data) - start - 1
    return (
     offset, length)


def construct_packet(data, header_start):
    """Returns a (length, packet) tuple constructed from 'data' at index
    'header_start'. If there is a next packet, it will be found at
    header_start + length."""
    tag = data[header_start] & 63
    new = bool(data[header_start] & 64)
    if new:
        data_offset, data_length, partial = new_tag_length(data, header_start + 1)
    else:
        tag >>= 2
        data_offset, data_length = old_tag_length(data, header_start)
        partial = False
    name, PacketType = TAG_TYPES.get(tag, ('Unknown', None))
    if not PacketType:
        PacketType = Packet
    data_offset += 1
    consumed = 0
    packet_data = bytearray()
    original_data = bytearray()
    while True:
        consumed += data_offset
        data_start = header_start + data_offset
        next_header_start = data_start + data_length
        original_data += data[header_start:next_header_start]
        packet_data += data[data_start:next_header_start]
        consumed += data_length
        if partial:
            data_offset, data_length, partial = new_tag_length(data, next_header_start)
            header_start = next_header_start
        else:
            break

    packet = PacketType(tag, name, new, packet_data, original_data)
    return (consumed, packet)