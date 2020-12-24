# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/RTP/RTCPHeader.py
# Compiled at: 2008-10-19 12:19:52
"""RTP Header
==========

This class provides a representation of the fixed RTP Headers as per
section 5.1 of RFC1889. The following attributes on an RTPHeader object
represent the fields in the header:
    
   version,padding, extension, CSRCCount, marker, payloadtype
   sequencenumber, timestamp, SSRC, CSRC

The order of the fields and sizes are defined in the variable "struct".
"""
from Kamaelia.bitfieldrec import bfrec, field

class RTCPHeader(bfrec):
    """Abstract (note, *not* base) class for RTCP packet types"""
    pass


class ReportBlock(bfrec):
    """RFC 1889, 6.3.1 page 25, used in SR & RR"""
    fields = field.mkList([('SSRC_n', 32, None),
     ('fractionLost', 8, None),
     ('cumulativePacketsLost', 24, None),
     ('extendedHighSeqNumRecv', 32, None),
     ('interarrivalJitter', 32, None),
     ('lastSRTimestamp', 32, None),
     ('delaySinceLastSR', 32, None)])


class SenderReport(RTCPHeader):
    """RFC1889, 6.3.1, Page 23"""
    fields = field.mkList([('version', 2, None),
     ('padding', 1, None),
     ('receptionReportCount', 5, None),
     ('packetType', 8, None),
     ('length', 16, None),
     ('SSRC', 32, None),
     ('NTPtimestamp', 64, None),
     ('RTPtimestamp:', 32, None),
     ('sendersPacketCount', 32, None),
     ('sendersOctetCount', 32, None)])

    def SenderReportInvariant(self):
        assert self.packetType == 200
        return True


class ReceiverReport(RTCPHeader):
    """RFC1889, 6.3.2, Page 28"""
    fields = field.mkList([('version', 2, None),
     ('padding', 1, None),
     ('receptionReportCount', 5, None),
     ('packetType', 8, None),
     ('length', 16, None),
     ('SSRC', 32, None)])

    def ReceiverReportInvariant(self):
        assert self.packetType == 201
        return True


class SourceDescription_item(bfrec):
    """RFC1889, 6.4, Page 31"""
    fields = field.mkList([('itemType', 8, None),
     ('length', 8, None),
     (
      'description', 8, list)])

    def SourceDescription_itemInvariant(self):
        assert len(self.description) == self.length
        return True


class CName(SourceDescription_item):
    """RFC1889, 6.4.1, Page 32"""

    def CNameInvariant(self):
        assert self.itemType == 1
        assert self.SourceDescription_itemInvariant()
        return True


class Name(SourceDescription_item):
    """RFC1889, 6.4.2, Page 34"""

    def NameInvariant(self):
        assert self.itemType == 2
        assert self.SourceDescription_itemInvariant()
        return True


class Email(SourceDescription_item):
    """RFC1889, 6.4.3, Page 34"""

    def EmailInvariant(self):
        assert self.itemType == 3
        assert self.SourceDescription_itemInvariant()
        return True


class Phone(SourceDescription_item):
    """RFC1889, 6.4.4, Page 34"""

    def PhoneInvariant(self):
        assert self.itemType == 4
        assert self.SourceDescription_itemInvariant()
        return True


class Loc(SourceDescription_item):
    """RFC1889, 6.4.5, Page 35"""

    def LocInvariant(self):
        assert self.itemType == 5
        assert self.SourceDescription_itemInvariant()
        return True


class Tool(SourceDescription_item):
    """RFC1889, 6.4.6, Page 35"""

    def ToolInvariant(self):
        assert self.itemType == 6
        assert self.SourceDescription_itemInvariant()
        return True


class Note(SourceDescription_item):
    """RFC1889, 6.4.7, Page 35"""

    def NoteInvariant(self):
        assert self.itemType == 7
        assert self.SourceDescription_itemInvariant()
        return True


class Priv(SourceDescription_item):
    """RFC1889, 6.4.8, Page 36
   Note Whilst having the same basic format, the fields
   here are redefined since the description portion is subdivided.
   """
    fields = field.mkList([('itemType', 8, None),
     ('length', 8, None),
     ('prefixLength', 8, None),
     (
      'prefixString', 8, list),
     (
      'description', 8, list)])

    def PrivInvariant(self):
        assert self.itemType == 8
        assert len(self.description) + len(self.prefixString) + 1 == self.length
        return True


class SourceDescription_chunk(bfrec):
    """RFC1889, 6.4, Page 31"""
    fields = field.mkList([('SSRC_CSRC', 32, None)])

    def SourceDescription_chunkInvariant(self):
        """octet count of chunk *must* be divisible by 4."""
        return True


class SourceDescription(RTCPHeader):
    """RFC1889, 6.4, Page 31"""
    fields = field.mkList([('version', 2, None),
     ('padding', 1, None),
     ('sourceCount', 5, None),
     ('packetType', 8, None),
     ('length', 16, None)])

    def SourceDescriptionInvariant(self):
        assert self.packetType == 202
        return True


class ByePacket(RTCPHeader):
    """RFC1889, 6.5, Page 37"""
    fields = field.mkList([('version', 2, None),
     ('padding', 1, None),
     ('sourceCount', 5, None),
     ('packetType', 8, None),
     ('length', 16, None),
     (
      'SSRC_CSRC', 32, list),
     ('reasonLength', 8, None),
     (
      'reasonString', 8, list)])

    def ByePacketInvariant(self):
        assert self.packetType == 203
        assert self.sourceCount == len(self.SSRC_CSRC)
        assert self.reasonLength == len(self.reasonString)
        assert self.length == (self.version.size + self.padding.size + self.sourceCount.size + self.packetType.size + self.length.size + self.reasonLength.size + self.SSRC_CSRC.size * len(self.SSRC_CSRC) + self.reasonString.size * len(self.reasonString)) / 32 - 1
        return True


class AppPacket(RTCPHeader):
    """RFC1889, 6.5, Page 37"""
    fields = field.mkList([('version', 2, None),
     ('padding', 1, None),
     ('subtype', 5, None),
     ('packetType', 8, None),
     ('length', 16, None),
     ('SSRC_CSRC', 32, None),
     (
      'name', 8, list),
     (
      'appData', 32, list)])

    def AppPacketInvariant(self):
        assert self.packetType == 204
        assert len(self.name) == 4
        assert self.reasonLength == len(self.reasonString)
        assert self.length == (self.version.size + self.padding.size + self.subtype.size + self.packetType.size + self.length.size + self.SSRC_CSRC.size + self.name.size * len(self.name) + self.appData.size * len(self.appData)) / 32 - 1
        return True


class RawRTPPayload(object):
    RTPHeader()
    RawRTPPayloadHeader()

    def pack(self):
        rtpheader = self.header.pack()
        rtppayloadheader = self.payloadheader.pack()
        result = rtpheader + rtppayloadheader + self.data


if __name__ == '__main__':
    RB = ReportBlock()
    RB.fractionLost = 5
    RB.cumulativePacketsLost = 5
    RB.extendedHighSeqNumRecv = 5
    RB.interarrivalJitter = 6
    RB.lastSRTimestamp = 7
    RB.delaySinceLastSR = 8
    RB.pack()
    SR = SenderReport()
    SR.version = 2
    SR.padding = 0
    SR.receptionReportCount = 5
    SR.packetType = 200
    SR.length = 32
    SR.SSRC = 12345
    SR.NTPtimestamp = 12345678901234567890
    SR.RTPtimestamp = 123456789
    SR.sendersPacketCount = 5
    SR.sendersOctetCount = 1000
    SR.pack()
    RR = ReceiverReport()
    RR.version = 2
    RR.padding = 1
    RR.receptionReportCount = 5
    RR.packetType = 201
    RR.length = 12345
    RR.SSRC = 123454321
    RR.pack()
    SDi = SourceDescription_item()
    SDi.itemType = 123
    SDi.length = 22
    SDi.description = [104, 101, 108, 108, 111]
    SDi.pack()
    CN = CName()
    CN.itemType = 1
    CN.description = [ ord(x) for x in "It's the cname" ]
    CN.length = len(CN.description)
    CN.pack()
    NDES = Name()
    NDES.itemType = 2
    NDES.description = [ ord(x) for x in "It's the name" ]
    NDES.length = len(NDES.description)
    NDES.pack()
    EML = Email()
    EML.itemType = 3
    EML.description = [ ord(x) for x in 'foo@bar.com' ]
    EML.length = len(EML.description)
    EML.pack()
    PNE = Phone()
    PNE.itemType = 4
    PNE.description = [ ord(x) for x in '01234 123456' ]
    PNE.length = len(PNE.description)
    PNE.pack()
    LOC = Loc()
    LOC.itemType = 5
    LOC.description = [ ord(x) for x in '01234 123456' ]
    LOC.length = len(LOC.description)
    LOC.pack()
    TLL = Tool()
    TLL.itemType = 5
    TLL.description = [ ord(x) for x in 'Axon' ]
    TLL.length = len(TLL.description)
    TLL.pack()
    NTE = Note()
    NTE.itemType = 5
    NTE.description = [ ord(x) for x in 'NB. Buy Milk' ]
    NTE.length = len(NTE.description)
    NTE.pack()
    PRV = Note()
    PRV.itemType = 5
    PRV.description = [ ord(x) for x in 'Some Note' ]
    PRV.prefixString = [ ord(x) for x in 'Some other Note' ]
    PRV.prefixLength = len(PRV.prefixString)
    PRV.length = len(PRV.description) + len(PRV.prefixString) + 1
    PRV.pack()
    SDES_c = SourceDescription_chunk()
    SDES_c.SSRC_CSRC = 1234
    SDES_c.pack()
    SDES = SourceDescription()
    SDES.version = 2
    SDES.padding = 1
    SDES.sourceCount = 16
    SDES.packetType = 202
    SDES.length = 123
    SDES.pack()
    BYE = ByePacket()
    BYE.version = 2
    BYE.padding = 0
    BYE.sourceCount = 6
    BYE.packetType = 203
    BYE.length = 1234
    BYE.SSRC_CSRC = [1, 2, 3, 4, 5, 6]
    BYE.reasonString = [ ord(x) for x in 'Wibble' ]
    BYE.reasonLength = len(BYE.reasonString)
    BYE.pack()
    APP = AppPacket()
    APP.version = 2
    APP.padding = 0
    APP.subtype = 6
    APP.packetType = 204
    APP.length = 1234
    APP.SSRC_CSRC = 123456
    APP.name = [ ord(x) for x in 'TEST' ]
    APP.appData = [ ord(x) for x in 'hello world' ]
    APP.pack()