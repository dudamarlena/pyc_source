# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\protocols\SMB\SMB2.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 43569 bytes
import io, os, sys, enum, uuid, traceback
from responder3.protocols.SMB.ntstatus import *
from responder3.protocols.SMB.utils import *

class SMB2HeaderFlag(enum.IntFlag):
    SMB2_FLAGS_SERVER_TO_REDIR = 1
    SMB2_FLAGS_ASYNC_COMMAND = 2
    SMB2_FLAGS_RELATED_OPERATIONS = 4
    SMB2_FLAGS_SIGNED = 8
    SMB2_FLAGS_PRIORITY_MASK = 112
    SMB2_FLAGS_DFS_OPERATIONS = 268435456
    SMB2_FLAGS_REPLAY_OPERATION = 536870912


class SMB2Command(enum.Enum):
    NEGOTIATE = 0
    SESSION_SETUP = 1
    LOGOFF = 2
    TREE_CONNECT = 3
    TREE_DISCONNECT = 4
    CREATE = 5
    CLOSE = 6
    FLUSH = 7
    READ = 8
    WRITE = 9
    LOCK = 10
    IOCTL = 11
    CANCEL = 12
    ECHO = 13
    QUERY_DIRECTORY = 14
    CHANGE_NOTIFY = 15
    QUERY_INFO = 16
    SET_INFO = 17
    OPLOCK_BREAK = 18


class SMB2Header_ASYNC:

    def __init__(self):
        self.ProtocolId = None
        self.StructureSize = None
        self.CreditCharge = None
        self.Status = None
        self.Command = None
        self.Credit = None
        self.Flags = None
        self.NextCommand = None
        self.MessageId = None
        self.AsyncId = None
        self.SessionId = None
        self.Signature = None

    @staticmethod
    def from_buffer(buff):
        hdr = SMB2Header_ASYNC()
        hdr.ProtocolId = buff.read(4)
        assert hdr.ProtocolId == b'\xfeSMB'
        hdr.StructureSize = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        assert hdr.StructureSize == 64
        hdr.CreditCharge = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        hdr.Status = NTStatus(int.from_bytes((buff.read(4)), byteorder='little', signed=False))
        hdr.Command = SMB2Command(int.from_bytes((buff.read(2)), byteorder='little', signed=False))
        hdr.Credit = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        hdr.Flags = SMB2HeaderFlag(int.from_bytes((buff.read(4)), byteorder='little', signed=False))
        hdr.NextCommand = int.from_bytes((buff.read(4)), byteorder='little', signed=False)
        hdr.MessageId = int.from_bytes((buff.read(8)), byteorder='little', signed=False)
        hdr.AsyncId = buff.read(8)
        hdr.SessionId = buff.read(8)
        hdr.Signature = buff.read(16)
        return hdr

    @staticmethod
    def construct(cmd, flags, msgid, Credit=0, NextCommand=0, CreditCharge=0, Signature=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', AsyncId=b'\x00\x00\x00\x00\x00\x00\x00\x00', SessionId=b'\x00\x00\x00\x00\x00\x00\x00\x00', status=NTStatus.STATUS_SUCCESS):
        hdr = SMB2Header_ASYNC()
        hdr.ProtocolId = b'\xfeSMB'
        hdr.StructureSize = 64
        hdr.CreditCharge = CreditCharge
        hdr.Status = status
        hdr.Command = cmd
        hdr.Credit = Credit
        hdr.Flags = flags
        hdr.NextCommand = NextCommand
        hdr.MessageId = msgid
        hdr.AsyncId = AsyncId
        hdr.SessionId = SessionId
        hdr.Signature = Signature
        return hdr

    def to_bytes(self):
        t = self.ProtocolId
        t += self.StructureSize.to_bytes(2, byteorder='little', signed=False)
        t += self.CreditCharge.to_bytes(2, byteorder='little', signed=False)
        t += self.Status.value.to_bytes(4, byteorder='little', signed=False)
        t += self.Command.value.to_bytes(2, byteorder='little', signed=False)
        t += self.Credit.to_bytes(2, byteorder='little', signed=False)
        t += self.Flags.to_bytes(4, byteorder='little', signed=False)
        t += self.NextCommand.to_bytes(4, byteorder='little', signed=False)
        t += self.MessageId.to_bytes(8, byteorder='little', signed=False)
        t += self.AsyncId
        t += self.SessionId
        t += self.Signature
        return t

    def __repr__(self):
        t = '===SMB2 HEADER ASYNC===\r\n'
        t += 'ProtocolId: %s\r\n' % self.ProtocolId
        t += 'StructureSize: %s\r\n' % self.StructureSize
        t += 'CreditCharge: %s\r\n' % self.CreditCharge
        t += 'Status: %s\r\n' % self.Status.name
        t += 'Command: %s\r\n' % self.Command.name
        t += 'Credit: %s\r\n' % self.Credit
        t += 'Flags: %s\r\n' % self.Flags
        t += 'NextCommand: %s\r\n' % self.NextCommand
        t += 'MessageId: %s\r\n' % self.MessageId
        t += 'AsyncId: %s\r\n' % self.AsyncId
        t += 'SessionId: %s\r\n' % self.SessionId
        t += 'Signature: %s\r\n' % self.Signature
        return t


class SMB2Header_SYNC:

    def __init__(self):
        self.ProtocolId = None
        self.StructureSize = None
        self.CreditCharge = None
        self.Status = None
        self.Command = None
        self.Credit = None
        self.Flags = None
        self.NextCommand = None
        self.MessageId = None
        self.Reserved = None
        self.TreeId = None
        self.SessionId = None
        self.Signature = None

    @staticmethod
    def from_buffer(buff):
        hdr = SMB2Header_SYNC()
        hdr.ProtocolId = buff.read(4)
        assert hdr.ProtocolId == b'\xfeSMB'
        hdr.StructureSize = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        assert hdr.StructureSize == 64
        hdr.CreditCharge = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        hdr.Status = NTStatus(int.from_bytes((buff.read(4)), byteorder='little', signed=False))
        hdr.Command = SMB2Command(int.from_bytes((buff.read(2)), byteorder='little', signed=False))
        hdr.Credit = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        hdr.Flags = SMB2HeaderFlag(int.from_bytes((buff.read(4)), byteorder='little', signed=False))
        hdr.NextCommand = int.from_bytes((buff.read(4)), byteorder='little', signed=False)
        hdr.MessageId = int.from_bytes((buff.read(8)), byteorder='little', signed=False)
        hdr.Reserved = buff.read(4)
        hdr.TreeId = buff.read(4)
        hdr.SessionId = buff.read(8)
        hdr.Signature = buff.read(16)
        return hdr

    def to_bytes(self):
        t = self.ProtocolId
        t += self.StructureSize.to_bytes(2, byteorder='little', signed=False)
        t += self.CreditCharge.to_bytes(2, byteorder='little', signed=False)
        t += self.Status.to_bytes(4, byteorder='little', signed=False)
        t += self.Command.to_bytes(2, byteorder='little', signed=False)
        t += self.Credit.to_bytes(2, byteorder='little', signed=False)
        t += self.Flags.to_bytes(4, byteorder='little', signed=False)
        t += self.NextCommand.to_bytes(4, byteorder='little', signed=False)
        t += self.MessageId.to_bytes(8, byteorder='little', signed=False)
        t += self.Reserved
        t += self.TreeId
        t += self.SessionId
        t += self.Signature
        return t

    def __repr__(self):
        t = '===SMB2 HEADER SYNC===\r\n'
        t += 'ProtocolId:    %s\r\n' % self.ProtocolId
        t += 'StructureSize: %s\r\n' % self.StructureSize
        t += 'CreditCharge:  %s\r\n' % self.CreditCharge
        t += 'Status:    %s\r\n' % self.Status.name
        t += 'Command:   %s\r\n' % self.Command.name
        t += 'Credit:    %s\r\n' % self.Credit
        t += 'Flags:     %s\r\n' % self.Flags
        t += 'NextCommand: %s\r\n' % self.NextCommand
        t += 'MessageId: %s\r\n' % self.MessageId
        t += 'Reserved:  %s\r\n' % self.Reserved
        t += 'TreeId:    %s\r\n' % self.TreeId
        t += 'SessionId: %s\r\n' % self.SessionId
        t += 'Signature: %s\r\n' % self.Signature
        return t


class SMB2NotImplementedCommand:

    def __init__(self):
        self.data = None

    @staticmethod
    def from_buffer(buff):
        cmd = SMB2NotImplementedCommand()
        cmd.data = buff.read()
        return cmd

    def __repr__(self):
        t = '=== SMB2NotImplementedCommand ===\r\n'
        t += 'Data: %s\r\n' % repr(self.data)
        return t


class SMB2Message:

    def __init__(self):
        self.type = 2
        self.header = None
        self.command = None

    @staticmethod
    def from_bytes(bbuff):
        return SMB2Message.from_buffer(io.BytesIO(bbuff))

    @staticmethod
    def from_buffer(buff):
        msg = SMB2Message()
        if SMB2Message.isAsync(buff):
            msg.header = SMB2Header_ASYNC.from_buffer(buff)
        else:
            msg.header = SMB2Header_SYNC.from_buffer(buff)
        classname = msg.header.Command.name
        try:
            if SMB2HeaderFlag.SMB2_FLAGS_SERVER_TO_REDIR in msg.header.Flags:
                classname += '_REPLY'
            else:
                classname += '_REQ'
            print(classname)
            class_ = getattr(sys.modules[__name__], classname)
            msg.command = class_.from_buffer(buff)
        except Exception as e:
            try:
                traceback.print_exc()
                print('Could not find command implementation! %s' % str(e))
                msg.command = SMB2NotImplementedCommand.from_buffer(buff)
            finally:
                e = None
                del e

        return msg

    @staticmethod
    def isAsync(buff):
        """
                jumping to the header flags and check if the AYSNC command flag is set
                """
        pos = buff.tell()
        buff.seek(16, io.SEEK_SET)
        flags = SMB2HeaderFlag(int.from_bytes((buff.read(4)), byteorder='little', signed=False))
        buff.seek(pos, io.SEEK_SET)
        return SMB2HeaderFlag.SMB2_FLAGS_ASYNC_COMMAND in flags

    def to_bytes(self):
        t = self.header.to_bytes()
        t += self.command.to_bytes()
        return t

    def __repr__(self):
        t = '== SMBv2 Message =='
        t += repr(self.header)
        t += repr(self.command)
        return t


class NegotiateSecurityMode(enum.IntFlag):
    SMB2_NEGOTIATE_SIGNING_ENABLED = 1
    SMB2_NEGOTIATE_SIGNING_REQUIRED = 2


class NegotiateCapabilities(enum.IntFlag):
    SMB2_GLOBAL_CAP_DFS = 1
    SMB2_GLOBAL_CAP_LEASING = 2
    SMB2_GLOBAL_CAP_LARGE_MTU = 4
    SMB2_GLOBAL_CAP_MULTI_CHANNEL = 8
    SMB2_GLOBAL_CAP_PERSISTENT_HANDLES = 16
    SMB2_GLOBAL_CAP_DIRECTORY_LEASING = 32
    SMB2_GLOBAL_CAP_ENCRYPTION = 64


class NegotiateDialects(enum.Enum):
    SMB202 = 514
    SMB210 = 528
    SMB300 = 768
    SMB302 = 770
    SMB311 = 785


class NEGOTIATE_REQ:

    def __init__(self):
        self.StructureSize = None
        self.DialectCount = None
        self.SecurityMode = None
        self.Reserved = None
        self.Capabilities = None
        self.ClientGuid = None
        self.ClientStartTime = None
        self.NegotiateContextOffset = None
        self.NegotiateContextCount = None
        self.Reserved2 = None
        self.NegotiateContextList = None
        self.Dialects = None

    @staticmethod
    def from_buffer(buff):
        cmd = NEGOTIATE_REQ()
        cmd.StructureSize = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        assert cmd.StructureSize == 36
        cmd.DialectCount = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        assert cmd.DialectCount > 0
        cmd.SecurityMode = NegotiateSecurityMode(int.from_bytes((buff.read(2)), byteorder='little', signed=False))
        cmd.Reserved = buff.read(2)
        cmd.Capabilities = NegotiateCapabilities(int.from_bytes((buff.read(4)), byteorder='little', signed=False))
        cmd.ClientGuid = uuid.UUID(bytes=(buff.read(16)))
        pos = buff.tell()
        buff.seek(8, io.SEEK_CUR)
        cmd.Dialects = []
        for i in range(0, cmd.DialectCount):
            cmd.Dialects.append(NegotiateDialects(int.from_bytes((buff.read(2)), byteorder='little', signed=False)))

        pos_buff_end = buff.tell()
        buff.seek(pos, io.SEEK_SET)
        if NegotiateDialects.SMB311 in cmd.Dialects:
            cmd.NegotiateContextOffset = int.from_bytes((buff.read(4)), byteorder='little', signed=False)
            cmd.NegotiateContextCount = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
            cmd.Reserved2 = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
            cmd.NegotiateContextList = []
            buff.seek(cmd.NegotiateContextOffset, io.SEEK_SET)
            for i in range(0, cmd.NegotiateContextCount):
                cmd.NegotiateContextList.append(SMB2NegotiateContext.from_buffer(buff))
                pad_pos = buff.tell()
                q, m = divmod(pad_pos, 8)
                if m != 0:
                    buff.seek((q + 1) * 8, io.SEEK_SET)

        else:
            cmd.ClientStartTime = wintime2datetime(int.from_bytes((buff.read(8)), byteorder='little', signed=False))
            buff.seek(pos_buff_end, io.SEEK_SET)
        return cmd

    def __repr__(self):
        t = '==== SMB2 NEGOTIATE REQ ====\r\n'
        t += 'StructureSize: %s\r\n' % self.StructureSize
        t += 'DialectCount:  %s\r\n' % self.DialectCount
        t += 'SecurityMode:  %s\r\n' % self.SecurityMode.name
        t += 'Reserved:      %s\r\n' % self.Reserved
        t += 'Capabilities:  %s\r\n' % repr(self.Capabilities)
        t += 'ClientGuid:    %s\r\n' % self.ClientGuid
        if NegotiateDialects.SMB311 in self.Dialects:
            t += 'NegotiateContextOffset:    %s\r\n' % self.NegotiateContextOffset
            t += 'NegotiateContextCount:    %s\r\n' % self.NegotiateContextCount
            t += 'Reserved2:    %s\r\n' % self.Reserved2
            for ctx in self.NegotiateContextList:
                t += repr(ctx)

        else:
            t += 'ClientStartTime:    %s\r\n' % self.ClientStartTime
        for dialect in self.Dialects:
            t += '\t Dialect: %s\r\n' % dialect.name

        return t


class SMB2ContextType(enum.Enum):
    SMB2_PREAUTH_INTEGRITY_CAPABILITIES = 1
    SMB2_ENCRYPTION_CAPABILITIES = 2


class SMB2HashAlgorithm(enum.Enum):
    SHA_512 = 1


class SMB2NegotiateContext:

    def __init__(self):
        self.ContextType = None
        self.DataLength = None
        self.Reserved = None
        self.Data = None

    @staticmethod
    def from_buffer(buff):
        ctx = SMB2NegotiateContext()
        ctx.ContextType = SMB2ContextType(int.from_bytes((buff.read(2)), byteorder='little', signed=False))
        ctx.DataLength = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        ctx.Reserved = buff.read(4)
        if ctx.ContextType == SMB2ContextType.SMB2_PREAUTH_INTEGRITY_CAPABILITIES:
            ctx.Data = SMB2PreauthIntegrityCapabilities.from_buffer(buff)
        else:
            if ctx.ContextType == SMB2ContextType.SMB2_ENCRYPTION_CAPABILITIES:
                ctx.Data = SMB2EncryptionCapabilities.from_buffer(buff)
        return ctx

    def to_bytes(self):
        t = self.ContextType.to_bytes(2, byteorder='little', signed=False)
        t += self.DataLength.to_bytes(2, byteorder='little', signed=False)
        t += self.Reserved.to_bytes(4, byteorder='little', signed=False)
        return t

    def __repr__(self):
        t = '==== SMB2 Negotiate Context ====\r\n'
        t += 'ConextType: %s\r\n' % self.ContextType.name
        t += 'DataLength: %s\r\n' % self.DataLength
        t += 'Data: %s\r\n' % repr(self.Data)
        return t


class SMB2PreauthIntegrityCapabilities:

    def __init__(self, data=None):
        self.HashAlgorithmCount = None
        self.SaltLength = None
        self.HashAlgorithms = None
        self.Salt = None

    @staticmethod
    def from_buffer(buff):
        cap = SMB2PreauthIntegrityCapabilities()
        cap.HashAlgorithmCount = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        cap.SaltLength = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        cap.HashAlgorithms = []
        for i in range(cap.HashAlgorithmCount):
            cap.HashAlgorithms.append(SMB2HashAlgorithm(int.from_bytes((buff.read(2)), byteorder='little', signed=False)))

        cap.Salt = buff.read(cap.SaltLength)
        return cap

    def to_bytes(self):
        t = self.HashAlgorithmCount.to_bytes(2, byteorder='little', signed=False)
        t += self.SaltLength.to_bytes(2, byteorder='little', signed=False)
        for hashalgo in self.HashAlgorithms:
            t += hashalgo.to_bytes(2, byteorder='little', signed=False)

        t += self.Salt
        return t

    def __repr__(self):
        t = '==== SMB2 Preauth Integrity Capabilities ====\r\n'
        t += 'HashAlgorithmCount: %s\r\n' % self.HashAlgorithmCount
        t += 'SaltLength: %s\r\n' % self.SaltLength
        t += 'Salt: %s\r\n' % self.Salt
        for algo in self.HashAlgorithms:
            t += 'HashAlgo: %s\r\n' % algo.name

        return t


class SMB2Cipher(enum.Enum):
    AES_128_CCM = 1
    AES_128_GCM = 2


class SMB2EncryptionCapabilities:

    def __init__(self):
        self.CipherCount = None
        self.Ciphers = None

    @staticmethod
    def from_buffer(buff):
        cap = SMB2EncryptionCapabilities()
        cap.CipherCount = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        cap.Ciphers = []
        for i in range(cap.CipherCount):
            cap.Ciphers.append(SMB2Cipher(int.from_bytes((buff.read(2)), byteorder='little', signed=False)))

        return cap

    def to_bytes(self):
        t = self.CipherCount.to_bytes(2, byteorder='little', signed=False)
        for cipher in self.Ciphers:
            t += cipher.to_bytes(2, byteorder='little', signed=False)

        return t

    def __repr__(self):
        t = '==== SMB2 Encryption Capabilities ====\r\n'
        t += 'CipherCount: %s\r\n' % self.CipherCount
        for cipher in self.Ciphers:
            t += 'Cipher: %s\r\n' % cipher.name

        return t


class NEGOTIATE_REPLY:

    def __init__(self):
        self.StructureSize = None
        self.SecurityMode = None
        self.DialectRevision = None
        self.NegotiateContextCount = None
        self.ServerGuid = None
        self.Capabilities = None
        self.MaxTransactSize = None
        self.MaxReadSize = None
        self.MaxWriteSize = None
        self.SystemTime = None
        self.ServerStartTime = None
        self.SecurityBufferOffset = None
        self.SecurityBufferLength = None
        self.NegotiateContextOffset = None
        self.Buffer = None
        self.Padding = None
        self.NegotiateContextList = None
        self.ppos = 64

    @staticmethod
    def from_bytes(bbuff):
        return NEGOTIATE_REPLY.from_buffer(io.BytesIO(bbuff))

    @staticmethod
    def from_buffer(buff):
        msg = NEGOTIATE_REPLY()
        msg.StructureSize = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        assert msg.StructureSize == 65
        msg.SecurityMode = NegotiateSecurityMode(int.from_bytes((buff.read(2)), byteorder='little', signed=False))
        msg.DialectRevision = NegotiateDialects(int.from_bytes((buff.read(2)), byteorder='little', signed=False))
        msg.NegotiateContextCount = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        msg.ServerGuid = uuid.UUID(bytes_le=(buff.read(16)))
        msg.Capabilities = NegotiateCapabilities(int.from_bytes((buff.read(4)), byteorder='little', signed=False))
        msg.MaxTransactSize = int.from_bytes((buff.read(4)), byteorder='little', signed=False)
        msg.MaxReadSize = int.from_bytes((buff.read(4)), byteorder='little', signed=False)
        msg.MaxWriteSize = int.from_bytes((buff.read(4)), byteorder='little', signed=False)
        msg.SystemTime = wintime2datetime(int.from_bytes((buff.read(8)), byteorder='little', signed=False))
        msg.ServerStartTime = wintime2datetime(int.from_bytes((buff.read(8)), byteorder='little', signed=False))
        msg.SecurityBufferOffset = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        msg.SecurityBufferLength = int.from_bytes((buff.read(2)), byteorder='little', signed=False)
        msg.NegotiateContextOffset = int.from_bytes((buff.read(4)), byteorder='little', signed=False)
        pos = buff.tell()
        if msg.SecurityBufferLength != 0:
            buff.seek(msg.SecurityBufferOffset, io.SEEK_SET)
            msg.Buffer = buff.read(msg.SecurityBufferLength)
        pos_buff_end = buff.tell()
        if msg.DialectRevision == NegotiateDialects.SMB311:
            msg.NegotiateContextList = []
            buff.seek(msg.NegotiateContextOffset, io.SEEK_SET)
            for i in range(msg.NegotiateContextCount):
                msg.NegotiateContextList.append(SMB2NegotiateContext.from_buffer(buff))

        return msg

    @staticmethod
    def construct(data, SecurityMode, DialectRevision, ServerGuid, Capabilities, MaxTransactSize=8388608, MaxReadSize=8388608, MaxWriteSize=8388608, SystemTime=datetime.datetime.now(), ServerStartTime=datetime.datetime.now() - datetime.timedelta(days=1), NegotiateContextList=[], ppos=None):
        cmd = NEGOTIATE_REPLY()
        if ppos is None:
            ppos = cmd.ppos
        else:
            cmd.StructureSize = 65
            cmd.SecurityMode = SecurityMode
            cmd.DialectRevision = DialectRevision
            cmd.NegotiateContextCount = len(NegotiateContextList)
            cmd.ServerGuid = ServerGuid
            cmd.Capabilities = Capabilities
            cmd.MaxTransactSize = MaxTransactSize
            cmd.MaxReadSize = MaxReadSize
            cmd.MaxWriteSize = MaxWriteSize
            cmd.SystemTime = SystemTime
            cmd.ServerStartTime = ServerStartTime
            cmd.SecurityBufferOffset = ppos + 64
            cmd.SecurityBufferLength = len(data)
            if NegotiateContextList == []:
                cmd.NegotiateContextOffset = 0
            else:
                cmd.NegotiateContextOffset = cmd.SecurityBufferOffset + cmd.SecurityBufferLength
        cmd.Buffer = data
        cmd.NegotiateContextList = NegotiateContextList
        return cmd

    def to_bytes(self, ppos=None):
        if ppos is None:
            ppos = self.ppos
        t = self.StructureSize.to_bytes(2, byteorder='little', signed=False)
        t += self.SecurityMode.to_bytes(2, byteorder='little', signed=False)
        t += self.DialectRevision.value.to_bytes(2, byteorder='little', signed=False)
        t += self.NegotiateContextCount.to_bytes(2, byteorder='little', signed=False)
        t += self.ServerGuid.bytes_le
        t += self.Capabilities.to_bytes(4, byteorder='little', signed=False)
        t += self.MaxTransactSize.to_bytes(4, byteorder='little', signed=False)
        t += self.MaxReadSize.to_bytes(4, byteorder='little', signed=False)
        t += self.MaxWriteSize.to_bytes(4, byteorder='little', signed=False)
        t += dt2wt(self.SystemTime).to_bytes(8, byteorder='little', signed=False)
        t += dt2wt(self.ServerStartTime).to_bytes(8, byteorder='little', signed=False)
        t += self.SecurityBufferOffset.to_bytes(2, byteorder='little', signed=False)
        t += self.SecurityBufferLength.to_bytes(2, byteorder='little', signed=False)
        print(self.NegotiateContextOffset)
        t += self.NegotiateContextOffset.to_bytes(4, byteorder='little', signed=False)
        t += self.Buffer
        if self.NegotiateContextCount > 0:
            for ngctx in self.NegotiateContextList:
                t += ngctx.to_bytes()
                q, m = divmod(len(t) + ppos, 8)
                t += b'\x00' * ((q + 1) * 8 - len(t))

        return t

    def __repr__(self):
        t = '==== SMB2 NEGOTIATE REPLY ====\r\n'
        t += 'StructureSize: %s\r\n' % self.StructureSize
        t += 'SecurityMode: %s\r\n' % repr(self.SecurityMode)
        t += 'DialectRevision: %s\r\n' % self.DialectRevision.name
        t += 'ServerGuid: %s\r\n' % self.ServerGuid
        t += 'Capabilities: %s\r\n' % repr(self.Capabilities)
        t += 'MaxTransactSize: %s\r\n' % self.MaxTransactSize
        t += 'MaxReadSize: %s\r\n' % self.MaxReadSize
        t += 'MaxWriteSize: %s\r\n' % self.MaxWriteSize
        t += 'SystemTime: %s\r\n' % self.SystemTime.isoformat()
        t += 'ServerStartTime: %s\r\n' % self.ServerStartTime.isoformat()
        t += 'SecurityBufferOffset: %s\r\n' % self.SecurityBufferOffset
        t += 'SecurityBufferLength: %s\r\n' % self.SecurityBufferLength
        t += 'Buffer: %s\r\n' % self.Buffer
        t += 'NegotiateContextList: %s\r\n' % self.NegotiateContextList
        return t


class SessionSetupFlag(enum.IntFlag):
    SMB2_SESSION_FLAG_BINDING = 1


class SessionSetupCapabilities(enum.IntFlag):
    SMB2_GLOBAL_CAP_DFS = 1
    SMB2_GLOBAL_CAP_UNUSED1 = 2
    SMB2_GLOBAL_CAP_UNUSED2 = 4
    SMB2_GLOBAL_CAP_UNUSED3 = 8


class SESSION_SETUP_REQ:

    def __init__(self):
        self.StructureSize = None
        self.Flags = None
        self.SecurityMode = None
        self.Capabilities = None
        self.Channel = None
        self.SecurityBufferOffset = None
        self.SecurityBufferLength = None
        self.PreviousSessionId = None
        self.Buffer = None

    @staticmethod
    def from_bytes(bbuff):
        return SESSION_SETUP_REQ.from_buffer(io.BytesIO(bbuff))

    @staticmethod
    def from_buffer(buff):
        msg = SESSION_SETUP_REQ()
        msg.StructureSize = int.from_bytes((buff.read(2)), byteorder='little')
        assert msg.StructureSize == 25
        msg.Flags = SessionSetupFlag(int.from_bytes((buff.read(1)), byteorder='little'))
        msg.SecurityMode = NegotiateSecurityMode(int.from_bytes((buff.read(1)), byteorder='little'))
        msg.Capabilities = SessionSetupCapabilities(int.from_bytes((buff.read(4)), byteorder='little'))
        msg.Channel = int.from_bytes((buff.read(4)), byteorder='little')
        msg.SecurityBufferOffset = int.from_bytes((buff.read(2)), byteorder='little')
        msg.SecurityBufferLength = int.from_bytes((buff.read(2)), byteorder='little')
        msg.PreviousSessionId = buff.read(2)
        buff.seek(msg.SecurityBufferOffset, io.SEEK_SET)
        msg.Buffer = buff.read(msg.SecurityBufferLength)
        return msg

    def __repr__(self):
        t = '==== SMB2 SESSION SETUP REQ ====\r\n'
        t += 'StructureSize: %s\r\n' % self.StructureSize
        t += 'Flags: %s\r\n' % repr(self.Flags)
        t += 'SecurityMode: %s\r\n' % self.SecurityMode
        t += 'Capabilities: %s\r\n' % self.Capabilities
        t += 'Channel: %s\r\n' % self.Channel
        t += 'SecurityBufferOffset: %s\r\n' % self.SecurityBufferOffset
        t += 'SecurityBufferLength: %s\r\n' % self.SecurityBufferLength
        t += 'PreviousSessionId: %s\r\n' % self.PreviousSessionId
        t += 'Buffer: %s\r\n' % self.Buffer
        return t


class SessionFlags(enum.IntFlag):
    SMB2_SESSION_FLAG_IS_GUEST = 1
    SMB2_SESSION_FLAG_IS_NULL = 2
    SMB2_SESSION_FLAG_ENCRYPT_DATA = 4


class SESSION_SETUP_REPLY:

    def __init__(self):
        self.StructureSize = None
        self.SessionFlags = None
        self.SecurityBufferOffset = None
        self.SecurityBufferLength = None
        self.Buffer = None
        self.ppos = 64

    @staticmethod
    def from_bytes(bbuff):
        return SESSION_SETUP_REPLY.from_buffer(io.BytesIO(bbuff))

    @staticmethod
    def from_buffer(buff):
        msg = SESSION_SETUP_REPLY()
        msg.StructureSize = int.from_bytes((buff.read(2)), byteorder='little')
        assert msg.StructureSize == 9
        msg.SessionFlags = SessionFlags(int.from_bytes((buff.read(2)), byteorder='little'))
        msg.SecurityBufferOffset = int.from_bytes((buff.read(2)), byteorder='little')
        msg.SecurityBufferLength = int.from_bytes((buff.read(2)), byteorder='little')
        msg.Buffer = buff.read(msg.SecurityBufferLength)

    @staticmethod
    def construct(data, flags, ppos=None):
        msg = SESSION_SETUP_REPLY()
        if ppos is None:
            ppos = msg.ppos
        msg.StructureSize = 9
        msg.SessionFlags = flags
        msg.SecurityBufferOffset = ppos + 8
        msg.SecurityBufferLength = len(data)
        msg.Buffer = data
        return msg

    def to_bytes(self):
        t = self.StructureSize.to_bytes(2, byteorder='little', signed=False)
        t += self.SessionFlags.to_bytes(2, byteorder='little', signed=False)
        t += self.SecurityBufferOffset.to_bytes(2, byteorder='little', signed=False)
        t += self.SecurityBufferLength.to_bytes(2, byteorder='little', signed=False)
        t += self.Buffer
        return t

    def __repr__(self):
        t = '==== SMB2 SESSION SETUP REPLY ====\r\n'
        t += 'StructureSize: %s\r\n' % self.StructureSize
        t += 'SessionFlags: %s\r\n' % repr(self.SessionFlags)
        t += 'SecurityBufferOffset: %s\r\n' % self.SecurityBufferOffset
        t += 'SecurityBufferLength: %s\r\n' % self.SecurityBufferLength
        t += 'Buffer: %s\r\n' % self.Buffer
        return t


class SMB2TreeConnectRQFlag(enum.IntFlag):
    SMB2_TREE_CONNECT_FLAG_CLUSTER_RECONNECT = 1
    SMB2_TREE_CONNECT_FLAG_REDIRECT_TO_OWNER = 2
    SMB2_TREE_CONNECT_FLAG_EXTENSION_PRESENT = 4


class TREE_CONNECT_REQ:

    def __init__(self, data=None):
        self.Dialect = NegotiateDialects.SMB300
        self.StructureSize = None
        self.Flags = None
        self.PathOffset = None
        self.PathLength = None
        self.PathName = None
        self.Reserved = None
        self.Buffer = None
        if data is not None:
            self.parse(data)

    def parse(self, data):
        self.StructureSize = int.from_bytes((data[:2]), byteorder='little')
        if not self.StructureSize == 9:
            raise AssertionError
        else:
            if self.Dialect == NegotiateDialects.SMB311:
                self.Flags = SMB2TreeConnectRQFlag(int.from_bytes((data[2:4]), byteorder='little'))
            else:
                self.Reserved = data[2:4]
            self.PathOffset = int.from_bytes((data[4:6]), byteorder='little')
            self.PathLength = int.from_bytes((data[6:8]), byteorder='little')
            if self.Dialect == NegotiateDialects.SMB311:
                self.Buffer = data[8:8 + self.PathLength]
            else:
                self.PathName = data[8:8 + self.PathLength].decode('utf-16')

    def __repr__(self):
        t = '==== SMB2 TREE CONNECT REQ ====\r\n'
        t += 'StructureSize: %s\r\n' % self.StructureSize
        if self.Dialect == NegotiateDialects.SMB311:
            t += 'Flags: %s\r\n' % repr(self.Flags)
        else:
            t += 'Reserved: %s\r\n' % repr(self.Reserved)
        t += 'PathOffset: %s\r\n' % self.PathOffset
        t += 'PathLength: %s\r\n' % self.PathLength
        if self.Dialect == NegotiateDialects.SMB311:
            t += 'Buffer: %s\r\n' % self.Buffer
        else:
            t += 'PathName: %s\r\n' % repr(self.PathName)
        return t


class SMB2ShareType(enum.Enum):
    SMB2_SHARE_TYPE_DISK = 1
    SMB2_SHARE_TYPE_PIPE = 2
    SMB2_SHARE_TYPE_PRINT = 3


class SMB2ShareFlags(enum.IntFlag):
    SMB2_SHAREFLAG_MANUAL_CACHING = 0
    SMB2_SHAREFLAG_AUTO_CACHING = 16
    SMB2_SHAREFLAG_VDO_CACHING = 32
    SMB2_SHAREFLAG_NO_CACHING = 48
    SMB2_SHAREFLAG_DFS = 1
    SMB2_SHAREFLAG_DFS_ROOT = 2
    SMB2_SHAREFLAG_RESTRICT_EXCLUSIVE_OPENS = 256
    SMB2_SHAREFLAG_FORCE_SHARED_DELETE = 512
    SMB2_SHAREFLAG_ALLOW_NAMESPACE_CACHING = 1024
    SMB2_SHAREFLAG_ACCESS_BASED_DIRECTORY_ENUM = 2048
    SMB2_SHAREFLAG_FORCE_LEVELII_OPLOCK = 4096
    SMB2_SHAREFLAG_ENABLE_HASH_V1 = 8192
    SMB2_SHAREFLAG_ENABLE_HASH_V2 = 16384
    SMB2_SHAREFLAG_ENCRYPT_DATA = 32768
    SMB2_SHAREFLAG_IDENTITY_REMOTING = 262144


class SMB2ShareCapabilities(enum.IntFlag):
    SMB2_SHARE_CAP_DFS = 8
    SMB2_SHARE_CAP_CONTINUOUS_AVAILABILITY = 16
    SMB2_SHARE_CAP_SCALEOUT = 32
    SMB2_SHARE_CAP_CLUSTER = 64
    SMB2_SHARE_CAP_ASYMMETRIC = 128
    SMB2_SHARE_CAP_REDIRECT_TO_OWNER = 256


class DirectoryAccessMask(enum.IntFlag):
    FILE_LIST_DIRECTORY = 1
    FILE_ADD_FILE = 2
    FILE_ADD_SUBDIRECTORY = 4
    FILE_READ_EA = 8
    FILE_WRITE_EA = 16
    FILE_TRAVERSE = 32
    FILE_DELETE_CHILD = 64
    FILE_READ_ATTRIBUTES = 128
    FILE_WRITE_ATTRIBUTES = 256
    DELETE = 65536
    READ_CONTROL = 131072
    WRITE_DAC = 262144
    WRITE_OWNER = 524288
    SYNCHRONIZE = 1048576
    ACCESS_SYSTEM_SECURITY = 16777216
    MAXIMUM_ALLOWED = 33554432
    GENERIC_ALL = 268435456
    GENERIC_EXECUTE = 536870912
    GENERIC_WRITE = 1073741824
    GENERIC_READ = 2147483648


class FilePipePrinterAccessMask(enum.IntFlag):
    FILE_READ_DATA = 1
    FILE_WRITE_DATA = 2
    FILE_APPEND_DATA = 4
    FILE_READ_EA = 8
    FILE_WRITE_EA = 16
    FILE_DELETE_CHILD = 64
    FILE_EXECUTE = 32
    FILE_READ_ATTRIBUTES = 128
    FILE_WRITE_ATTRIBUTES = 256
    DELETE = 65536
    READ_CONTROL = 131072
    WRITE_DAC = 262144
    WRITE_OWNER = 524288
    SYNCHRONIZE = 1048576
    ACCESS_SYSTEM_SECURITY = 16777216
    MAXIMUM_ALLOWED = 33554432
    GENERIC_ALL = 268435456
    GENERIC_EXECUTE = 536870912
    GENERIC_WRITE = 1073741824
    GENERIC_READ = 2147483648


class TREE_CONNECT_REPLY:

    def __init__(self, data=None):
        self.StructureSize = None
        self.ShareType = None
        self.Reserved = None
        self.ShareFlags = None
        self.Capabilities = None
        self.MaximalAccess = None
        if data is not None:
            self.parse(data)

    def parse(self, data):
        self.StructureSize = int.from_bytes((data[:2]), byteorder='little')
        if not self.StructureSize == 16:
            raise AssertionError
        else:
            self.ShareType = SMB2ShareType(data[2])
            self.Reserved = data[3]
            self.ShareFlags = SMB2ShareFlags(int.from_bytes((data[4:8]), byteorder='little'))
            self.Capabilities = SMB2ShareCapabilities(int.from_bytes((data[8:12]), byteorder='little'))
            temp_sharetype = 'file'
            if temp_sharetype == 'file':
                self.MaximalAccess = FilePipePrinterAccessMask(int.from_bytes((data[12:16]), byteorder='little'))
            else:
                self.MaximalAccess = DirectoryAccessMask(int.from_bytes((data[12:16]), byteorder='little'))

    def __repr__(self):
        t = '==== SMB2 TREE CONNECT REPLY ====\r\n'
        t += 'StructureSize: %s\r\n' % self.StructureSize
        t += 'ShareType: %s\r\n' % self.ShareType.name
        t += 'Reserved: %s\r\n' % self.Reserved
        t += 'ShareFlags: %s\r\n' % repr(self.ShareFlags)
        t += 'Capabilities: %s\r\n' % repr(self.Capabilities)
        t += 'MaximalAccess: %s\r\n' % self.MaximalAccess
        return t