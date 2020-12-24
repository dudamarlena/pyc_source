# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/RTP/RTPHeader.py
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

class RTPHeader(bfrec):
    """RFC1889, 5.1, Page 10"""
    fields = field.mkList([('version', 2, None),
     ('padding', 1, None),
     ('extension', 1, None),
     ('CSRCCount', 4, None),
     ('marker', 1, None),
     ('payloadtype', 7, None),
     ('sequencenumber', 16, None),
     ('timestamp', 32, None),
     ('SSRC', 32, None),
     (
      'CSRC', 32, list)])

    def RTPHeaderInvariant(self):
        assert len(self.CSRC) <= 15
        return True


class RTPSource(object):

    def _generateSSRC(self):
        """rfc1889, 3, Page 8
      The SSRC identifier is a randomly chosen value meant to be globally
      unique within a particular RTP session. If a participant generates
      multiple streams in one RTP session, for example from separate video
      cameras, each must be identified as a different SSRC.
      """
        pass


class RawRTPPayloadHeader(bfrec):
    """No RFC, specific to this implementation"""
    fields = field.mkList([('length', 16, None)])


class RawRTPPayload(object):
    RTPHeader()
    RawRTPPayloadHeader()

    def pack(self):
        rtpheader = self.header.pack()
        rtppayloadheader = self.payloadheader.pack()
        result = rtpheader + rtppayloadheader + self.data


if __name__ == '__main__':
    a = RTPHeader()
    a.timestamp = 1048640772
    a.pack()