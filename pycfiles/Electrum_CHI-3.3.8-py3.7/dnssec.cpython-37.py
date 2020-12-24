# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/dnssec.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 10281 bytes
import time, struct, dns.name, dns.query, dns.dnssec, dns.message, dns.resolver, dns.rdatatype, dns.rdtypes.ANY.NS, dns.rdtypes.ANY.CNAME, dns.rdtypes.ANY.DLV, dns.rdtypes.ANY.DNSKEY, dns.rdtypes.ANY.DS, dns.rdtypes.ANY.NSEC, dns.rdtypes.ANY.NSEC3, dns.rdtypes.ANY.NSEC3PARAM, dns.rdtypes.ANY.RRSIG, dns.rdtypes.ANY.SOA, dns.rdtypes.ANY.TXT, dns.rdtypes.IN.A, dns.rdtypes.IN.AAAA, ecdsa
from . import rsakey

def python_validate_rrsig(rrset, rrsig, keys, origin=None, now=None):
    from dns.dnssec import ValidationFailure, ECDSAP256SHA256, ECDSAP384SHA384
    from dns.dnssec import _find_candidate_keys, _make_hash, _is_ecdsa, _is_rsa, _to_rdata, _make_algorithm_id
    if isinstance(origin, str):
        origin = dns.name.from_text(origin, dns.name.root)
    for candidate_key in _find_candidate_keys(keys, rrsig):
        if not candidate_key:
            raise ValidationFailure('unknown key')
        else:
            if isinstance(rrset, tuple):
                rrname = rrset[0]
                rdataset = rrset[1]
            else:
                rrname = rrset.name
                rdataset = rrset
            if now is None:
                now = time.time()
            else:
                if rrsig.expiration < now:
                    raise ValidationFailure('expired')
                if rrsig.inception > now:
                    raise ValidationFailure('not yet valid')
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
                    n = ecdsa.util.string_to_number(rsa_n)
                    e = ecdsa.util.string_to_number(rsa_e)
                    pubkey = rsakey.RSAKey(n, e)
                    sig = rrsig.signature
                else:
                    if _is_ecdsa(rrsig.algorithm):
                        if rrsig.algorithm == ECDSAP256SHA256:
                            curve = ecdsa.curves.NIST256p
                            key_len = 32
                        else:
                            if rrsig.algorithm == ECDSAP384SHA384:
                                curve = ecdsa.curves.NIST384p
                                key_len = 48
                            else:
                                raise ValidationFailure('unknown ECDSA curve')
                        keyptr = candidate_key.key
                        x = ecdsa.util.string_to_number(keyptr[0:key_len])
                        y = ecdsa.util.string_to_number(keyptr[key_len:key_len * 2])
                        assert ecdsa.ecdsa.point_is_valid(curve.generator, x, y)
                        point = ecdsa.ellipticcurve.Point(curve.curve, x, y, curve.order)
                        verifying_key = ecdsa.keys.VerifyingKey.from_public_point(point, curve)
                        r = rrsig.signature[:key_len]
                        s = rrsig.signature[key_len:]
                        sig = ecdsa.ecdsa.Signature(ecdsa.util.string_to_number(r), ecdsa.util.string_to_number(s))
                    else:
                        raise ValidationFailure('unknown algorithm %u' % rrsig.algorithm)
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
            if pubkey.verify(bytearray(sig), bytearray(digest)):
                return
        elif _is_ecdsa(rrsig.algorithm):
            diglong = ecdsa.util.string_to_number(digest)
            if verifying_key.pubkey.verifies(diglong, sig):
                return
        else:
            raise ValidationFailure('unknown algorithm %s' % rrsig.algorithm)

    raise ValidationFailure('verify failure')


dns.dnssec._validate_rrsig = python_validate_rrsig
dns.dnssec.validate_rrsig = python_validate_rrsig
dns.dnssec.validate = dns.dnssec._validate
from .logging import get_logger
_logger = get_logger(__name__)
trust_anchors = [
 dns.rrset.from_text('.', 1, 'IN', 'DNSKEY', '257 3 8 AwEAAaz/tAm8yTn4Mfeh5eyI96WSVexTBAvkMgJzkKTOiW1vkIbzxeF3+/4RgWOq7HrxRixHlFlExOLAJr5emLvN7SWXgnLh4+B5xQlNVz8Og8kvArMtNROxVQuCaSnIDdD5LKyWbRd2n9WGe2R8PzgCmr3EgVLrjyBxWezF0jLHwVN8efS3rCj/EWgvIWgb9tarpVUDK/b58Da+sqqls3eNbuv7pr+eoZG+SrDK6nWeL3c6H5Apxz7LjVc1uTIdsIXxuOLYA4/ilBmSVIzuDWfdRUfhHdY6+cn8HFRm+2hM8AnXGXws9555KrUB5qihylGa8subX2Nn6UwNR1AkUTV74bU='),
 dns.rrset.from_text('.', 15202, 'IN', 'DNSKEY', '257 3 8 AwEAAagAIKlVZrpC6Ia7gEzahOR+9W29euxhJhVVLOyQbSEW0O8gcCjF FVQUTf6v58fLjwBd0YI0EzrAcQqBGCzh/RStIoO8g0NfnfL2MTJRkxoX bfDaUeVPQuYEhg37NZWAJQ9VnMVDxP/VHL496M/QZxkjf5/Efucp2gaD X6RS6CXpoY68LsvPVjR0ZSwzz1apAzvN9dlzEheX7ICJBBtuA6G3LQpz W5hOA2hzCTMjJPJ8LbqF6dsV6DoBQzgul0sGIcGOYl7OyQdXfZ57relS Qageu+ipAdTTJ25AsRTAoub8ONGcLmqrAmRLKBP1dfwhYB4N7knNnulq QxA+Uk1ihz0=')]

def check_query(ns, sub, _type, keys):
    q = dns.message.make_query(sub, _type, want_dnssec=True)
    response = dns.query.tcp(q, ns, timeout=5)
    if not response.rcode() == 0:
        raise AssertionError('No answer')
    else:
        answer = response.answer
        if not len(answer) != 0:
            raise AssertionError(('No DNS record found', sub, _type))
        else:
            assert len(answer) != 1, ('No DNSSEC record found', sub, _type)
            if answer[0].rdtype == dns.rdatatype.RRSIG:
                rrsig, rrset = answer
            else:
                if answer[1].rdtype == dns.rdatatype.RRSIG:
                    rrset, rrsig = answer
                else:
                    raise Exception('No signature set in record')
    if keys is None:
        keys = {dns.name.from_text(sub): rrset}
    dns.dnssec.validate(rrset, rrsig, keys)
    return rrset


def get_and_validate(ns, url, _type):
    root_rrset = None
    for dnskey_rr in trust_anchors:
        try:
            root_rrset = check_query(ns, '', dns.rdatatype.DNSKEY, {dns.name.root: dnskey_rr})
            break
        except dns.dnssec.ValidationFailure:
            continue

    if not root_rrset:
        raise dns.dnssec.ValidationFailure('None of the trust anchors found in DNS')
    keys = {dns.name.root: root_rrset}
    parts = url.split('.')
    for i in range(len(parts), 0, -1):
        sub = '.'.join(parts[i - 1:])
        name = dns.name.from_text(sub)
        query = dns.message.make_query(sub, dns.rdatatype.NS)
        response = dns.query.udp(query, ns, 3)
        assert response.rcode() == dns.rcode.NOERROR, 'query error'
        rrset = response.authority[0] if len(response.authority) > 0 else response.answer[0]
        rr = rrset[0]
        if rr.rdtype == dns.rdatatype.SOA:
            continue
        rrset = check_query(ns, sub, dns.rdatatype.DNSKEY, None)
        ds_rrset = check_query(ns, sub, dns.rdatatype.DS, keys)
        for ds in ds_rrset:
            for dnskey in rrset:
                htype = 'SHA256' if ds.digest_type == 2 else 'SHA1'
                good_ds = dns.dnssec.make_ds(name, dnskey, htype)
                if ds == good_ds:
                    break
            else:
                continue

            break
        else:
            raise Exception('DS does not match DNSKEY')

        keys = {name: rrset}

    rrset = check_query(ns, url, _type, keys)
    return rrset


def query(url, rtype):
    nameservers = [
     '8.8.8.8']
    ns = nameservers[0]
    try:
        out = get_and_validate(ns, url, rtype)
        validated = True
    except BaseException as e:
        try:
            _logger.info(f"DNSSEC error: {repr(e)}")
            resolver = dns.resolver.get_default_resolver()
            out = resolver.query(url, rtype)
            validated = False
        finally:
            e = None
            del e

    return (
     out, validated)