# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/x509.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 11467 bytes
import hashlib, time
from datetime import datetime
import ecdsa
from . import util
from .util import profiler, bh2u
from .logging import get_logger
_logger = get_logger(__name__)
ALGO_RSA_SHA1 = '1.2.840.113549.1.1.5'
ALGO_RSA_SHA256 = '1.2.840.113549.1.1.11'
ALGO_RSA_SHA384 = '1.2.840.113549.1.1.12'
ALGO_RSA_SHA512 = '1.2.840.113549.1.1.13'
ALGO_ECDSA_SHA256 = '1.2.840.10045.4.3.2'
PREFIX_RSA_SHA256 = bytearray([
 48, 49, 48, 13, 6, 9, 96, 134, 72, 1, 101, 3, 4, 2, 1, 5, 0, 4, 32])
PREFIX_RSA_SHA384 = bytearray([
 48, 65, 48, 13, 6, 9, 96, 134, 72, 1, 101, 3, 4, 2, 2, 5, 0, 4, 48])
PREFIX_RSA_SHA512 = bytearray([
 48, 81, 48, 13, 6, 9, 96, 134, 72, 1, 101, 3, 4, 2, 3, 5, 0, 4, 64])
ASN1_TYPES = {'BOOLEAN':1, 
 'INTEGER':2, 
 'BIT STRING':3, 
 'OCTET STRING':4, 
 'NULL':5, 
 'OBJECT IDENTIFIER':6, 
 'SEQUENCE':112, 
 'SET':113, 
 'PrintableString':19, 
 'IA5String':22, 
 'UTCTime':23, 
 'GeneralizedTime':24, 
 'ENUMERATED':10, 
 'UTF8String':12}

class CertificateError(Exception):
    pass


def bitstr_to_bytestr(s):
    if s[0] != 0:
        raise TypeError('no padding')
    return s[1:]


def bytestr_to_int(s):
    i = 0
    for char in s:
        i <<= 8
        i |= char

    return i


def decode_OID(s):
    r = []
    r.append(s[0] // 40)
    r.append(s[0] % 40)
    k = 0
    for i in s[1:]:
        if i < 128:
            r.append(i + 128 * k)
            k = 0
        else:
            k = i - 128 + 128 * k

    return '.'.join(map(str, r))


def encode_OID(oid):
    x = [int(i) for i in oid.split('.')]
    s = chr(x[0] * 40 + x[1])
    for i in x[2:]:
        ss = chr(i % 128)
        while i > 128:
            i //= 128
            ss = chr(128 + i % 128) + ss

        s += ss

    return s


class ASN1_Node(bytes):

    def get_node(self, ix):
        first = self[(ix + 1)]
        if first & 128 == 0:
            length = first
            ixf = ix + 2
            ixl = ixf + length - 1
        else:
            lengthbytes = first & 127
            length = bytestr_to_int(self[ix + 2:ix + 2 + lengthbytes])
            ixf = ix + 2 + lengthbytes
            ixl = ixf + length - 1
        return (
         ix, ixf, ixl)

    def root(self):
        return self.get_node(0)

    def next_node(self, node):
        ixs, ixf, ixl = node
        return self.get_node(ixl + 1)

    def first_child(self, node):
        ixs, ixf, ixl = node
        if self[ixs] & 32 != 32:
            raise TypeError('Can only open constructed types.', hex(self[ixs]))
        return self.get_node(ixf)

    def is_child_of(node1, node2):
        ixs, ixf, ixl = node1
        jxs, jxf, jxl = node2
        return ixf <= jxs and jxl <= ixl or jxf <= ixs and ixl <= jxl

    def get_all(self, node):
        ixs, ixf, ixl = node
        return self[ixs:ixl + 1]

    def get_value_of_type(self, node, asn1_type):
        ixs, ixf, ixl = node
        if ASN1_TYPES[asn1_type] != self[ixs]:
            raise TypeError('Wrong type:', hex(self[ixs]), hex(ASN1_TYPES[asn1_type]))
        return self[ixf:ixl + 1]

    def get_value(self, node):
        ixs, ixf, ixl = node
        return self[ixf:ixl + 1]

    def get_children(self, node):
        nodes = []
        ii = self.first_child(node)
        nodes.append(ii)
        while ii[2] < node[2]:
            ii = self.next_node(ii)
            nodes.append(ii)

        return nodes

    def get_sequence(self):
        return list(map(lambda j: self.get_value(j), self.get_children(self.root())))

    def get_dict(self, node):
        p = {}
        for ii in self.get_children(node):
            for iii in self.get_children(ii):
                iiii = self.first_child(iii)
                oid = decode_OID(self.get_value_of_type(iiii, 'OBJECT IDENTIFIER'))
                iiii = self.next_node(iiii)
                value = self.get_value(iiii)
                p[oid] = value

        return p

    def decode_time(self, ii):
        GENERALIZED_TIMESTAMP_FMT = '%Y%m%d%H%M%SZ'
        UTCTIME_TIMESTAMP_FMT = '%y%m%d%H%M%SZ'
        try:
            return time.strptime(self.get_value_of_type(ii, 'UTCTime').decode('ascii'), UTCTIME_TIMESTAMP_FMT)
        except TypeError:
            return time.strptime(self.get_value_of_type(ii, 'GeneralizedTime').decode('ascii'), GENERALIZED_TIMESTAMP_FMT)


class X509(object):

    def __init__(self, b):
        self.bytes = bytearray(b)
        der = ASN1_Node(b)
        root = der.root()
        cert = der.first_child(root)
        self.data = der.get_all(cert)
        if der.get_value(cert)[0] == 160:
            version = der.first_child(cert)
            serial_number = der.next_node(version)
        else:
            serial_number = der.first_child(cert)
        self.serial_number = bytestr_to_int(der.get_value_of_type(serial_number, 'INTEGER'))
        sig_algo = der.next_node(serial_number)
        ii = der.first_child(sig_algo)
        self.sig_algo = decode_OID(der.get_value_of_type(ii, 'OBJECT IDENTIFIER'))
        issuer = der.next_node(sig_algo)
        self.issuer = der.get_dict(issuer)
        validity = der.next_node(issuer)
        ii = der.first_child(validity)
        self.notBefore = der.decode_time(ii)
        ii = der.next_node(ii)
        self.notAfter = der.decode_time(ii)
        subject = der.next_node(validity)
        self.subject = der.get_dict(subject)
        subject_pki = der.next_node(subject)
        public_key_algo = der.first_child(subject_pki)
        ii = der.first_child(public_key_algo)
        self.public_key_algo = decode_OID(der.get_value_of_type(ii, 'OBJECT IDENTIFIER'))
        if self.public_key_algo != '1.2.840.10045.2.1':
            subject_public_key = der.next_node(public_key_algo)
            spk = der.get_value_of_type(subject_public_key, 'BIT STRING')
            spk = ASN1_Node(bitstr_to_bytestr(spk))
            r = spk.root()
            modulus = spk.first_child(r)
            exponent = spk.next_node(modulus)
            rsa_n = spk.get_value_of_type(modulus, 'INTEGER')
            rsa_e = spk.get_value_of_type(exponent, 'INTEGER')
            self.modulus = ecdsa.util.string_to_number(rsa_n)
            self.exponent = ecdsa.util.string_to_number(rsa_e)
        else:
            subject_public_key = der.next_node(public_key_algo)
            spk = der.get_value_of_type(subject_public_key, 'BIT STRING')
            self.ec_public_key = spk
        self.CA = False
        self.AKI = None
        self.SKI = None
        i = subject_pki
        while i[2] < cert[2]:
            i = der.next_node(i)
            d = der.get_dict(i)
            for oid, value in d.items():
                value = ASN1_Node(value)
                if oid == '2.5.29.19':
                    self.CA = bool(value)
                elif oid == '2.5.29.14':
                    r = value.root()
                    value = value.get_value_of_type(r, 'OCTET STRING')
                    self.SKI = bh2u(value)
                elif oid == '2.5.29.35':
                    self.AKI = bh2u(value.get_sequence()[0])
                    continue

        cert_sig_algo = der.next_node(cert)
        ii = der.first_child(cert_sig_algo)
        self.cert_sig_algo = decode_OID(der.get_value_of_type(ii, 'OBJECT IDENTIFIER'))
        cert_sig = der.next_node(cert_sig_algo)
        self.signature = der.get_value(cert_sig)[1:]

    def get_keyID(self):
        if self.SKI:
            return self.SKI
        return repr(self.subject)

    def get_issuer_keyID(self):
        if self.AKI:
            return self.AKI
        return repr(self.issuer)

    def get_common_name(self):
        return self.subject.get('2.5.4.3', b'unknown').decode()

    def get_signature(self):
        return (
         self.cert_sig_algo, self.signature, self.data)

    def check_ca(self):
        return self.CA

    def check_date(self):
        now = time.gmtime()
        if self.notBefore > now:
            raise CertificateError('Certificate has not entered its valid date range. (%s)' % self.get_common_name())
        if self.notAfter <= now:
            dt = datetime.utcfromtimestamp(time.mktime(self.notAfter))
            raise CertificateError(f"Certificate ({self.get_common_name()}) has expired (at {dt} UTC).")

    def getFingerprint(self):
        return hashlib.sha1(self.bytes).digest()


@profiler
def load_certificates(ca_path):
    from . import pem
    ca_list = {}
    ca_keyID = {}
    with open(ca_path, 'r', encoding='utf-8') as (f):
        s = f.read()
    bList = pem.dePemList(s, 'CERTIFICATE')
    for b in bList:
        try:
            x = X509(b)
            x.check_date()
        except BaseException as e:
            try:
                _logger.info(f"cert error: {e}")
                continue
            finally:
                e = None
                del e

        fp = x.getFingerprint()
        ca_list[fp] = x
        ca_keyID[x.get_keyID()] = fp

    return (ca_list, ca_keyID)


if __name__ == '__main__':
    import certifi
    ca_path = certifi.where()
    ca_list, ca_keyID = load_certificates(ca_path)