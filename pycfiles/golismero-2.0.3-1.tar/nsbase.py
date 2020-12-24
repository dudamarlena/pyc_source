# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/dns/rdtypes/nsbase.py
# Compiled at: 2013-08-26 10:52:44
"""NS-like base classes."""
import cStringIO, dns.exception, dns.rdata, dns.name

class NSBase(dns.rdata.Rdata):
    """Base class for rdata that is like an NS record.

    @ivar target: the target name of the rdata
    @type target: dns.name.Name object"""
    __slots__ = [
     'target']

    def __init__(self, rdclass, rdtype, target):
        super(NSBase, self).__init__(rdclass, rdtype)
        self.target = target

    def to_text(self, origin=None, relativize=True, **kw):
        target = self.target.choose_relativity(origin, relativize)
        return str(target)

    def from_text(cls, rdclass, rdtype, tok, origin=None, relativize=True):
        target = tok.get_name()
        target = target.choose_relativity(origin, relativize)
        tok.get_eol()
        return cls(rdclass, rdtype, target)

    from_text = classmethod(from_text)

    def to_wire(self, file, compress=None, origin=None):
        self.target.to_wire(file, compress, origin)

    def to_digestable(self, origin=None):
        return self.target.to_digestable(origin)

    def from_wire(cls, rdclass, rdtype, wire, current, rdlen, origin=None):
        target, cused = dns.name.from_wire(wire[:current + rdlen], current)
        if cused != rdlen:
            raise dns.exception.FormError
        if origin is not None:
            target = target.relativize(origin)
        return cls(rdclass, rdtype, target)

    from_wire = classmethod(from_wire)

    def choose_relativity(self, origin=None, relativize=True):
        self.target = self.target.choose_relativity(origin, relativize)

    def _cmp(self, other):
        return cmp(self.target, other.target)


class UncompressedNS(NSBase):
    """Base class for rdata that is like an NS record, but whose name
    is not compressed when convert to DNS wire format, and whose
    digestable form is not downcased."""

    def to_wire(self, file, compress=None, origin=None):
        super(UncompressedNS, self).to_wire(file, None, origin)
        return

    def to_digestable(self, origin=None):
        f = cStringIO.StringIO()
        self.to_wire(f, None, origin)
        return f.getvalue()