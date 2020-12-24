# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\protocols\LLMNR.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 4436 bytes
import enum, io, socket, asyncio, ipaddress
from responder3.protocols.DNS import *

class LLMNRFlags(enum.IntFlag):
    CONFILCT = 64
    TRUNCATION = 32
    TENTATIVE = 16
    RESERVED1 = 8
    RESERVED2 = 4
    RESERVED3 = 2
    RESERVED4 = 1


class LLMNROpcode(enum.Enum):
    DEFAULT = 0


class LLMNRResponse(enum.Enum):
    REQUEST = 0
    RESPONSE = 1


class LLMNRPacket:

    def __init__(self):
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

    async def from_streamreader(reader):
        data = await reader.read()
        return LLMNRPacket.from_bytes(data)

    def from_bytes(bbuff):
        return LLMNRPacket.from_buffer(io.BytesIO(bbuff))

    def from_buffer(buff):
        packet = LLMNRPacket()
        packet.TransactionID = buff.read(2)
        temp = int.from_bytes((buff.read(2)), byteorder='big', signed=False)
        packet.QR = LLMNRResponse(temp >> 15)
        packet.Opcode = LLMNROpcode((temp & 30720) >> 11)
        packet.FLAGS = LLMNRFlags((temp & 2032) >> 4)
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
        t = '== LLMNRPacket ==\r\n'
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
        t = b''
        t += self.TransactionID
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

        return t

    def construct(TID, response, flags=0, opcode=LLMNROpcode.DEFAULT, rcode=DNSResponseCode.NOERR, questions=[], answers=[], authorities=[], additionals=[]):
        packet = LLMNRPacket()
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