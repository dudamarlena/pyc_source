# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/dns/rdtypes/ANY/NSEC.py
# Compiled at: 2013-08-26 10:52:44
import cStringIO, dns.exception, dns.rdata, dns.rdatatype, dns.name

class NSEC(dns.rdata.Rdata):
    """NSEC record

    @ivar next: the next name
    @type next: dns.name.Name object
    @ivar windows: the windowed bitmap list
    @type windows: list of (window number, string) tuples"""
    __slots__ = [
     'next', 'windows']

    def __init__(self, rdclass, rdtype, next, windows):
        super(NSEC, self).__init__(rdclass, rdtype)
        self.next = next
        self.windows = windows

    def to_text(self, origin=None, relativize=True, **kw):
        next = self.next.choose_relativity(origin, relativize)
        text = ''
        for window, bitmap in self.windows:
            bits = []
            for i in xrange(0, len(bitmap)):
                byte = ord(bitmap[i])
                for j in xrange(0, 8):
                    if byte & 128 >> j:
                        bits.append(dns.rdatatype.to_text(window * 256 + i * 8 + j))

            text += ' ' + (' ').join(bits)

        return '%s%s' % (next, text)

    def from_text(cls, rdclass, rdtype, tok, origin=None, relativize=True):
        next = tok.get_name()
        next = next.choose_relativity(origin, relativize)
        rdtypes = []
        while 1:
            token = tok.get().unescape()
            if token.is_eol_or_eof():
                break
            nrdtype = dns.rdatatype.from_text(token.value)
            if nrdtype == 0:
                raise dns.exception.SyntaxError('NSEC with bit 0')
            if nrdtype > 65535:
                raise dns.exception.SyntaxError('NSEC with bit > 65535')
            rdtypes.append(nrdtype)

        rdtypes.sort()
        window = 0
        octets = 0
        prior_rdtype = 0
        bitmap = ['\x00'] * 32
        windows = []
        for nrdtype in rdtypes:
            if nrdtype == prior_rdtype:
                continue
            prior_rdtype = nrdtype
            new_window = nrdtype // 256
            if new_window != window:
                windows.append((window, ('').join(bitmap[0:octets])))
                bitmap = ['\x00'] * 32
                window = new_window
            offset = nrdtype % 256
            byte = offset // 8
            bit = offset % 8
            octets = byte + 1
            bitmap[byte] = chr(ord(bitmap[byte]) | 128 >> bit)

        windows.append((window, ('').join(bitmap[0:octets])))
        return cls(rdclass, rdtype, next, windows)

    from_text = classmethod(from_text)

    def to_wire(self, file, compress=None, origin=None):
        self.next.to_wire(file, None, origin)
        for window, bitmap in self.windows:
            file.write(chr(window))
            file.write(chr(len(bitmap)))
            file.write(bitmap)

        return

    def from_wire(cls, rdclass, rdtype, wire, current, rdlen, origin=None):
        next, cused = dns.name.from_wire(wire[:current + rdlen], current)
        current += cused
        rdlen -= cused
        windows = []
        while rdlen > 0:
            if rdlen < 3:
                raise dns.exception.FormError('NSEC too short')
            window = ord(wire[current])
            octets = ord(wire[(current + 1)])
            if octets == 0 or octets > 32:
                raise dns.exception.FormError('bad NSEC octets')
            current += 2
            rdlen -= 2
            if rdlen < octets:
                raise dns.exception.FormError('bad NSEC bitmap length')
            bitmap = wire[current:current + octets].unwrap()
            current += octets
            rdlen -= octets
            windows.append((window, bitmap))

        if origin is not None:
            next = next.relativize(origin)
        return cls(rdclass, rdtype, next, windows)

    from_wire = classmethod(from_wire)

    def choose_relativity(self, origin=None, relativize=True):
        self.next = self.next.choose_relativity(origin, relativize)

    def _cmp(self, other):
        return self._wire_cmp(other)