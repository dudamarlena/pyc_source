# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\protocols\authentication\NTLM.py
# Compiled at: 2019-08-15 18:27:11
# Size of source mod 2**32: 48774 bytes
import io, os, enum, base64, collections, hmac
from responder3.crypto.symmetric import DES
from responder3.crypto.hashing import *
from responder3.core.commons import timestamp2datetime
from responder3.core.logging.log_objects import Credential
from responder3.protocols.SMB.ntstatus import *
from responder3.protocols.authentication.common import *

class NegotiateFlags(enum.IntFlag):
    NEGOTIATE_56 = 2147483648
    NEGOTIATE_KEY_EXCH = 1073741824
    NEGOTIATE_128 = 536870912
    r1 = 268435456
    r2 = 134217728
    r3 = 67108864
    NEGOTIATE_VERSION = 33554432
    r4 = 16777216
    NEGOTIATE_TARGET_INFO = 8388608
    REQUEST_NON_NT_SESSION_KEY = 4194304
    r5 = 2097152
    NEGOTIATE_IDENTIFY = 1048576
    NEGOTIATE_EXTENDED_SESSIONSECURITY = 524288
    r6 = 262144
    TARGET_TYPE_SERVER = 131072
    TARGET_TYPE_DOMAIN = 65536
    NEGOTIATE_ALWAYS_SIGN = 32768
    r7 = 16384
    NEGOTIATE_OEM_WORKSTATION_SUPPLIED = 8192
    NEGOTIATE_OEM_DOMAIN_SUPPLIED = 4096
    J = 2048
    r8 = 1024
    NEGOTIATE_NTLM = 512
    r9 = 256
    NEGOTIATE_LM_KEY = 128
    NEGOTIATE_DATAGRAM = 64
    NEGOTIATE_SEAL = 32
    NEGOTIATE_SIGN = 16
    r10 = 8
    REQUEST_TARGET = 4
    NTLM_NEGOTIATE_OEM = 2
    NEGOTIATE_UNICODE = 1


NegotiateFlagExp = {NegotiateFlags.NEGOTIATE_56: 'requests 56-bit encryption. If the client sends NTLMSSP_NEGOTIATE_SEAL or NTLMSSP_NEGOTIATE_SIGN with NTLMSSP_NEGOTIATE_56 to the server in the NEGOTIATE_MESSAGE, the server MUST return NTLMSSP_NEGOTIATE_56 to the client in the CHALLENGE_MESSAGE.   Otherwise it is ignored. If both NTLMSSP_NEGOTIATE_56 and NTLMSSP_NEGOTIATE_128 are requested and supported by the client and server, NTLMSSP_NEGOTIATE_56 and NTLMSSP_NEGOTIATE_128 will both be returned to the client. Clients and servers that set NTLMSSP_NEGOTIATE_SEAL SHOULD set NTLMSSP_NEGOTIATE_56 if it is supported. An alternate name for this field is NTLMSSP_NEGOTIATE_56.', 
 NegotiateFlags.NEGOTIATE_KEY_EXCH: 'requests an explicit key exchange. This capability SHOULD be used because it improves security for message integrity or confidentiality. See sections 3.2.5.1.2, 3.2.5.2.1, and 3.2.5.2.2 for details. An alternate name for this field is NTLMSSP_NEGOTIATE_KEY_EXCH.', 
 NegotiateFlags.NEGOTIATE_128: 'requests 128-bit session key negotiation. An alternate name for this field is NTLMSSP_NEGOTIATE_128. If the client sends NTLMSSP_NEGOTIATE_128 to the server in the NEGOTIATE_MESSAGE, the server MUST return NTLMSSP_NEGOTIATE_128 to the client in the CHALLENGE_MESSAGE only if the client sets NTLMSSP_NEGOTIATE_SEAL or NTLMSSP_NEGOTIATE_SIGN. Otherwise it is ignored. If both NTLMSSP_NEGOTIATE_56 and NTLMSSP_NEGOTIATE_128 are requested and supported by the client and server, NTLMSSP_NEGOTIATE_56 and NTLMSSP_NEGOTIATE_128 will both be returned to the client. Clients and servers that set NTLMSSP_NEGOTIATE_SEAL SHOULD set NTLMSSP_NEGOTIATE_128 if it is supported. An alternate name for this field is NTLMSSP_NEGOTIATE_128.<23>', 
 NegotiateFlags.r1: 'This bit is unused and MUST be zero.', 
 NegotiateFlags.r2: 'This bit is unused and MUST be zero.', 
 NegotiateFlags.r3: 'This bit is unused and MUST be zero.', 
 NegotiateFlags.NEGOTIATE_VERSION: 'requests the protocol version number. The data corresponding to this flag is provided in the Version field of the NEGOTIATE_MESSAGE, the CHALLENGE_MESSAGE, and the AUTHENTICATE_MESSAGE.<24> An alternate name for this field is NTLMSSP_NEGOTIATE_VERSION.', 
 NegotiateFlags.r4: 'This bit is unused and MUST be zero.', 
 NegotiateFlags.NEGOTIATE_TARGET_INFO: 'indicates that the TargetInfo fields in the CHALLENGE_MESSAGE (section 2.2.1.2) are populated. An alternate name for this field is NTLMSSP_NEGOTIATE_TARGET_INFO.', 
 NegotiateFlags.REQUEST_NON_NT_SESSION_KEY: ' requests the usage of the LMOWF. An alternate name for this field is NTLMSSP_REQUEST_NON_NT_SESSION_KEY.', 
 NegotiateFlags.r5: 'This bit is unused and MUST be zero.', 
 NegotiateFlags.NEGOTIATE_IDENTIFY: 'requests an identify level token. An alternate name for this field is NTLMSSP_NEGOTIATE_IDENTIFY.', 
 NegotiateFlags.NEGOTIATE_EXTENDED_SESSIONSECURITY: 'requests usage of the NTLM v2 session security. NTLM v2 session security is a misnomer because it is not NTLM v2. It is NTLM v1 using the extended session security that is also in NTLM v2. NTLMSSP_NEGOTIATE_LM_KEY and NTLMSSP_NEGOTIATE_EXTENDED_SESSIONSECURITY are mutually exclusive. If both NTLMSSP_NEGOTIATE_EXTENDED_SESSIONSECURITY and NTLMSSP_NEGOTIATE_LM_KEY are requested, NTLMSSP_NEGOTIATE_EXTENDED_SESSIONSECURITY alone MUST be returned to the client. NTLM v2 authentication session key generation MUST be supported by both the client and the DC in order to be used, and extended  session security signing and sealing requires support from the client and the server in order to be used.<25> An alternate name for this field is NTLMSSP_NEGOTIATE_EXTENDED_SESSIONSECURITY.', 
 NegotiateFlags.r6: 'This bit is unused and MUST be zero.', 
 NegotiateFlags.TARGET_TYPE_SERVER: 'TargetName MUST be a server name. The data corresponding to this flag is provided by the server in the TargetName field of the CHALLENGE_MESSAGE. If this bit is set, then NTLMSSP_TARGET_TYPE_DOMAIN MUST NOT be set. This flag MUST be ignored in the NEGOTIATE_MESSAGE and the AUTHENTICATE_MESSAGE. An alternate name for this field is NTLMSSP_TARGET_TYPE_SERVER.', 
 NegotiateFlags.TARGET_TYPE_DOMAIN: 'TargetName MUST be a domain name. The data corresponding to this flag is provided by the server in the TargetName field of the CHALLENGE_MESSAGE. then NTLMSSP_TARGET_TYPE_SERVER MUST NOT be set. This flag MUST be ignored in the NEGOTIATE_MESSAGE and the AUTHENTICATE_MESSAGE. An alternate name for this field is NTLMSSP_TARGET_TYPE_DOMAIN.', 
 NegotiateFlags.NEGOTIATE_ALWAYS_SIGN: ' requests the presence of a signature block on all messages. NTLMSSP_NEGOTIATE_ALWAYS_SIGN MUST be set in the NEGOTIATE_MESSAGE to the server and the CHALLENGE_MESSAGE to the client. NTLMSSP_NEGOTIATE_ALWAYS_SIGN is overridden by NTLMSSP_NEGOTIATE_SIGN and NTLMSSP_NEGOTIATE_SEAL, if they are supported. An alternate name for this field is NTLMSSP_NEGOTIATE_ALWAYS_SIGN.', 
 NegotiateFlags.r7: 'This bit is unused and MUST be zero.', 
 NegotiateFlags.NEGOTIATE_OEM_WORKSTATION_SUPPLIED: 'This flag indicates whether the Workstation field is present. If this flag is not set, the Workstation field MUST be ignored. If this flag is set, the length of the Workstation field specifies whether the workstation name is nonempty or not.<26> An alternate name for this field is NTLMSSP_NEGOTIATE_OEM_WORKSTATION_SUPPLIED.', 
 NegotiateFlags.NEGOTIATE_OEM_DOMAIN_SUPPLIED: 'the domain name is provided (section 2.2.1.1).<27> An alternate name for this field is NTLMSSP_NEGOTIATE_OEM_DOMAIN_SUPPLIED.', 
 NegotiateFlags.J: 'the connection SHOULD be anonymous.<28>', 
 NegotiateFlags.r8: 'This bit is unused and MUST be zero.', 
 NegotiateFlags.NEGOTIATE_NTLM: 'requests usage of the NTLM v1 session security protocol. NTLMSSP_NEGOTIATE_NTLM MUST be set in the NEGOTIATE_MESSAGE to the server and the CHALLENGE_MESSAGE to the client. An alternate name for this field is NTLMSSP_NEGOTIATE_NTLM.', 
 NegotiateFlags.r9: 'This bit is unused and MUST be zero.', 
 NegotiateFlags.NEGOTIATE_LM_KEY: 'requests LAN Manager (LM) session key computation. NTLMSSP_NEGOTIATE_LM_KEY and NTLMSSP_NEGOTIATE_EXTENDED_SESSIONSECURITY are mutually exclusive. If both NTLMSSP_NEGOTIATE_LM_KEY and NTLMSSP_NEGOTIATE_EXTENDED_SESSIONSECURITY are requested, NTLMSSP_NEGOTIATE_EXTENDED_SESSIONSECURITY alone MUST be returned to the client. NTLM v2 authentication session key generation MUST be supported by both the client and the DC in order to be used, and extended session security signing and sealing requires support from the client and the server to be used. An alternate name for this field is NTLMSSP_NEGOTIATE_LM_KEY.', 
 NegotiateFlags.NEGOTIATE_DATAGRAM: 'requests connectionless authentication. If NTLMSSP_NEGOTIATE_DATAGRAM is set, then NTLMSSP_NEGOTIATE_KEY_EXCH MUST always be set in the AUTHENTICATE_MESSAGE to the server and the CHALLENGE_MESSAGE to the client. An alternate name for this field is NTLMSSP_NEGOTIATE_DATAGRAM', 
 NegotiateFlags.NEGOTIATE_SEAL: 'requests session key negotiation for message confidentiality. If the client sends NTLMSSP_NEGOTIATE_SEAL to the server in the NEGOTIATE_MESSAGE, the server MUST return NTLMSSP_NEGOTIATE_SEAL to the client in the CHALLENGE_MESSAGE. Clients and servers that set NTLMSSP_NEGOTIATE_SEAL SHOULD always set NTLMSSP_NEGOTIATE_56 and NTLMSSP_NEGOTIATE_128, if they are supported. An alternate name for this field is NTLMSSP_NEGOTIATE_SEAL.', 
 NegotiateFlags.NEGOTIATE_SIGN: 'requests session key negotiation for message signatures. If the client sends NTLMSSP_NEGOTIATE_SIGN to the server in the NEGOTIATE_MESSAGE, the server MUST return NTLMSSP_NEGOTIATE_SIGN to the client in the CHALLENGE_MESSAGE. An alternate name for this field is NTLMSSP_NEGOTIATE_SIGN.', 
 NegotiateFlags.r10: 'This bit is unused and MUST be zero.', 
 NegotiateFlags.REQUEST_TARGET: 'TargetName field of the CHALLENGE_MESSAGE (section 2.2.1.2) MUST be supplied. An alternate name for this field is NTLMSSP_REQUEST_TARGET.', 
 NegotiateFlags.NTLM_NEGOTIATE_OEM: 'requests OEM character set encoding. An alternate name for this field is NTLM_NEGOTIATE_OEM. See bit A for details.', 
 NegotiateFlags.NEGOTIATE_UNICODE: 'requests Unicode character set encoding. An alternate name for this field is NTLMSSP_NEGOTIATE_UNICODE.'}

class NTLMRevisionCurrent(enum.Enum):
    NTLMSSP_REVISION_W2K3 = 15


class WindowsMajorVersion(enum.Enum):
    WINDOWS_MAJOR_VERSION_5 = 5
    WINDOWS_MAJOR_VERSION_6 = 6
    WINDOWS_MAJOR_VERSION_10 = 10


class WindowsMinorVersion(enum.Enum):
    WINDOWS_MINOR_VERSION_0 = 0
    WINDOWS_MINOR_VERSION_1 = 1
    WINDOWS_MINOR_VERSION_2 = 2
    WINDOWS_MINOR_VERSION_3 = 3


WindowsProduct = {(
 WindowsMajorVersion.WINDOWS_MAJOR_VERSION_5, WindowsMinorVersion.WINDOWS_MINOR_VERSION_1): 'Windows XP operating system Service Pack 2 (SP2)', 
 (
 WindowsMajorVersion.WINDOWS_MAJOR_VERSION_5, WindowsMinorVersion.WINDOWS_MINOR_VERSION_2): 'Windows Server 2003', 
 (
 WindowsMajorVersion.WINDOWS_MAJOR_VERSION_6, WindowsMinorVersion.WINDOWS_MINOR_VERSION_0): 'Windows Vista or Windows Server 2008', 
 (
 WindowsMajorVersion.WINDOWS_MAJOR_VERSION_6, WindowsMinorVersion.WINDOWS_MINOR_VERSION_1): 'Windows 7 or Windows Server 2008 R2', 
 (
 WindowsMajorVersion.WINDOWS_MAJOR_VERSION_6, WindowsMinorVersion.WINDOWS_MINOR_VERSION_2): 'Windows 8 or Windows Server 2012 operating system', 
 (
 WindowsMajorVersion.WINDOWS_MAJOR_VERSION_6, WindowsMinorVersion.WINDOWS_MINOR_VERSION_3): 'Windows 8.1 or Windows Server 2012 R2', 
 (
 WindowsMajorVersion.WINDOWS_MAJOR_VERSION_10, WindowsMinorVersion.WINDOWS_MINOR_VERSION_0): 'Windows 10 or Windows Server 2016'}

class AVPAIRType(enum.Enum):
    MsvAvEOL = 0
    MsvAvNbComputerName = 1
    MsvAvNbDomainName = 2
    MsvAvDnsComputerName = 3
    MsvAvDnsDomainName = 4
    MsvAvDnsTreeName = 5
    MsvAvFlags = 6
    MsvAvTimestamp = 7
    MsvAvSingleHost = 8
    MsvAvTargetName = 9
    MsvChannelBindings = 10


class AVPairs(collections.UserDict):
    __doc__ = '\n\tAVPairs is a dictionary-like object that stores the "AVPair list" in a key -value format where key is an AVPAIRType object and value is the corresponding object defined by the MSDN documentation. Usually it\'s string but can be other object as well\n\t'

    def __init__(self, data=None):
        collections.UserDict.__init__(self, data)

    @staticmethod
    def from_bytes(bbuff):
        return AVPairs.from_buffer(io.BytesIO(bbuff))

    @staticmethod
    def from_buffer(buff):
        avp = AVPairs()
        while True:
            avId = AVPAIRType(int.from_bytes((buff.read(2)), byteorder='little', signed=False))
            AvLen = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
            if avId == AVPAIRType.MsvAvEOL:
                break
            elif avId in [AVPAIRType.MsvAvNbComputerName,
             AVPAIRType.MsvAvNbDomainName,
             AVPAIRType.MsvAvDnsComputerName,
             AVPAIRType.MsvAvDnsDomainName,
             AVPAIRType.MsvAvDnsTreeName,
             AVPAIRType.MsvAvTargetName]:
                avp[avId] = buff.read(AvLen).decode('utf-16le')
            else:
                avp[avId] = buff.read(AvLen)

        return avp

    def to_bytes(self):
        t = b''
        for av in self.data:
            t += AVPair(data=(self.data[av]), type=av).to_bytes()

        t += AVPair(data='', type=(AVPAIRType.MsvAvEOL)).to_bytes()
        return t


class AVPair:

    def __init__(self, data=None, type=None):
        self.type = type
        self.data = data

    def to_bytes(self):
        t = self.type.value.to_bytes(2, byteorder='little', signed=False)
        t += len(self.data.encode('utf-16le')).to_bytes(2, byteorder='little', signed=False)
        t += self.data.encode('utf-16le')
        return t


class Fields:

    def __init__(self, length, offset, maxLength=None):
        self.length = length
        self.maxLength = length if maxLength is None else maxLength
        self.offset = offset

    @staticmethod
    def from_bytes(bbuff):
        return Fields.from_buffer(io.BytesIO(bbuff))

    @staticmethod
    def from_buffer(buff):
        length = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        maxLength = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        offset = int.from_bytes((buff.read(4)), byteorder='little', signed=False)
        return Fields(length, offset, maxLength=maxLength)

    def to_bytes(self):
        return self.length.to_bytes(2, byteorder='little', signed=False) + self.maxLength.to_bytes(2, byteorder='little', signed=False) + self.offset.to_bytes(4, byteorder='little', signed=False)


class Version:

    def __init__(self):
        self.ProductMajorVersion = None
        self.ProductMinorVersion = None
        self.ProductBuild = None
        self.Reserved = None
        self.NTLMRevisionCurrent = None
        self.WindowsProduct = None

    def to_bytes(self):
        t = self.ProductMajorVersion.value.to_bytes(1, byteorder='little', signed=False)
        t += self.ProductMinorVersion.value.to_bytes(1, byteorder='little', signed=False)
        t += self.ProductBuild.to_bytes(2, byteorder='little', signed=False)
        t += self.Reserved.to_bytes(3, byteorder='little', signed=False)
        t += self.NTLMRevisionCurrent.value.to_bytes(1, byteorder='little', signed=False)
        return t

    @staticmethod
    def from_bytes(bbuff):
        return Version.from_buffer(io.BytesIO(bbuff))

    @staticmethod
    def from_buffer(buff):
        v = Version()
        v.ProductMajorVersion = WindowsMajorVersion(int.from_bytes((buff.read(1)), byteorder='little', signed=False))
        v.ProductMinorVersion = WindowsMinorVersion(int.from_bytes((buff.read(1)), byteorder='little', signed=False))
        v.ProductBuild = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        v.Reserved = int.from_bytes((buff.read(3)), byteorder='little', signed=False)
        v.NTLMRevisionCurrent = NTLMRevisionCurrent(int.from_bytes((buff.read(1)), byteorder='little', signed=False))
        v.WindowsProduct = WindowsProduct[(v.ProductMajorVersion, v.ProductMinorVersion)]
        return v

    def __repr__(self):
        t = '== NTLMVersion ==\r\n'
        t += 'ProductMajorVersion  : %s\r\n' % repr(self.ProductMajorVersion.name)
        t += 'ProductMinorVersion  : %s\r\n' % repr(self.ProductMinorVersion.name)
        t += 'ProductBuild         : %s\r\n' % repr(self.ProductBuild)
        t += 'WindowsProduct       : %s\r\n' % repr(self.WindowsProduct)
        return t


NTLMServerTemplates = {'Windows2003': {'flags':NegotiateFlags.NEGOTIATE_56 | NegotiateFlags.NEGOTIATE_128 | NegotiateFlags.NEGOTIATE_VERSION | NegotiateFlags.NEGOTIATE_TARGET_INFO | NegotiateFlags.NEGOTIATE_EXTENDED_SESSIONSECURITY | NegotiateFlags.TARGET_TYPE_DOMAIN | NegotiateFlags.NEGOTIATE_NTLM | NegotiateFlags.REQUEST_TARGET | NegotiateFlags.NEGOTIATE_UNICODE, 
                 'version':Version.from_bytes(b'\x05\x02\xce\x0e\x00\x00\x00\x0f'), 
                 'targetinfo':AVPairs({AVPAIRType.MsvAvNbDomainName: 'SMB', 
                  AVPAIRType.MsvAvNbComputerName: 'SMB-TOOLKIT', 
                  AVPAIRType.MsvAvDnsDomainName: 'smb.local', 
                  AVPAIRType.MsvAvDnsComputerName: 'server2003.smb.local', 
                  AVPAIRType.MsvAvDnsTreeName: 'smb.local'}), 
                 'targetname':'SMB'}}

class NTLMAuthenticate:

    def __init__(self, _use_NTLMv2=True):
        self.Signature = None
        self.MessageType = None
        self.LmChallengeResponseFields = None
        self.NtChallengeResponseFields = None
        self.DomainNameFields = None
        self.UserNameFields = None
        self.WorkstationFields = None
        self.EncryptedRandomSessionKeyFields = None
        self.NegotiateFlags = None
        self.Version = None
        self.MIC = None
        self.Payload = None
        self.LMChallenge = None
        self.NTChallenge = None
        self.DomainName = None
        self.UserName = None
        self.Workstation = None
        self.EncryptedRandomSession = None
        self._use_NTLMv2 = _use_NTLMv2

    @staticmethod
    def from_bytes(bbuff, _use_NTLMv2=True):
        return NTLMAuthenticate.from_buffer((io.BytesIO(bbuff)), _use_NTLMv2=_use_NTLMv2)

    @staticmethod
    def from_buffer(buff, _use_NTLMv2=True):
        auth = NTLMAuthenticate(_use_NTLMv2)
        auth.Signature = buff.read(8).decode('ascii')
        auth.MessageType = int.from_bytes((buff.read(4)), byteorder='little', signed=False)
        auth.LmChallengeResponseFields = Fields.from_buffer(buff)
        auth.NtChallengeResponseFields = Fields.from_buffer(buff)
        auth.DomainNameFields = Fields.from_buffer(buff)
        auth.UserNameFields = Fields.from_buffer(buff)
        auth.WorkstationFields = Fields.from_buffer(buff)
        auth.EncryptedRandomSessionKeyFields = Fields.from_buffer(buff)
        auth.NegotiateFlags = NegotiateFlags(int.from_bytes((buff.read(4)), byteorder='little', signed=False))
        if auth.NegotiateFlags & NegotiateFlags.NEGOTIATE_VERSION:
            auth.Version = Version.from_buffer(buff)
        if auth.NegotiateFlags & NegotiateFlags.NEGOTIATE_ALWAYS_SIGN:
            auth.MIC = int.from_bytes((buff.read(16)), byteorder='little', signed=False)
        currPos = buff.tell()
        if auth._use_NTLMv2 and auth.NtChallengeResponseFields.length > 24:
            buff.seek(auth.LmChallengeResponseFields.offset, io.SEEK_SET)
            auth.LMChallenge = LMv2Response.from_buffer(buff)
            buff.seek(auth.NtChallengeResponseFields.offset, io.SEEK_SET)
            auth.NTChallenge = NTLMv2Response.from_buffer(buff)
        else:
            buff.seek(auth.LmChallengeResponseFields.offset, io.SEEK_SET)
            auth.LMChallenge = LMResponse.from_buffer(buff)
            buff.seek(auth.NtChallengeResponseFields.offset, io.SEEK_SET)
            auth.NTChallenge = NTLMv1Response.from_buffer(buff)
        buff.seek(auth.DomainNameFields.offset, io.SEEK_SET)
        auth.DomainName = buff.read(auth.DomainNameFields.length).decode('utf-16le')
        buff.seek(auth.UserNameFields.offset, io.SEEK_SET)
        auth.UserName = buff.read(auth.UserNameFields.length).decode('utf-16le')
        buff.seek(auth.WorkstationFields.offset, io.SEEK_SET)
        auth.Workstation = buff.read(auth.WorkstationFields.length).decode('utf-16le')
        buff.seek(auth.EncryptedRandomSessionKeyFields.offset, io.SEEK_SET)
        auth.EncryptedRandomSession = buff.read(auth.EncryptedRandomSessionKeyFields.length).decode('utf-16le')
        buff.seek(currPos, io.SEEK_SET)
        return auth

    def __repr__(self):
        t = '== NTLMAuthenticate ==\r\n'
        t += 'Signature     : %s\r\n' % repr(self.Signature)
        t += 'MessageType   : %s\r\n' % repr(self.MessageType)
        t += 'NegotiateFlags: %s\r\n' % repr(self.NegotiateFlags)
        t += 'Version       : %s\r\n' % repr(self.Version)
        t += 'MIC           : %s\r\n' % repr(self.MIC)
        t += 'LMChallenge   : %s\r\n' % repr(self.LMChallenge)
        t += 'NTChallenge   : %s\r\n' % repr(self.NTChallenge)
        t += 'DomainName    : %s\r\n' % repr(self.DomainName)
        t += 'UserName      : %s\r\n' % repr(self.UserName)
        t += 'Workstation   : %s\r\n' % repr(self.Workstation)
        t += 'EncryptedRandomSession: %s\r\n' % repr(self.EncryptedRandomSession)
        return t


class LMResponse:

    def __init__(self):
        self.Response = None
        self.raw = None

    @staticmethod
    def from_bytes(bbuff):
        return LMResponse.from_buffer(io.BytesIO(bbuff))

    @staticmethod
    def from_buffer(buff):
        t = LMResponse()
        t.Response = buff.read(24).hex()
        return t

    def __repr__(self):
        t = '== LMResponse ==\r\n'
        t += 'Response: %s\r\n' % repr(self.Response)
        return t


class LMv2Response:

    def __init__(self):
        self.Response = None
        self.ChallengeFromClinet = None

    @staticmethod
    def from_bytes(bbuff):
        return LMv2Response.from_buffer(io.BytesIO(bbuff))

    @staticmethod
    def from_buffer(buff):
        t = LMv2Response()
        t.Response = buff.read(16).hex()
        t.ChallengeFromClinet = buff.read(8).hex()
        return t

    def __repr__(self):
        t = '== LMv2Response ==\r\n'
        t += 'Response: %s\r\n' % repr(self.Response)
        t += 'ChallengeFromClinet: %s\r\n' % repr(self.ChallengeFromClinet)
        return t


class NTLMv1Response:

    def __init__(self):
        self.Response = None

    @staticmethod
    def from_bytes(bbuff):
        return NTLMv1Response.from_buffer(io.BytesIO(bbuff))

    @staticmethod
    def from_buffer(buff):
        t = NTLMv1Response()
        t.Response = buff.read(24).hex()
        return t

    def __repr__(self):
        t = '== NTLMv1Response ==\r\n'
        t += 'Response: %s\r\n' % repr(self.Response)
        return t


class NTLMv2Response:

    def __init__(self):
        self.Response = None
        self.ChallengeFromClinet = None
        self.ChallengeFromClinet_hex = None

    @staticmethod
    def from_bytes(bbuff):
        return NTLMv2Response.from_buffer(io.BytesIO(bbuff))

    @staticmethod
    def from_buffer(buff):
        t = NTLMv2Response()
        t.Response = buff.read(16).hex()
        pos = buff.tell()
        t.ChallengeFromClinet = NTLMv2ClientChallenge.from_buffer(buff)
        pos2 = buff.tell()
        challengeLength = pos2 - pos
        buff.seek(pos, io.SEEK_SET)
        t.ChallengeFromClinet_hex = buff.read(challengeLength).hex()
        return t

    def __repr__(self):
        t = '== NTLMv2Response ==\r\n'
        t += 'Response           : %s\r\n' % repr(self.Response)
        t += 'ChallengeFromClinet: %s\r\n' % repr(self.ChallengeFromClinet)
        return t


class NTLMv2ClientChallenge:

    def __init__(self):
        self.RespType = None
        self.HiRespType = None
        self.Reserved1 = None
        self.Reserved2 = None
        self.TimeStamp = None
        self.ChallengeFromClient = None
        self.Reserved3 = None
        self.Details = None
        self.Reserved4 = None

    @staticmethod
    def from_bytes(bbuff):
        return NTLMv2ClientChallenge.from_buffer(io.BytesIO(bbuff))

    @staticmethod
    def from_buffer(buff):
        cc = NTLMv2ClientChallenge()
        cc.RespType = int.from_bytes((buff.read(1)), byteorder='little', signed=False)
        cc.HiRespType = int.from_bytes((buff.read(1)), byteorder='little', signed=False)
        cc.Reserved1 = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        cc.Reserved2 = int.from_bytes((buff.read(4)), byteorder='little', signed=False)
        cc.TimeStamp = timestamp2datetime(buff.read(8))
        cc.ChallengeFromClient = buff.read(8).hex()
        cc.Reserved3 = int.from_bytes((buff.read(4)), byteorder='little', signed=False)
        cc.Details = AVPairs.from_buffer(buff)
        cc.Reserved3 = int.from_bytes((buff.read(4)), byteorder='little', signed=False)
        return cc

    def __repr__(self):
        t = '== NTLMv2ClientChallenge ==\r\n'
        t += 'RespType           : %s\r\n' % repr(self.RespType)
        t += 'TimeStamp          : %s\r\n' % repr(self.TimeStamp)
        t += 'ChallengeFromClient: %s\r\n' % repr(self.ChallengeFromClient)
        t += 'Details            : %s\r\n' % repr(self.Details)
        return t


class NTLMChallenge:

    def __init__(self):
        self.Signature = 'NTLMSSP\x00'
        self.MessageType = 2
        self.TargetNameFields = None
        self.NegotiateFlags = None
        self.ServerChallenge = None
        self.Reserved = (b'\x00\x00\x00\x00\x00\x00\x00\x00').hex()
        self.TargetInfoFields = None
        self.Version = None
        self.Payload = None
        self.TargetName = None
        self.TargetInfo = None

    @staticmethod
    def construct_from_template(templateName, challenge=os.urandom(8).hex(), ess=True):
        version = NTLMServerTemplates[templateName]['version']
        challenge = challenge
        targetName = NTLMServerTemplates[templateName]['targetname']
        targetInfo = NTLMServerTemplates[templateName]['targetinfo']
        targetInfo = NTLMServerTemplates[templateName]['targetinfo']
        flags = NTLMServerTemplates[templateName]['flags']
        if ess:
            flags |= NegotiateFlags.NEGOTIATE_EXTENDED_SESSIONSECURITY
        else:
            flags &= ~NegotiateFlags.NEGOTIATE_EXTENDED_SESSIONSECURITY
        return NTLMChallenge.construct(challenge=challenge, targetName=targetName, targetInfo=targetInfo, version=version, flags=flags)

    @staticmethod
    def construct(challenge=os.urandom(8), targetName=None, targetInfo=None, version=None, flags=None):
        t = NTLMChallenge()
        t.NegotiateFlags = flags
        t.Version = version
        t.ServerChallenge = challenge
        t.TargetName = targetName
        t.TargetInfo = targetInfo
        t.TargetNameFields = Fields(len(t.TargetName.encode('utf-16le')), 56)
        t.TargetInfoFields = Fields(len(t.TargetInfo.to_bytes()), 56 + len(t.TargetName.encode('utf-16le')))
        t.Payload = t.TargetName.encode('utf-16le')
        t.Payload += t.TargetInfo.to_bytes()
        return t

    def to_bytes(self):
        tn = self.TargetName.encode('utf-16le')
        ti = self.TargetInfo.to_bytes()
        buff = self.Signature.encode('ascii')
        buff += self.MessageType.to_bytes(4, byteorder='little', signed=False)
        buff += self.TargetNameFields.to_bytes()
        buff += self.NegotiateFlags.to_bytes(4, byteorder='little', signed=False)
        buff += bytes.fromhex(self.ServerChallenge)
        buff += bytes.fromhex(self.Reserved)
        buff += self.TargetInfoFields.to_bytes()
        buff += self.Version.to_bytes()
        buff += self.Payload
        return buff

    def __repr__(self):
        t = '== NTLMChallenge ==\r\n'
        t += 'Signature      : %s\r\n' % repr(self.Signature)
        t += 'MessageType    : %s\r\n' % repr(self.MessageType)
        t += 'ServerChallenge: %s\r\n' % repr(self.ServerChallenge)
        t += 'TargetName     : %s\r\n' % repr(self.TargetName)
        t += 'TargetInfo     : %s\r\n' % repr(self.TargetInfo)
        return t

    def toBase64(self):
        return base64.b64encode(self.to_bytes()).decode('ascii')


class NTLMNegotiate:

    def __init__(self):
        self.Signature = None
        self.MessageType = None
        self.NegotiateFlags = None
        self.DomainNameFields = None
        self.WorkstationFields = None
        self.Version = None
        self.Payload = None
        self.Domain = None
        self.Workstation = None

    @staticmethod
    def from_bytes(bbuff):
        return NTLMNegotiate.from_buffer(io.BytesIO(bbuff))

    @staticmethod
    def from_buffer(buff):
        t = NTLMNegotiate()
        t.Signature = buff.read(8).decode('ascii')
        t.MessageType = int.from_bytes((buff.read(4)), byteorder='little', signed=False)
        t.NegotiateFlags = NegotiateFlags(int.from_bytes((buff.read(4)), byteorder='little', signed=False))
        t.DomainNameFields = Fields.from_buffer(buff)
        t.WorkstationFields = Fields.from_buffer(buff)
        if t.NegotiateFlags & NegotiateFlags.NEGOTIATE_VERSION:
            t.Version = buff.read(8)
        currPos = buff.tell()
        if t.DomainNameFields.length != 0:
            buff.seek(t.DomainNameFields.offset, io.SEEK_SET)
            raw_data = buff.read(t.WorkstationFields.length)
            try:
                t.Domain = raw_data.decode('utf-16le')
            except UnicodeDecodeError:
                t.Domain = raw_data.decode('utf-8')

        if t.WorkstationFields.length != 0:
            buff.seek(t.WorkstationFields.offset, io.SEEK_SET)
            raw_data = buff.read(t.WorkstationFields.length)
            try:
                t.Workstation = raw_data.decode('utf-16le')
            except UnicodeDecodeError:
                t.Workstation = raw_data.decode('utf-8')

        buff.seek(currPos, io.SEEK_SET)
        return t

    def __repr__(self):
        t = '== NTLMNegotiate ==\r\n'
        t += 'Signature  : %s\r\n' % repr(self.Signature)
        t += 'MessageType: %s\r\n' % repr(self.MessageType)
        t += 'NegotiateFlags: %s\r\n' % repr(self.NegotiateFlags)
        t += 'Version    : %s\r\n' % repr(self.Version)
        t += 'Domain     : %s\r\n' % repr(self.Domain)
        t += 'Workstation: %s\r\n' % repr(self.Workstation)
        return t

    def contrct(self):
        pass


class NTLMAuthMode(enum.Enum):
    CLIENT = enum.auto()
    SERVER = enum.auto()


class NTLMAUTHHandler:

    def __init__(self, mode=AUTHModuleMode.SERVER, credentials={}):
        self.mode = mode
        self.use_NTLMv2 = None
        self.use_Extended_security = None
        self.serverTemplateName = None
        self.challenge = None
        self.ntlmNegotiate = None
        self.ntlmChallenge = None
        self.ntlmAuthenticate = None
        self.credentials = credentials
        self.client_credentials = None
        self.SessionBaseKey = None
        self.KeyExchangeKey = None

    def setup_defaults(self):
        self.use_NTLMv2 = True
        self.use_Extended_security = True
        self.serverTemplateName = 'Windows2003'
        self.challenge = 'AAAAAAAAAAAAAAAA'

    def setup(self, settings=None):
        if not settings:
            self.setup_defaults()
            return
        else:
            self.use_NTLMv2 = not settings['ntlm_downgrade']
            self.use_Extended_security = settings['extended_security']
            self.challenge = settings['challenge']
            if settings['template']['name'].upper() == 'CUSTOM':
                NTLMServerTemplates['CUSTOM'] = {'flags':settings['template']['flags'],  'version':settings['template']['version'], 
                 'targetinfo':settings['template']['targetinfo'], 
                 'targetname':settings['template']['targetname']}
            else:
                if settings['template']['name'] in NTLMServerTemplates:
                    self.serverTemplateName = settings['template']['name']

    def do_auth(self, authData):
        if self.ntlmNegotiate is None:
            self.ntlmNegotiate = NTLMNegotiate.from_bytes(authData)
            self.ntlmChallenge = NTLMChallenge.construct_from_template((self.serverTemplateName), challenge=(self.challenge), ess=(self.use_Extended_security))
            return (AuthResult.CONTINUE, self.ntlmChallenge.to_bytes())
        if self.ntlmAuthenticate is None:
            self.ntlmAuthenticate = NTLMAuthenticate.from_bytes(authData, self.use_NTLMv2)
            creds = NTLMCredentials.construct(self.ntlmNegotiate, self.ntlmChallenge, self.ntlmAuthenticate)
            print(creds)
            auth_credential = creds[0]
            if auth_credential.verify(self.credentials):
                return (
                 AuthResult.FAIL, auth_credential)
            return (AuthResult.FAIL, auth_credential)
        else:
            raise Exception('Too many calls to do_AUTH function!')


class NTLMCredentials:

    @staticmethod
    def construct(ntlmNegotiate, ntlmChallenge, ntlmAuthenticate):
        if isinstance(ntlmAuthenticate.NTChallenge, NTLMv2Response):
            creds = netntlmv2()
            creds.username = ntlmAuthenticate.UserName
            creds.domain = ntlmAuthenticate.DomainName
            creds.ServerChallenge = ntlmChallenge.ServerChallenge
            creds.ClientResponse = ntlmAuthenticate.NTChallenge.Response
            creds.ChallengeFromClinet = ntlmAuthenticate.NTChallenge.ChallengeFromClinet_hex
            creds2 = netlmv2()
            creds2.username = ntlmAuthenticate.UserName
            creds2.domain = ntlmAuthenticate.DomainName
            creds2.ServerChallenge = ntlmChallenge.ServerChallenge
            creds2.ClientResponse = ntlmAuthenticate.LMChallenge.Response
            creds2.ChallengeFromClinet = ntlmAuthenticate.LMChallenge.ChallengeFromClinet
            return [creds, creds2]
        if ntlmAuthenticate.NegotiateFlags & NegotiateFlags.NEGOTIATE_EXTENDED_SESSIONSECURITY:
            creds = netntlm_ess()
            creds.username = ntlmAuthenticate.UserName
            creds.domain = ntlmAuthenticate.DomainName
            creds.ServerChallenge = ntlmChallenge.ServerChallenge
            creds.ClientResponse = ntlmAuthenticate.NTChallenge.Response
            creds.ChallengeFromClinet = ntlmAuthenticate.LMChallenge.Response
            return [
             creds]
        creds = netntlm()
        creds.username = ntlmAuthenticate.UserName
        creds.domain = ntlmAuthenticate.DomainName
        creds.ServerChallenge = ntlmChallenge.ServerChallenge
        creds.ClientResponse = ntlmAuthenticate.NTChallenge.Response
        if ntlmAuthenticate.NTChallenge.Response == ntlmAuthenticate.LMChallenge.Response:
            return [creds]
        creds2 = netlm()
        creds2.username = ntlmAuthenticate.UserName
        creds2.domain = ntlmAuthenticate.DomainName
        creds2.ServerChallenge = ntlmChallenge.ServerChallenge
        creds2.ClientResponse = ntlmAuthenticate.LMChallenge.Response
        return [creds2, creds]


class netlm:

    def __init__(self):
        self.username = None
        self.domain = None
        self.ServerChallenge = None
        self.ClientResponse = None

    def to_credential(self):
        cred = Credential('netLM', username=(self.username),
          fullhash=('%s:$NETLM$%s$%s' % (self.username, self.ServerChallenge, self.ClientResponse)))
        return cred

    def verify(self, creds, credtype='plain'):
        """
                Verifies the authentication data against the user credentials
                Be careful! If the credtype is 'hash' then LM hash is expected!
                :param creds: dictionary containing the domain, user, hash/password
                :param credtype: can be 'plain' or 'hash' this indicates what type of credential lookup to perform
                :return: bool
                """
        if creds is None:
            return True
        elif self.domain not in creds:
            return False
            if self.username not in creds[self.domain]:
                return False
            if credtype == 'plain':
                lm_hash = LMOWFv1(creds[self.domain][self.username])
        elif credtype == 'hash':
            lm_hash = bytes.fromhex(creds[self.domain][self.username])
        else:
            raise Exception('Unknown cred type!')
        calc_response = DESL(lm_hash, self.ServerChallenge)
        return self.ClientResponse == calc_response.hex()


class netlmv2:

    def __init__(self):
        self.username = None
        self.domain = None
        self.ServerChallenge = None
        self.ClientResponse = None
        self.ChallengeFromClinet = None

    def to_credential(self):
        cred = Credential('netLMv2',
          username=(self.username),
          fullhash=('$NETLMv2$%s$%s$%s$%s' % (self.username, self.ServerChallenge, self.ClientResponse, self.ChallengeFromClinet)))
        return cred

    def verify(self, creds, credtype='plain'):
        """
                Verifies the authentication data against the user credentials
                :param creds: dictionary containing the domain, user, hash/password
                :param credtype: can be 'plain' or 'hash' this indicates what type of credential lookup to perform
                :return: bool
                """
        if creds is None:
            return True
        elif self.domain not in creds:
            return False
            if self.username not in creds[self.domain]:
                return False
            if credtype == 'plain':
                lm_hash = LMOWFv2(creds[self.domain][self.username], self.username, self.domain)
        elif credtype == 'hash':
            lm_hash = LMOWFv2(None, self.username, self.domain, bytes.fromhex(creds[self.domain][self.username]))
        else:
            raise Exception('Unknown cred type!')
        hm = hmac_md5(lm_hash)
        hm.update(bytes.fromhex(self.ServerChallenge))
        hm.update(bytes.fromhex(self.ChallengeFromClinet))
        return self.ClientResponse == hm.hexdigest()


class netntlm_ess:

    def __init__(self):
        self.username = None
        self.domain = None
        self.ServerChallenge = None
        self.ClientResponse = None
        self.ChallengeFromClinet = None

    def to_credential(self):
        cred = Credential('netNTLMv1-ESS',
          username=(self.username),
          fullhash=('%s::%s:%s:%s:%s' % (self.username, self.domain, self.ChallengeFromClinet, self.ClientResponse, self.ServerChallenge)))
        return cred

    def calc_session_base_key(self, creds, credtype='plain'):
        if credtype == 'plain':
            nt_hash = NTOWFv1(creds[self.domain][self.username])
        else:
            if credtype == 'hash':
                nt_hash = bytes.fromhex(creds[self.domain][self.username])
            else:
                raise Exception('Unknown cred type!')
        session_base_key = md4(nt_hash).digest()
        return session_base_key

    def verify(self, creds, credtype='plain'):
        """
                Verifies the authentication data against the user credentials
                :param creds: dictionary containing the domain, user, hash/password
                :param credtype: can be 'plain' or 'hash' this indicates what type of credential lookup to perform
                :return: bool
                """
        if creds is None:
            return True
        elif self.domain not in creds:
            return False
            if self.username not in creds[self.domain]:
                return False
            if credtype == 'plain':
                nt_hash = NTOWFv1(creds[self.domain][self.username])
        elif credtype == 'hash':
            nt_hash = bytes.fromhex(creds[self.domain][self.username])
        else:
            raise Exception('Unknown cred type!')
        temp_1 = md5(bytes.fromhex(self.ServerChallenge) + bytes.fromhex(self.ChallengeFromClinet)[:8]).digest()
        calc_response = DESL(nt_hash, temp_1[:8])
        return calc_response == bytes.fromhex(self.ClientResponse)


class netntlm:

    def __init__(self):
        self.username = None
        self.domain = None
        self.ServerChallenge = None
        self.ClientResponse = None

    def to_credential(self):
        cred = Credential('netNTLMv1', username=(self.username),
          fullhash=('%s:$NETNTLM$%s$%s' % (self.username, self.ServerChallenge, self.ClientResponse)))
        return cred

    def calc_session_base_key(self, creds, credtype='plain'):
        if credtype == 'plain':
            nt_hash = NTOWFv1(creds[self.domain][self.username])
        else:
            if credtype == 'hash':
                nt_hash = bytes.fromhex(creds[self.domain][self.username])
            else:
                raise Exception('Unknown cred type!')
        session_base_key = md4(nt_hash).digest()
        return session_base_key

    def verify(self, creds, credtype='plain'):
        """
                Verifies the authentication data against the user credentials
                :param creds: dictionary containing the domain, user, hash/password
                :param credtype: can be 'plain' or 'hash' this indicates what type of credential lookup to perform
                :return: bool
                """
        if creds is None:
            return True
        elif self.domain not in creds:
            return False
            if self.username not in creds[self.domain]:
                return False
            if credtype == 'plain':
                nt_hash = NTOWFv1(creds[self.domain][self.username])
        elif credtype == 'hash':
            nt_hash = bytes.fromhex(creds[self.domain][self.username])
        else:
            raise Exception('Unknown cred type!')
        return DESL(nt_hash, self.ServerChallenge) == bytes.fromhex(self.ClientResponse)


class netntlmv2:

    def __init__(self):
        self.username = None
        self.domain = None
        self.ServerChallenge = None
        self.ClientResponse = None
        self.ChallengeFromClinet = None

    def to_credential(self):
        cred = Credential('netNTLMv2',
          username=(self.username),
          domain=(self.domain),
          fullhash=('%s::%s:%s:%s:%s' % (self.username, self.domain, self.ServerChallenge, self.ClientResponse, self.ChallengeFromClinet)))
        return cred

    def calc_session_base_key(self, creds, credtype='plain'):
        if credtype == 'plain':
            nt_hash = NTOWFv2(creds[self.domain][self.username], self.username, self.domain)
        else:
            if credtype == 'hash':
                nt_hash = NTOWFv2(None, self.username, self.domain, bytes.fromhex(creds[self.domain][self.username]))
            else:
                raise Exception('Unknown cred type!')
        hm = hmac_md5(nt_hash)
        hm.update(self.ClientResponse)
        return hm.digest()

    def verify(self, creds, credtype='plain'):
        """
                Verifies the authentication data against the user credentials
                :param creds: dictionary containing the domain, user, hash/password
                :param credtype: can be 'plain' or 'hash' this indicates what type of credential lookup to perform 
                :return: bool
                """
        if creds is None:
            return True
        elif self.domain not in creds:
            return False
            if self.username not in creds[self.domain]:
                return False
            if credtype == 'plain':
                nt_hash = NTOWFv2(creds[self.domain][self.username], self.username, self.domain)
        elif credtype == 'hash':
            nt_hash = NTOWFv2(None, self.username, self.domain, bytes.fromhex(creds[self.domain][self.username]))
        else:
            raise Exception('Unknown cred type!')
        hm = hmac_md5(nt_hash)
        hm.update(bytes.fromhex(self.ServerChallenge))
        hm.update(bytes.fromhex(self.ChallengeFromClinet))
        return self.ClientResponse == hm.hexdigest()


def LMOWFv1(password):
    LM_SECRET = b'KGS!@#$%'
    t1 = password[:14].ljust(14, '\x00').upper()
    d = DES(t1[:7].encode('ascii'))
    r1 = d.encrypt(LM_SECRET)
    d = DES(t1[7:].encode('ascii'))
    r2 = d.encrypt(LM_SECRET)
    return r1 + r2


def NTOWFv1(password):
    return md4(password.encode('utf-16le')).digest()


def LMOWFv2(Passwd, User, UserDom, PasswdHash=None):
    return NTOWFv2(Passwd, User, UserDom, PasswdHash)


def NTOWFv2(Passwd, User, UserDom, PasswdHash=None):
    if PasswdHash is not None:
        fp = hmac_md5(PasswdHash)
    else:
        fp = hmac_md5(NTOWFv1(Passwd))
    fp.update((User.upper() + UserDom).encode('utf-16le'))
    return fp.digest()


def DESL(K, D):
    """
        Indicates the encryption of an 8-byte data item D with the 16-byte key K
        using the Data Encryption Standard Long (DESL) algorithm.
        The result is 24 bytes in length.
        :param K:
        :param D:
        :return:
        """
    if len(K) != 16:
        raise Exception('K MUST be 16 bytes long')
    if len(D) != 8:
        raise Exception('D MUST be 8 bytes long')
    res = b''
    print(len(K[:6]))
    res += DES(K[:7]).encrypt(D)
    res += DES(K[7:14]).encrypt(D)
    res += DES(K[14:] + b'\x00\x00\x00\x00\x00').encrypt(D)
    return res