# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\protocols\RDP\rdp_packets.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 2389 bytes
import enum

class RDP_PROTOCOL(enum.IntFlag):
    PROTOCOL_RDP = 0
    PROTOCOL_SSL = 1
    PROTOCOL_HYBRID = 2
    PROTOCOL_RDSTLS = 4
    PROTOCOL_HYBRID_EX = 8


class RDP_NEG_REQ_FAGS(enum.IntFlag):
    RESTRICTED_ADMIN_MODE_REQUIRED = 1
    REDIRECTED_AUTHENTICATION_MODE_REQUIRED = 2
    CORRELATION_INFO_PRESENT = 8


class RDP_NEG_REQ:

    def __init__(self):
        self.type = None
        self.flags = None
        self.length = None
        self.requestedProtocols = None


class RDP_NEG_CORRELATION_INFO:

    def __init__(self):
        self.type = None
        self.flags = None
        self.length = None
        self.correlationId = None
        self.reserved = None


class X224ConnectionRequest:

    def __init__(self):
        self.tpktHeader = None
        self.x224Crq = None
        self.routingToken = None
        self.cookie = None
        self.rdpNegReq = None
        self.rdpCorrelationInfo = None


class RDP_NEG_RSP_FLAGS(enum.IntFlag):
    EXTENDED_CLIENT_DATA_SUPPORTED = 1
    DYNVC_GFX_PROTOCOL_SUPPORTED = 2
    NEGRSP_FLAG_RESERVED = 4
    RESTRICTED_ADMIN_MODE_SUPPORTED = 8
    REDIRECTED_AUTHENTICATION_MODE_SUPPORTED = 16


class RDP_NEG_RSP:

    def __init__(self):
        self.type = None
        self.flags = None
        self.length = None
        self.selectedProtocol = None


class RDP_NEG_FAILURE:

    def __init__(self):
        self.type = None
        self.flags = None
        self.length = None
        self.failureCode = None


class X224ConnectionConfirm:

    def __init__(self):
        self.tpktHeader = None
        self.x224Ccf = None
        self.rdpNegData = None


class TS_UD_HEADER:

    def __init__(self):
        self.type = None
        self.length = None


class MCSConnect:

    def __init__(self):
        self.tpktHeader = None
        self.x224Data = None
        self.mcsCi = None
        self.gccCCrq = None
        self.clientCoreData = None
        self.clientSecurityData = None
        self.clientNetworkData = None
        self.clientClusterData = None
        self.clientMonitorData = None
        self.clientMessageChannelData = None
        self.clientMultitransportChannelData = None
        self.clientMonitorExtendedData = None