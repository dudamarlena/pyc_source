# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\protocols\DNS.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 26663 bytes
import enum, io, asyncio, ipaddress, socket

class DNSResponseCode(enum.Enum):
    NOERR = 0
    FORMATERR = 1
    SERVERERR = 2
    NAMEERR = 3
    NOTIMPL = 4
    REFUSED = 5
    RESERVED6 = 6
    RESERVED7 = 7
    RESERVED8 = 8
    RESERVED9 = 9
    RESERVED10 = 10
    RESERVED11 = 11
    RESERVED12 = 12
    RESERVED13 = 13
    RESERVED14 = 14
    RESERVED15 = 15


class DNSType(enum.Enum):
    A = 1
    NS = 2
    MD = 3
    MF = 4
    CNAME = 5
    SOA = 6
    MB = 7
    MG = 8
    MR = 9
    NULL = 10
    WKS = 11
    PTR = 12
    HINFO = 13
    MINFO = 14
    MX = 15
    TXT = 16
    RP = 17
    AFSDB = 18
    SIG = 24
    KEY = 25
    AAAA = 28
    LOC = 29
    SRV = 33
    NAPTR = 35
    KX = 36
    CERT = 37
    DNAME = 39
    OPT = 41
    APL = 42
    DS = 43
    SSHFP = 44
    IPSECKEY = 45
    RRSIG = 46
    NSEC = 47
    DNSKEY = 48
    DHCID = 49
    NSEC3 = 50
    NSEC3PARAM = 51
    TLSA = 52
    HIP = 55
    CDS = 59
    CDNSKEY = 60
    OPENPGPKEY = 61
    TKEY = 249
    TSIG = 250
    IXFR = 251
    AXFR = 252
    ANY = 255
    URI = 256
    CAA = 257


class DNSClass(enum.Enum):
    IN = 1
    CS = 2
    CH = 3
    HS = 4
    ANY = 255


class DNSOpcode(enum.Enum):
    QUERY = 0
    IQUERY = 1
    STATUS = 2
    RESERVED3 = 3
    RESERVED4 = 4
    RESERVED5 = 5
    RESERVED6 = 6
    RESERVED7 = 7
    RESERVED8 = 8
    RESERVED9 = 9
    RESERVED10 = 10
    RESERVED11 = 11
    RESERVED12 = 12
    RESERVED13 = 13
    RESERVED14 = 14
    RESERVED15 = 15


class DNSFlags(enum.IntFlag):
    AA = 64
    TC = 32
    RD = 16
    RA = 8
    RESERVED1 = 4
    RESERVED2 = 2
    RESERVED3 = 1


class DNSResponse(enum.Enum):
    REQUEST = 0
    RESPONSE = 1


class DNSPacket:

    def __init__(self, proto=socket.SOCK_STREAM):
        self.proto = proto
        self.PACKETLEN = None
        self.TransactionID = None
        self.QR = None
        self.Opcode = None
        self.FLAGS = None
        self.Rcode = None
        self.QDCOUNT = None
        self.ANCOUNT = None
        self.NSCOUNT = None
        self.ARCOUNT = None
        self.Questions = []
        self.Answers = []
        self.Authorities = []
        self.Additionals = []

    async def from_streamreader(reader, proto=socket.SOCK_DGRAM):
        if proto == socket.SOCK_DGRAM:
            data = await reader.read()
            return DNSPacket.from_bytes(data)
        plen_bytes = await reader.readexactly(2)
        plen = int.from_bytes(plen_bytes, byteorder='big', signed=False)
        data = await reader.readexactly(plen)
        return DNSPacket.from_bytes((plen_bytes + data), proto=proto)

    def from_bytes(bbuff, proto=socket.SOCK_DGRAM):
        return DNSPacket.from_buffer(io.BytesIO(bbuff), proto)

    def from_buffer(buff, proto=socket.SOCK_DGRAM):
        packet = DNSPacket()
        packet.proto = proto
        if packet.proto == socket.SOCK_STREAM:
            packet.PACKETLEN = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
            buff = io.BytesIO(buff.read())
        packet.TransactionID = buff.read(2)
        temp = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        packet.QR = DNSResponse(temp >> 15)
        packet.Opcode = DNSOpcode((temp & 30720) >> 11)
        packet.FLAGS = DNSFlags(temp >> 4 & 127)
        packet.Rcode = DNSResponseCode(temp & 15)
        packet.QDCOUNT = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        packet.ANCOUNT = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        packet.NSCOUNT = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        packet.ARCOUNT = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        for i in range(0, packet.QDCOUNT):
            dnsq = DNSQuestion.from_buffer(buff)
            packet.Questions.append(dnsq)

        for i in range(0, packet.ANCOUNT):
            dnsr = DNSResourceParser.from_buffer(buff)
            packet.Answers.append(dnsr)

        for i in range(0, packet.NSCOUNT):
            dnsr = DNSResourceParser.from_buffer(buff)
            packet.Authorities.append(dnsr)

        for i in range(0, packet.ARCOUNT):
            dnsr = DNSResourceParser.from_buffer(buff)
            packet.Additionals.append(dnsr)

        return packet

    def __repr__(self):
        t = '== DNS Packet ==\r\n'
        t += 'TransactionID:  %s\r\n' % self.TransactionID.hex()
        t += 'QR:  %s\r\n' % self.QR.name
        t += 'Opcode: %s\r\n' % self.Opcode.name
        t += 'FLAGS: %s\r\n' % repr(self.FLAGS)
        t += 'Rcode: %s\r\n' % self.Rcode.name
        t += 'QDCOUNT: %s\r\n' % self.QDCOUNT
        t += 'ANCOUNT: %s\r\n' % self.ANCOUNT
        t += 'NSCOUNT: %s\r\n' % self.NSCOUNT
        t += 'ARCOUNT: %s\r\n' % self.ARCOUNT
        if len(self.Questions) > 0:
            for question in self.Questions:
                t += repr(question)

        if len(self.Answers) > 0:
            for answer in self.Answers:
                t += repr(answer)

        if len(self.Authorities) > 0:
            for answer in self.Authorities:
                t += repr(answer)

        if len(self.Additionals) > 0:
            for answer in self.Additionals:
                t += repr(answer)

        return t

    def to_bytes(self):
        t = self.TransactionID
        a = self.Rcode.value
        a |= self.FLAGS << 4 & 2032
        a |= self.Opcode.value << 11 & 30720
        a |= self.QR.value << 15 & 32768
        t += a.to_bytes(2, byteorder='big', signed=False)
        t += self.QDCOUNT.to_bytes(2, byteorder='big', signed=False)
        t += self.ANCOUNT.to_bytes(2, byteorder='big', signed=False)
        t += self.NSCOUNT.to_bytes(2, byteorder='big', signed=False)
        t += self.ARCOUNT.to_bytes(2, byteorder='big', signed=False)
        for q in self.Questions:
            t += q.to_bytes()

        for q in self.Answers:
            t += q.to_bytes()

        for q in self.Authorities:
            t += q.to_bytes()

        for q in self.Additionals:
            t += q.to_bytes()

        if self.proto == socket.SOCK_STREAM:
            self.PACKETLEN = len(t)
            t = self.PACKETLEN.to_bytes(2, byteorder='big', signed=False) + t
        return t

    def construct(TID, response, flags=0, opcode=DNSOpcode.QUERY, rcode=DNSResponseCode.NOERR, questions=[], answers=[], authorities=[], additionals=[], proto=socket.SOCK_DGRAM):
        packet = DNSPacket()
        packet.proto = proto
        packet.TransactionID = TID
        packet.QR = response
        packet.Opcode = opcode
        packet.FLAGS = flags
        packet.Rcode = rcode
        packet.QDCOUNT = len(questions)
        packet.ANCOUNT = len(answers)
        packet.NSCOUNT = len(authorities)
        packet.ARCOUNT = len(additionals)
        packet.Questions = questions
        packet.Answers = answers
        packet.Authorities = authorities
        packet.Additionals = additionals
        return packet


class DNSQuestion:

    def __init__(self):
        self.QNAME = None
        self.QTYPE = None
        self.QCLASS = None
        self.QU = None

    def from_bytes(bbuff):
        return DNSQuestion.from_buffer(io.BytesIO(bbuff))

    def from_buffer(buff):
        qst = DNSQuestion()
        qst.QNAME = DNSName.from_buffer(buff)
        qst.QTYPE = DNSType(int.from_bytes((buff.read(2)), byteorder='big', signed=False))
        temp = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        qst.QCLASS = DNSClass(temp & 32767)
        qst.QU = bool((temp & 32768) >> 15)
        return qst

    def to_bytes(self):
        t = self.QNAME.to_bytes()
        t += self.QTYPE.value.to_bytes(2, byteorder='big', signed=False)
        a = self.QCLASS.value
        a |= int(self.QU) << 15
        t += a.to_bytes(2, byteorder='big', signed=False)
        return t

    def construct(qname, qtype, qclass, qu=False):
        qst = DNSQuestion()
        qst.QNAME = DNSName.construct(qname)
        qst.QTYPE = qtype
        qst.QCLASS = qclass
        qst.QU = qu
        return qst

    def __repr__(self):
        t = '== DNSQuestion ==\r\n'
        t += 'QNAME:  %s\r\n' % self.QNAME.name
        t += 'QTYPE:  %s\r\n' % self.QTYPE.name
        t += 'QCLASS: %s\r\n' % self.QCLASS.name
        t += 'QU    : %s\r\n' % self.QU
        return t


class DNSOPT:

    def __init__(self):
        self.Code = None
        self.Length = None
        self.Value = None
        self.size = None

    def from_bytes(buff):
        return DNSOPT.from_buffer(io.BytesIO(buff))

    def from_buffer(buff):
        o = DNSOPT()
        o.Code = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        o.Length = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        o.Value = buff.read(o.Length)
        o.size = o.Length + 2
        return o


class DNSOPTResource:

    def __init__(self):
        self.NAME = None
        self.TYPE = None
        self.UDPSIZE = None
        self.EXTRCODE = None
        self.VERSION = None
        self.DO = None
        self.Z = None
        self.RDLENGTH = None
        self.RDATA = None
        self.options = []

    def from_bytes(bbuff):
        return DNSOPTResource.from_buffer(io.BytesIO(bbuff))

    def from_buffer(buff):
        rsc = DNSOPTResource()
        rsc.NAME = DNSName.from_buffer(buff)
        rsc.TYPE = DNSType(int.from_bytes((buff.read(2)), byteorder='big', signed=False))
        rsc.UDPSIZE = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        rsc.EXTRCODE = int.from_bytes((buff.read(1)), byteorder='big', signed=False)
        rsc.VERSION = int.from_bytes((buff.read(1)), byteorder='big', signed=False)
        temp = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        rsc.DO = bool(temp & 32768)
        rsc.Z = temp & 32767
        rsc.RDLENGTH = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        rsc.RDATA = buff.read(rsc.RDLENGTH)
        return rsc

    def __repr__(self):
        t = '== DNSOPTResource ==\r\n'
        t += 'NAME:  %s\r\n' % self.NAME.name
        t += 'TYPE:  %s\r\n' % self.TYPE.name
        t += 'UDPSIZE : %d\r\n' % self.UDPSIZE
        t += 'EXTRCODE: %s\r\n' % self.EXTRCODE
        t += 'VERSION: %s\r\n' % self.VERSION
        t += 'DO: %s\r\n' % repr(self.DO)
        t += 'RDLENGTH: %d\r\n' % self.RDLENGTH
        t += 'RDATA: %s\r\n' % repr(self.RDATA)
        return t

    def to_bytes(self):
        t = self.NAME.to_bytes()
        t += self.TYPE.value.to_bytes(2, byteorder='big', signed=False)
        t += self.UDPSIZE.to_bytes(2, byteorder='big', signed=False)
        t += self.EXTRCODE.to_bytes(1, byteorder='big', signed=False)
        t += self.VERSION.to_bytes(1, byteorder='big', signed=False)
        a = self.Z
        a |= int(self.DO) << 15
        t += a.to_bytes(2, byteorder='big', signed=False)
        t += self.RDLENGTH.to_bytes(2, byteorder='big', signed=False)
        t += self.RDATA
        return t


class DNSResource:

    def __init__(self):
        self.NAME = None
        self.TYPE = None
        self.CLASS = None
        self.CFLUSH = None
        self.TTL = None
        self.RDLENGTH = None
        self.RDATA = None

    def parse_header(self, buff):
        self.NAME = DNSName.from_buffer(buff)
        self.TYPE = DNSType(int.from_bytes((buff.read(2)), byteorder='big', signed=False))
        temp = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        self.CLASS = DNSClass(temp & 32767)
        self.CFLUSH = bool((temp & 32768) >> 15)
        self.TTL = int.from_bytes((buff.read(4)), byteorder='big', signed=False)
        self.RDLENGTH = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        pos = buff.tell()
        self.RDATA = buff.read(self.RDLENGTH)
        buff.seek(pos, io.SEEK_SET)

    def from_bytes(bbuff):
        return DNSResource.from_buffer(io.BytesIO(bbuff))

    def from_buffer(buff):
        res = DNSResource()
        res.parse_header(buff)
        res.RDATA = buff.read(res.RDLENGTH)
        return res

    def to_bytes(self):
        t = self.NAME.to_bytes()
        t += self.TYPE.value.to_bytes(2, byteorder='big', signed=False)
        a = self.CLASS.value
        a |= int(self.CFLUSH) << 15
        t += a.to_bytes(2, byteorder='big', signed=False)
        t += self.TTL.to_bytes(4, byteorder='big', signed=False)
        t += self.RDLENGTH.to_bytes(2, byteorder='big', signed=False)
        t += self.RDATA
        return t

    def construct(self, rname, rtype, rdata, ttl=30, rclass=DNSClass.IN, cflush=False):
        res = DNSResource()
        res.NAME = DNSName.construct(rname)
        res.TYPE = rtype
        res.CLASS = rclass
        res.CFLUSH = cflush
        res.TTL = ttl
        res.RDATA = rdata
        return res

    def __repr__(self):
        t = '== DNSResource ==\r\n'
        t += 'NAME:  %s\r\n' % self.NAME.name
        t += 'TYPE:  %s\r\n' % self.TYPE.name
        t += 'CLASS : %s\r\n' % self.CLASS.name
        t += 'CFLUSH: %s\r\n' % self.CFLUSH
        t += 'TTL: %s\r\n' % self.TTL
        t += 'RDLENGTH: %s\r\n' % self.RDLENGTH
        t += 'RDATA: %s\r\n' % repr(self.RDATA)
        return t


class DNSAResource(DNSResource):

    def __init__(self):
        DNSResource.__init__(self)
        self.ipaddress = None

    def from_bytes(bbuff):
        return DNSAResource.from_buffer(io.BytesIO(bbuff))

    def from_buffer(buff):
        res = DNSAResource()
        res.parse_header(buff)
        res.ipaddress = ipaddress.IPv4Address(buff.read(res.RDLENGTH))
        return res

    def construct(rname, ipv4, ttl=3000, rclass=DNSClass.IN, cflush=False):
        res = DNSAResource()
        res.NAME = DNSName.construct(rname)
        res.TYPE = DNSType.A
        res.CLASS = rclass
        res.CFLUSH = cflush
        res.TTL = ttl
        res.ipaddress = ipv4
        res.RDATA = res.ipaddress.packed
        res.RDLENGTH = len(res.RDATA)
        return res

    def __repr__(self):
        t = '=== DNS A ===\r\n'
        t += DNSResource.__repr__(self)
        t += 'IP address: %s\r\n' % str(self.ipaddress)
        return t


class DNSAAAAResource(DNSResource):

    def __init__(self):
        DNSResource.__init__(self)
        self.ipaddress = None

    def from_bytes(bbuff):
        return DNSAAAAResource.from_buffer(io.BytesIO(bbuff))

    def from_buffer(buff):
        res = DNSAAAAResource()
        res.parse_header(buff)
        res.ipaddress = ipaddress.IPv6Address(buff.read(res.RDLENGTH))
        return res

    def construct(rname, ipv6, ttl=3000, rclass=DNSClass.IN, cflush=False):
        res = DNSAAAAResource()
        res.NAME = DNSName.construct(rname)
        res.TYPE = DNSType.AAAA
        res.CLASS = rclass
        res.CFLUSH = cflush
        res.TTL = ttl
        res.ipaddress = ipv6
        res.RDATA = res.ipaddress.packed
        res.RDLENGTH = len(res.RDATA)
        return res

    def __repr__(self):
        t = '=== DNS AAAA ===\r\n'
        t += DNSResource.__repr__(self)
        t += 'IP address: %s\r\n' % str(self.ipaddress)
        return t


class DNSPTRResource(DNSResource):

    def __init__(self):
        DNSResource.__init__(self)
        self.domainname = None

    def from_bytes(bbuff):
        return DNSPTRResource.from_buffer(io.BytesIO(bbuff))

    def from_buffer(buff):
        res = DNSPTRResource()
        res.parse_header(buff)
        res.domainname = DNSName.from_buffer(buff)
        return res

    def construct(rname, domainname, ttl=3000, rclass=DNSClass.IN, cflush=False):
        res = DNSPTRResource()
        res.NAME = DNSName.construct(rname)
        res.TYPE = DNSType.PTR
        res.CLASS = rclass
        res.CFLUSH = cflush
        res.TTL = ttl
        res.domainname = domainname
        res.RDATA = DNSName.construct(res.domainname)
        res.RDLENGTH = len(res.RDATA)
        return res

    def __repr__(self):
        t = '=== DNS PTR ===\r\n'
        t += DNSResource.__repr__(self)
        t += 'PTR name: %s\r\n' % str(self.domainname)
        return t


class DNSSRVResource(DNSResource):

    def __init__(self):
        DNSResource.__init__(self)
        self.Service = None
        self.Proto = None
        self.Name = None
        self.Priority = None
        self.Weight = None
        self.Port = None
        self.Target = None

    def from_bytes(bbuff):
        return DNSSRVResource.from_buffer(io.BytesIO(bbuff))

    def from_buffer(buff):
        res = DNSSRVResource()
        res.parse_header(buff)
        try:
            if res.NAME.name.count('.') == 4:
                res.Service, res.Proto, res.Name, tld = res.NAME.name.split('.')
                print(res.Service, res.Proto, res.Name, tld)
            else:
                res.Service = res.NAME.name
        except Exception as e:
            try:
                print(res.NAME.name)
                raise e
            finally:
                e = None
                del e

        res.Priority = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        res.Weight = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        res.Port = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        res.Target = DNSName.from_buffer(buff)
        return res

    def __repr__(self):
        t = '=== DNS SRV ===\r\n'
        t += DNSResource.__repr__(self)
        t += 'Priority: %s\r\n' % str(self.Priority)
        t += 'Weight: %s\r\n' % str(self.Weight)
        t += 'Port: %s\r\n' % str(self.Port)
        t += 'Target: %s\r\n' % str(self.Target)
        return t


class DNSResourceParser:

    def from_bytes(bbuff):
        return DNSResourceParser.from_buffer(io.BytesIO(bbuff))

    def from_buffer(buff):
        pos = buff.tell()
        resname = DNSName.from_buffer(buff)
        restype = DNSType(int.from_bytes((buff.read(2)), byteorder='big', signed=False))
        if restype == DNSType.OPT:
            buff.seek(pos, io.SEEK_SET)
            return DNSOPTResource.from_buffer(buff)
        else:
            buff.seek(pos, io.SEEK_SET)
            if restype == DNSType.A:
                rsc = DNSAResource.from_buffer(buff)
            else:
                if restype == DNSType.AAAA:
                    rsc = DNSAAAAResource.from_buffer(buff)
                else:
                    if restype == DNSType.PTR:
                        rsc = DNSPTRResource.from_buffer(buff)
                    else:
                        if restype == DNSType.SRV:
                            rsc = DNSSRVResource.from_buffer(buff)
                        else:
                            rsc = DNSResource.from_buffer(buff)
        return rsc


class DNSName:

    def __init__(self):
        self.name = ''
        self.compressed = False
        self.compressed_pos = None
        self.compressed_done = False

    def from_bytes(bbuff):
        return DNSName.from_buffer(io.BytesIO(bbuff))

    def from_buffer(buff):
        dnsname = DNSName()
        dnsname.parse(buff)
        return dnsname

    def parse(self, data, rec=False):
        if self.compressed_done:
            return
        temp = data.read(1)[0]
        if not self.compressed:
            self.compressed = (temp & 192) >> 6 == 3
            if self.compressed:
                data.seek(-1, io.SEEK_CUR)
                self.compressed_pos = data.tell()
                temp = int.from_bytes((data.read(2)), byteorder='big', signed=False)
                ptr = temp & 16383
                data.seek(ptr, io.SEEK_SET)
                self.parse(data, rec)
                data.seek(self.compressed_pos + 2, io.SEEK_SET)
                self.compressed_done = True
                return
        length = temp
        if length == 0:
            return
        if length < 63:
            if rec:
                self.name += '.' + data.read(length).decode()
            else:
                self.name += data.read(length).decode()
            self.parse(data, True)

    def construct(name):
        dnsname = DNSName()
        dnsname.name = name
        return dnsname

    def to_bytes(self):
        t = b''
        for label in self.name.split('.'):
            t += len(label).to_bytes(1, byteorder='big', signed=False)
            t += label.encode()

        t += b'\x00'
        return t

    def __repr__(self):
        return self.name