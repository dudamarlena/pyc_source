# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/dns/dnssec.py
# Compiled at: 2013-08-26 10:52:44
"""Common DNSSEC-related functions and constants."""
import cStringIO, struct, time, dns.exception, dns.hash, dns.name, dns.node, dns.rdataset, dns.rdata, dns.rdatatype, dns.rdataclass

class UnsupportedAlgorithm(dns.exception.DNSException):
    """Raised if an algorithm is not supported."""
    pass


class ValidationFailure(dns.exception.DNSException):
    """The DNSSEC signature is invalid."""
    pass


RSAMD5 = 1
DH = 2
DSA = 3
ECC = 4
RSASHA1 = 5
DSANSEC3SHA1 = 6
RSASHA1NSEC3SHA1 = 7
RSASHA256 = 8
RSASHA512 = 10
INDIRECT = 252
PRIVATEDNS = 253
PRIVATEOID = 254
_algorithm_by_text = {'RSAMD5': RSAMD5, 
   'DH': DH, 
   'DSA': DSA, 
   'ECC': ECC, 
   'RSASHA1': RSASHA1, 
   'DSANSEC3SHA1': DSANSEC3SHA1, 
   'RSASHA1NSEC3SHA1': RSASHA1NSEC3SHA1, 
   'RSASHA256': RSASHA256, 
   'RSASHA512': RSASHA512, 
   'INDIRECT': INDIRECT, 
   'PRIVATEDNS': PRIVATEDNS, 
   'PRIVATEOID': PRIVATEOID}
_algorithm_by_value = dict([ (y, x) for x, y in _algorithm_by_text.iteritems() ])

def algorithm_from_text(text):
    """Convert text into a DNSSEC algorithm value
    @rtype: int"""
    value = _algorithm_by_text.get(text.upper())
    if value is None:
        value = int(text)
    return value


def algorithm_to_text(value):
    """Convert a DNSSEC algorithm value to text
    @rtype: string"""
    text = _algorithm_by_value.get(value)
    if text is None:
        text = str(value)
    return text


def _to_rdata(record, origin):
    s = cStringIO.StringIO()
    record.to_wire(s, origin=origin)
    return s.getvalue()


def key_id(key, origin=None):
    rdata = _to_rdata(key, origin)
    if key.algorithm == RSAMD5:
        return (ord(rdata[(-3)]) << 8) + ord(rdata[(-2)])
    else:
        total = 0
        for i in range(len(rdata) // 2):
            total += (ord(rdata[(2 * i)]) << 8) + ord(rdata[(2 * i + 1)])

        if len(rdata) % 2 != 0:
            total += ord(rdata[(len(rdata) - 1)]) << 8
        total += total >> 16 & 65535
        return total & 65535


def make_ds(name, key, algorithm, origin=None):
    if algorithm.upper() == 'SHA1':
        dsalg = 1
        hash = dns.hash.get('SHA1')()
    elif algorithm.upper() == 'SHA256':
        dsalg = 2
        hash = dns.hash.get('SHA256')()
    else:
        raise UnsupportedAlgorithm, 'unsupported algorithm "%s"' % algorithm
    if isinstance(name, (str, unicode)):
        name = dns.name.from_text(name, origin)
    hash.update(name.canonicalize().to_wire())
    hash.update(_to_rdata(key, origin))
    digest = hash.digest()
    dsrdata = struct.pack('!HBB', key_id(key), key.algorithm, dsalg) + digest
    return dns.rdata.from_wire(dns.rdataclass.IN, dns.rdatatype.DS, dsrdata, 0, len(dsrdata))


def _find_candidate_keys(keys, rrsig):
    candidate_keys = []
    value = keys.get(rrsig.signer)
    if value is None:
        return
    else:
        if isinstance(value, dns.node.Node):
            try:
                rdataset = node.find_rdataset(dns.rdataclass.IN, dns.rdatatype.DNSKEY)
            except KeyError:
                return

        else:
            rdataset = value
        for rdata in rdataset:
            if rdata.algorithm == rrsig.algorithm and key_id(rdata) == rrsig.key_tag:
                candidate_keys.append(rdata)

        return candidate_keys


def _is_rsa(algorithm):
    return algorithm in (RSAMD5, RSASHA1,
     RSASHA1NSEC3SHA1, RSASHA256,
     RSASHA512)


def _is_dsa(algorithm):
    return algorithm in (DSA, DSANSEC3SHA1)


def _is_md5(algorithm):
    return algorithm == RSAMD5


def _is_sha1(algorithm):
    return algorithm in (DSA, RSASHA1,
     DSANSEC3SHA1, RSASHA1NSEC3SHA1)


def _is_sha256(algorithm):
    return algorithm == RSASHA256


def _is_sha512(algorithm):
    return algorithm == RSASHA512


def _make_hash(algorithm):
    if _is_md5(algorithm):
        return dns.hash.get('MD5')()
    if _is_sha1(algorithm):
        return dns.hash.get('SHA1')()
    if _is_sha256(algorithm):
        return dns.hash.get('SHA256')()
    if _is_sha512(algorithm):
        return dns.hash.get('SHA512')()
    raise ValidationFailure, 'unknown hash for algorithm %u' % algorithm


def _make_algorithm_id(algorithm):
    if _is_md5(algorithm):
        oid = [
         42, 134, 72, 134, 247, 13, 2, 5]
    elif _is_sha1(algorithm):
        oid = [
         43, 14, 3, 2, 26]
    elif _is_sha256(algorithm):
        oid = [
         96, 134, 72, 1, 101, 3, 4, 2, 1]
    elif _is_sha512(algorithm):
        oid = [
         96, 134, 72, 1, 101, 3, 4, 2, 3]
    else:
        raise ValidationFailure, 'unknown algorithm %u' % algorithm
    olen = len(oid)
    dlen = _make_hash(algorithm).digest_size
    idbytes = [
     48] + [8 + olen + dlen] + [48, olen + 4] + [6, olen] + oid + [5, 0] + [4, dlen]
    return ('').join(map(chr, idbytes))


def _validate_rrsig(rrset, rrsig, keys, origin=None, now=None):
    """Validate an RRset against a single signature rdata

    The owner name of the rrsig is assumed to be the same as the owner name
    of the rrset.

    @param rrset: The RRset to validate
    @type rrset: dns.rrset.RRset or (dns.name.Name, dns.rdataset.Rdataset)
    tuple
    @param rrsig: The signature rdata
    @type rrsig: dns.rrset.Rdata
    @param keys: The key dictionary.
    @type keys: a dictionary keyed by dns.name.Name with node or rdataset values
    @param origin: The origin to use for relative names
    @type origin: dns.name.Name or None
    @param now: The time to use when validating the signatures.  The default
    is the current time.
    @type now: int
    """
    if isinstance(origin, (str, unicode)):
        origin = dns.name.from_text(origin, dns.name.root)
    for candidate_key in _find_candidate_keys(keys, rrsig):
        if not candidate_key:
            raise ValidationFailure, 'unknown key'
        if isinstance(rrset, tuple):
            rrname = rrset[0]
            rdataset = rrset[1]
        else:
            rrname = rrset.name
            rdataset = rrset
        if now is None:
            now = time.time()
        if rrsig.expiration < now:
            raise ValidationFailure, 'expired'
        if rrsig.inception > now:
            raise ValidationFailure, 'not yet valid'
        hash = _make_hash(rrsig.algorithm)
        if _is_rsa(rrsig.algorithm):
            keyptr = candidate_key.key
            bytes, = struct.unpack('!B', keyptr[0:1])
            keyptr = keyptr[1:]
            if bytes == 0:
                bytes, = struct.unpack('!H', keyptr[0:2])
                keyptr = keyptr[2:]
            rsa_e = keyptr[0:bytes]
            rsa_n = keyptr[bytes:]
            keylen = len(rsa_n) * 8
            pubkey = Crypto.PublicKey.RSA.construct((
             Crypto.Util.number.bytes_to_long(rsa_n),
             Crypto.Util.number.bytes_to_long(rsa_e)))
            sig = (Crypto.Util.number.bytes_to_long(rrsig.signature),)
        else:
            if _is_dsa(rrsig.algorithm):
                keyptr = candidate_key.key
                t, = struct.unpack('!B', keyptr[0:1])
                keyptr = keyptr[1:]
                octets = 64 + t * 8
                dsa_q = keyptr[0:20]
                keyptr = keyptr[20:]
                dsa_p = keyptr[0:octets]
                keyptr = keyptr[octets:]
                dsa_g = keyptr[0:octets]
                keyptr = keyptr[octets:]
                dsa_y = keyptr[0:octets]
                pubkey = Crypto.PublicKey.DSA.construct((
                 Crypto.Util.number.bytes_to_long(dsa_y),
                 Crypto.Util.number.bytes_to_long(dsa_g),
                 Crypto.Util.number.bytes_to_long(dsa_p),
                 Crypto.Util.number.bytes_to_long(dsa_q)))
                dsa_r, dsa_s = struct.unpack('!20s20s', rrsig.signature[1:])
                sig = (Crypto.Util.number.bytes_to_long(dsa_r),
                 Crypto.Util.number.bytes_to_long(dsa_s))
            else:
                raise ValidationFailure, 'unknown algorithm %u' % rrsig.algorithm
            hash.update(_to_rdata(rrsig, origin)[:18])
            hash.update(rrsig.signer.to_digestable(origin))
            if rrsig.labels < len(rrname) - 1:
                suffix = rrname.split(rrsig.labels + 1)[1]
                rrname = dns.name.from_text('*', suffix)
            rrnamebuf = rrname.to_digestable(origin)
            rrfixed = struct.pack('!HHI', rdataset.rdtype, rdataset.rdclass, rrsig.original_ttl)
            rrlist = sorted(rdataset)
            for rr in rrlist:
                hash.update(rrnamebuf)
                hash.update(rrfixed)
                rrdata = rr.to_digestable(origin)
                rrlen = struct.pack('!H', len(rrdata))
                hash.update(rrlen)
                hash.update(rrdata)

            digest = hash.digest()
            if _is_rsa(rrsig.algorithm):
                digest = _make_algorithm_id(rrsig.algorithm) + digest
                padlen = keylen // 8 - len(digest) - 3
                digest = chr(0) + chr(1) + chr(255) * padlen + chr(0) + digest
            elif _is_dsa(rrsig.algorithm):
                pass
            else:
                raise ValidationFailure, 'unknown algorithm %u' % rrsig.algorithm
            if pubkey.verify(digest, sig):
                return

    raise ValidationFailure, 'verify failure'
    return


def _validate(rrset, rrsigset, keys, origin=None, now=None):
    """Validate an RRset

    @param rrset: The RRset to validate
    @type rrset: dns.rrset.RRset or (dns.name.Name, dns.rdataset.Rdataset)
    tuple
    @param rrsigset: The signature RRset
    @type rrsigset: dns.rrset.RRset or (dns.name.Name, dns.rdataset.Rdataset)
    tuple
    @param keys: The key dictionary.
    @type keys: a dictionary keyed by dns.name.Name with node or rdataset values
    @param origin: The origin to use for relative names
    @type origin: dns.name.Name or None
    @param now: The time to use when validating the signatures.  The default
    is the current time.
    @type now: int
    """
    if isinstance(origin, (str, unicode)):
        origin = dns.name.from_text(origin, dns.name.root)
    if isinstance(rrset, tuple):
        rrname = rrset[0]
    else:
        rrname = rrset.name
    if isinstance(rrsigset, tuple):
        rrsigname = rrsigset[0]
        rrsigrdataset = rrsigset[1]
    else:
        rrsigname = rrsigset.name
        rrsigrdataset = rrsigset
    rrname = rrname.choose_relativity(origin)
    rrsigname = rrname.choose_relativity(origin)
    if rrname != rrsigname:
        raise ValidationFailure, 'owner names do not match'
    for rrsig in rrsigrdataset:
        try:
            _validate_rrsig(rrset, rrsig, keys, origin, now)
            return
        except ValidationFailure as e:
            pass

    raise ValidationFailure, 'no RRSIGs validated'


def _need_pycrypto(*args, **kwargs):
    raise NotImplementedError, 'DNSSEC validation requires pycrypto'


try:
    import Crypto.PublicKey.RSA, Crypto.PublicKey.DSA, Crypto.Util.number
    validate = _validate
    validate_rrsig = _validate_rrsig
except ImportError:
    validate = _need_pycrypto
    validate_rrsig = _need_pycrypto