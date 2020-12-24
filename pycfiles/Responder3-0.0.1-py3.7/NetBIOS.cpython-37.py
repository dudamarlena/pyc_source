# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\protocols\NetBIOS.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 12360 bytes
import io, enum, asyncio, ipaddress

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


class NBQType(enum.Enum):
    NB = 32
    NBSTAT = 33


class NBQClass(enum.Enum):
    IN = 1


class NBRType(enum.Enum):
    A = 1
    NS = 2
    NULL = 10
    NB = 32
    NBSTAT = 33


class NBRClass(enum.Enum):
    IN = 1


class NBTSNMFlags(enum.IntFlag):
    AUTHORATIVEANSWER = 64
    TRUNCATED = 32
    RECURSIONDESIRED = 16
    RECURSIONAVAILABLE = 8
    BROADCAST = 1


class NBTNSOpcode(enum.Enum):
    QUERY = 0
    REGISTRATION = 5
    RELEASE = 6
    WACK = 7
    REFRESH = 8


class NBTSResponse(enum.Enum):
    REQUEST = 0
    RESPONSE = 1


class NBTNSPacket:

    def __init__(self):
        self.NAME_TRN_ID = None
        self.RESPONSE = None
        self.NM_FLAGS = None
        self.OPCPDE = None
        self.RCODE = None
        self.QDCOUNT = None
        self.ANCOUNT = None
        self.NSCOUNT = None
        self.ARCOUNT = None
        self.Questions = []
        self.Answers = []
        self.Authorities = []
        self.Additionals = []

    async def from_streamreader(reader):
        data = await reader.read()
        return NBTNSPacket.from_bytes(data)

    def from_bytes(bbuff):
        return NBTNSPacket.from_buffer(io.BytesIO(bbuff))

    def from_buffer(buff):
        packet = NBTNSPacket()
        packet.NAME_TRN_ID = buff.read(2)
        t = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        packet.RESPONSE = NBTSResponse(t >> 15)
        packet.OPCODE = NBTNSOpcode((t & 30720) >> 11)
        packet.NM_FLAGS = NBTSNMFlags((t & 2032) >> 4)
        packet.RCODE = t & 15
        packet.QDCOUNT = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        packet.ANCOUNT = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        packet.NSCOUNT = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        packet.ARCOUNT = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        for i in range(0, packet.QDCOUNT):
            dnsq = NBQuestion.from_buffer(buff)
            packet.Questions.append(dnsq)

        for i in range(0, packet.ANCOUNT):
            dnsr = NBResource.from_buffer(buff)
            packet.Answers.append(dnsr)

        for i in range(0, packet.NSCOUNT):
            dnsr = NBResource.from_buffer(buff)
            packet.Answers.append(dnsr)

        for i in range(0, packet.ARCOUNT):
            dnsr = NBResource.from_buffer(buff)
            packet.Answers.append(dnsr)

        return packet

    def construct(self, TID, response, opcode, nmflags, rcode=0, questions=[], answers=[], authorities=[], additionals=[]):
        self.NAME_TRN_ID = TID
        self.RESPONSE = response
        self.OPCODE = opcode
        self.NM_FLAGS = nmflags
        self.RCODE = rcode
        self.QDCOUNT = len(questions)
        self.ANCOUNT = len(answers)
        self.NSCOUNT = len(authorities)
        self.ARCOUNT = len(additionals)
        self.Questions = questions
        self.Answers = answers
        self.Authorities = authorities
        self.Additionals = additionals

    def to_bytes(self):
        t = self.NAME_TRN_ID
        a = self.RCODE & 15
        a |= self.NM_FLAGS << 4 & 2032
        a |= self.OPCODE.value << 11 & 30720
        a |= self.RESPONSE.value << 15 & 32768
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

        return t

    def __repr__(self):
        t = '== NBTNSPacket ==\r\n'
        t += 'TransactionID %s\r\n' % self.NAME_TRN_ID.hex()
        t += 'RESPONSE : %s\r\n' % self.RESPONSE.name
        t += 'OPCODE   : %s\r\n' % self.OPCODE.name
        t += 'NM_FLAGS : %s\r\n' % repr(self.NM_FLAGS)
        t += 'RCODE    : %s\r\n' % self.RCODE
        t += 'QDCOUNT  : %s\r\n' % self.QDCOUNT
        t += 'ANCOUNT  : %s\r\n' % self.ANCOUNT
        t += 'NSCOUNT  : %s\r\n' % self.NSCOUNT
        t += 'ARCOUNT  : %s\r\n' % self.ARCOUNT
        for question in self.Questions:
            t += repr(question)

        for answer in self.Answers:
            t += repr(answer)

        return t


class NBQuestion:

    def __init__(self):
        self.QNAME = None
        self.QTYPE = None
        self.QCLASS = None

    def from_bytes(bbuff):
        return NBQuestion.from_buffer(io.BytesIO(bbuff))

    def from_buffer(buff):
        qst = NBQuestion()
        qst.QNAME = NBName.from_buffer(buff)
        qst.QTYPE = NBQType(int.from_bytes((buff.read(2)), byteorder='big'))
        qst.QCLASS = NBQClass(int.from_bytes((buff.read(2)), byteorder='big'))
        return qst

    def to_bytes(self):
        t = self.QNAME.to_bytes()
        t += self.QTYPE.value.to_bytes(2, byteorder='big', signed=False)
        t += self.QCLASS.value.to_bytes(2, byteorder='big', signed=False)
        return t

    def construct(self, qname, qtype, qclass):
        self.QNAME = qname
        self.QTYPE = qtype
        self.QCLASS = qclass

    def __repr__(self):
        t = '== NetBIOS Question ==\r\n'
        t += 'QNAME:  %s\r\n' % self.QNAME
        t += 'QTYPE:  %s\r\n' % self.QTYPE.name
        t += 'QCLASS: %s\r\n' % self.QCLASS.name
        return t


class NBResource:

    def __init__(self):
        self.NAME = None
        self.TYPE = None
        self.CLASS = None
        self.TTL = None
        self.RDLENGTH = None
        self.RDATA = None

    def from_bytes(bbuff):
        return NBResource.from_buffer(io.BytesIO(bbuff))

    def from_buffer(buff):
        rs = NBResource()
        rs.NAME = NBName.from_buffer(buff)
        rs.TYPE = NBRType(int.from_bytes((buff.read(2)), byteorder='big'))
        rs.CLASS = NBRClass(int.from_bytes((buff.read(2)), byteorder='big'))
        rs.TTL = int.from_bytes((buff.read(4)), byteorder='big')
        rs.RDLENGTH = int.from_bytes((buff.read(2)), byteorder='big')
        trdata = buff.read(rs.RDLENGTH)
        if rs.TYPE == NBRType.A and rs.QCLASS == NBRClass.IN:
            rs.RDATA = ipaddress.IPv4Address(trdata)
        else:
            rs.RDATA = trdata

    def to_bytes(self):
        t = self.NAME.to_bytes()
        t += self.TYPE.value.to_bytes(2, byteorder='big', signed=False)
        t += self.CLASS.value.to_bytes(2, byteorder='big', signed=False)
        t += self.TTL.to_bytes(4, byteorder='big', signed=False)
        t += self.RDLENGTH.to_bytes(2, byteorder='big', signed=False)
        t += self.RDATA
        return t

    def construct(self, name, rtype, ip, flags=0, ttl=3000, rclass=NBRClass.IN):
        self.NAME = name
        self.TYPE = rtype
        self.CLASS = rclass
        self.TTL = ttl
        if self.TYPE == NBRType.NB:
            if self.CLASS == NBRClass.IN:
                self.RDATA = flags.to_bytes(2, byteorder='big', signed=False)
                self.RDATA += ip.packed
        self.RDLENGTH = len(self.RDATA)

    def __repr__(self):
        t = '== NetBIOS Resource ==\r\n'
        t += 'NAME:  %s\r\n' % self.NAME
        t += 'TYPE:  %s\r\n' % self.TYPE.name
        t += 'CLASS: %s\r\n' % self.CLASS.name
        t += 'TTL: %s\r\n' % self.TTL
        t += 'RDLENGTH: %s\r\n' % self.RDLENGTH
        t += 'RDATA: %s\r\n' % repr(self.RDATA)
        return t


class NBSuffixGroup(enum.Enum):
    MACHINE_GROUP = 0
    MASTER_BROWSER = 1
    BROWSER_SERVICE = 30

    @classmethod
    def has_value(cls, value):
        return any((value == item.value for item in cls))


class NBSuffixUnique(enum.Enum):
    WORKSTATION = 0
    DOMAIN = 27
    MACHINE_GROUP = 29
    SERVER = 32
    DOMAIN_CONTROLLER = 28
    UNKNOWN_1 = 25
    UNKNOWN_2 = 72

    @classmethod
    def has_value(cls, value):
        return any((value == item.value for item in cls))


class NBName:

    def __init__(self):
        self.length = None
        self.name = None
        self.suffix = None

    def from_bytes(bbuff):
        return NBName.from_buffer(io.BytesIO(bbuff))

    def from_buffer(buff):
        name = NBName()
        name.length = int.from_bytes((buff.read(1)), byteorder='big')
        if name.length == 32:
            temp = NBName.decode_NS(buff.read(name.length))
        else:
            ptr = int.from_bytes((buff.read(1)), byteorder='big')
            pos = buff.tell()
            buff.seek(ptr, io.SEEK_SET)
            tlen = int.from_bytes((buff.read(1)), byteorder='big')
            temp = NBName.decode_NS(buff.read(tlen))
            buff.seek(pos, io.SEEK_SET)
        name.name = temp[:-1].strip()
        if NBSuffixUnique.has_value(ord(temp[(-1)])):
            name.suffix = NBSuffixUnique(ord(temp[(-1)]))
        else:
            name.suffix = NBSuffixGroup(ord(temp[(-1)]))
        if name.length == 32:
            zero = buff.read(1)
        return name

    def construct(name, suffix=NBSuffixUnique.WORKSTATION):
        assert len(name) == 15, 'NBNames max size is 15 chars'
        nbname = NBName()
        nbname.suffix = suffix
        nbname.name = name
        nbname.length = len(NBName.encode_NS(name, suffix.value))
        return name

    def to_bytes(self):
        t = self.length.to_bytes(1, byteorder='big', signed=False)
        t += NBName.encode_NS(self.name, self.suffix.value)
        t += b'\x00'
        return t

    def encode_NS(name, suffix):
        name = name.encode()
        name = name.ljust(15, b' ')
        name = name.upper()
        name += suffix.to_bytes(1, byteorder='big', signed=False)
        temp = b''
        for c in name:
            temp += (((c & 240) >> 4) + 65).to_bytes(1, byteorder='big', signed=False)
            temp += ((c & 15) + 65).to_bytes(1, byteorder='big', signed=False)

        return temp

    def decode_NS(encoded_name):
        name_raw = ''
        transform = [i - 65 & 15 for i in encoded_name]
        i = 0
        while i < len(transform):
            name_raw += chr(transform[i] << 4 | transform[(i + 1)])
            i += 2

        return name_raw

    def __repr__(self):
        t = '== NBName ==\r\n'
        t += 'name  : %s \r\n' % self.name
        t += 'suffix: %s \r\n' % repr(self.suffix)
        t += 'length: %s \r\n' % repr(self.length)
        return t