# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/dns/rdtypes/dsbase.py
# Compiled at: 2013-08-26 10:52:44
import struct, dns.rdata, dns.rdatatype

class DSBase(dns.rdata.Rdata):
    """Base class for rdata that is like a DS record

    @ivar key_tag: the key tag
    @type key_tag: int
    @ivar algorithm: the algorithm
    @type algorithm: int
    @ivar digest_type: the digest type
    @type digest_type: int
    @ivar digest: the digest
    @type digest: int
    @see: draft-ietf-dnsext-delegation-signer-14.txt"""
    __slots__ = [
     'key_tag', 'algorithm', 'digest_type', 'digest']

    def __init__(self, rdclass, rdtype, key_tag, algorithm, digest_type, digest):
        super(DSBase, self).__init__(rdclass, rdtype)
        self.key_tag = key_tag
        self.algorithm = algorithm
        self.digest_type = digest_type
        self.digest = digest

    def to_text(self, origin=None, relativize=True, **kw):
        return '%d %d %d %s' % (self.key_tag, self.algorithm,
         self.digest_type,
         dns.rdata._hexify(self.digest, chunksize=128))

    def from_text(cls, rdclass, rdtype, tok, origin=None, relativize=True):
        key_tag = tok.get_uint16()
        algorithm = tok.get_uint8()
        digest_type = tok.get_uint8()
        chunks = []
        while 1:
            t = tok.get().unescape()
            if t.is_eol_or_eof():
                break
            if not t.is_identifier():
                raise dns.exception.SyntaxError
            chunks.append(t.value)

        digest = ('').join(chunks)
        digest = digest.decode('hex_codec')
        return cls(rdclass, rdtype, key_tag, algorithm, digest_type, digest)

    from_text = classmethod(from_text)

    def to_wire(self, file, compress=None, origin=None):
        header = struct.pack('!HBB', self.key_tag, self.algorithm, self.digest_type)
        file.write(header)
        file.write(self.digest)

    def from_wire(cls, rdclass, rdtype, wire, current, rdlen, origin=None):
        header = struct.unpack('!HBB', wire[current:current + 4])
        current += 4
        rdlen -= 4
        digest = wire[current:current + rdlen].unwrap()
        return cls(rdclass, rdtype, header[0], header[1], header[2], digest)

    from_wire = classmethod(from_wire)

    def _cmp(self, other):
        hs = struct.pack('!HBB', self.key_tag, self.algorithm, self.digest_type)
        ho = struct.pack('!HBB', other.key_tag, other.algorithm, other.digest_type)
        v = cmp(hs, ho)
        if v == 0:
            v = cmp(self.digest, other.digest)
        return v