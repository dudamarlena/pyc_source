# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/bvll.py
# Compiled at: 2020-04-22 18:16:21
"""
BACnet Virtual Link Layer Module
"""
from .errors import EncodingError, DecodingError
from .debugging import ModuleLogger, DebugContents, bacpypes_debugging
from .pdu import Address, PCI, PDUData, unpack_ip_addr
_debug = 0
_log = ModuleLogger(globals())
bvl_pdu_types = {}

def register_bvlpdu_type(klass):
    bvl_pdu_types[klass.messageType] = klass


@bacpypes_debugging
class BVLCI(PCI, DebugContents):
    _debug_contents = ('bvlciType', 'bvlciFunction', 'bvlciLength')
    result = 0
    writeBroadcastDistributionTable = 1
    readBroadcastDistributionTable = 2
    readBroadcastDistributionTableAck = 3
    forwardedNPDU = 4
    registerForeignDevice = 5
    readForeignDeviceTable = 6
    readForeignDeviceTableAck = 7
    deleteForeignDeviceTableEntry = 8
    distributeBroadcastToNetwork = 9
    originalUnicastNPDU = 10
    originalBroadcastNPDU = 11

    def __init__(self, *args, **kwargs):
        if _debug:
            BVLCI._debug('__init__ %r %r', args, kwargs)
        super(BVLCI, self).__init__(*args, **kwargs)
        self.bvlciType = 129
        self.bvlciFunction = None
        self.bvlciLength = None
        return

    def update(self, bvlci):
        PCI.update(self, bvlci)
        self.bvlciType = bvlci.bvlciType
        self.bvlciFunction = bvlci.bvlciFunction
        self.bvlciLength = bvlci.bvlciLength

    def encode(self, pdu):
        """encode the contents of the BVLCI into the PDU."""
        if _debug:
            BVLCI._debug('encode %s', str(pdu))
        PCI.update(pdu, self)
        pdu.put(self.bvlciType)
        pdu.put(self.bvlciFunction)
        if self.bvlciLength != len(self.pduData) + 4:
            raise EncodingError('invalid BVLCI length')
        pdu.put_short(self.bvlciLength)

    def decode(self, pdu):
        """decode the contents of the PDU into the BVLCI."""
        if _debug:
            BVLCI._debug('decode %s', str(pdu))
        PCI.update(self, pdu)
        self.bvlciType = pdu.get()
        if self.bvlciType != 129:
            raise DecodingError('invalid BVLCI type')
        self.bvlciFunction = pdu.get()
        self.bvlciLength = pdu.get_short()
        if self.bvlciLength != len(pdu.pduData) + 4:
            raise DecodingError('invalid BVLCI length')

    def bvlci_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        if _debug:
            BVLCI._debug('bvlci_contents use_dict=%r as_class=%r', use_dict, as_class)
        if use_dict is None:
            use_dict = as_class()
        use_dict.__setitem__('type', self.bvlciType)
        use_dict.__setitem__('function', self.bvlciFunction)
        use_dict.__setitem__('length', self.bvlciLength)
        return use_dict


@bacpypes_debugging
class BVLPDU(BVLCI, PDUData):

    def __init__(self, *args, **kwargs):
        if _debug:
            BVLPDU._debug('__init__ %r %r', args, kwargs)
        super(BVLPDU, self).__init__(*args, **kwargs)

    def encode(self, pdu):
        BVLCI.encode(self, pdu)
        pdu.put_data(self.pduData)

    def decode(self, pdu):
        BVLCI.decode(self, pdu)
        self.pduData = pdu.get_data(len(pdu.pduData))

    def bvlpdu_contents(self, use_dict=None, as_class=dict):
        return PDUData.pdudata_contents(self, use_dict=use_dict, as_class=as_class)

    def dict_contents(self, use_dict=None, as_class=dict, key_values=()):
        """Return the contents of an object as a dict."""
        if _debug:
            BVLPDU._debug('dict_contents use_dict=%r as_class=%r key_values=%r', use_dict, as_class, key_values)
        if use_dict is None:
            use_dict = as_class()
        self.bvlci_contents(use_dict=use_dict, as_class=as_class)
        self.bvlpdu_contents(use_dict=use_dict, as_class=as_class)
        return use_dict


@bacpypes_debugging
def key_value_contents(use_dict=None, as_class=dict, key_values=()):
    """Return the contents of an object as a dict."""
    if _debug:
        key_value_contents._debug('key_value_contents use_dict=%r as_class=%r key_values=%r', use_dict, as_class, key_values)
    if use_dict is None:
        use_dict = as_class()
    for k, v in key_values:
        if v is not None:
            if hasattr(v, 'dict_contents'):
                v = v.dict_contents(as_class=as_class)
            use_dict.__setitem__(k, v)

    return use_dict


class Result(BVLPDU):
    _debug_contents = ('bvlciResultCode', )
    messageType = BVLCI.result

    def __init__(self, code=None, *args, **kwargs):
        super(Result, self).__init__(*args, **kwargs)
        self.bvlciFunction = BVLCI.result
        self.bvlciLength = 6
        self.bvlciResultCode = code

    def encode(self, bvlpdu):
        BVLCI.update(bvlpdu, self)
        bvlpdu.put_short(self.bvlciResultCode)

    def decode(self, bvlpdu):
        BVLCI.update(self, bvlpdu)
        self.bvlciResultCode = bvlpdu.get_short()

    def bvlpdu_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        return key_value_contents(use_dict=use_dict, as_class=as_class, key_values=(
         ('function', 'Result'),
         (
          'result_code', self.bvlciResultCode)))


register_bvlpdu_type(Result)

class WriteBroadcastDistributionTable(BVLPDU):
    _debug_contents = ('bvlciBDT', )
    messageType = BVLCI.writeBroadcastDistributionTable

    def __init__(self, bdt=[], *args, **kwargs):
        super(WriteBroadcastDistributionTable, self).__init__(*args, **kwargs)
        self.bvlciFunction = BVLCI.writeBroadcastDistributionTable
        self.bvlciLength = 4 + 10 * len(bdt)
        self.bvlciBDT = bdt

    def encode(self, bvlpdu):
        BVLCI.update(bvlpdu, self)
        for bdte in self.bvlciBDT:
            bvlpdu.put_data(bdte.addrAddr)
            bvlpdu.put_long(bdte.addrMask)

    def decode(self, bvlpdu):
        BVLCI.update(self, bvlpdu)
        self.bvlciBDT = []
        while bvlpdu.pduData:
            bdte = Address(unpack_ip_addr(bvlpdu.get_data(6)))
            bdte.addrMask = bvlpdu.get_long()
            self.bvlciBDT.append(bdte)

    def bvlpdu_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        broadcast_distribution_table = []
        for bdte in self.bvlciBDT:
            broadcast_distribution_table.append(str(bdte))

        return key_value_contents(use_dict=use_dict, as_class=as_class, key_values=(
         ('function', 'WriteBroadcastDistributionTable'),
         (
          'bdt', broadcast_distribution_table)))


register_bvlpdu_type(WriteBroadcastDistributionTable)

class ReadBroadcastDistributionTable(BVLPDU):
    messageType = BVLCI.readBroadcastDistributionTable

    def __init__(self, *args, **kwargs):
        super(ReadBroadcastDistributionTable, self).__init__(*args, **kwargs)
        self.bvlciFunction = BVLCI.readBroadcastDistributionTable
        self.bvlciLength = 4

    def encode(self, bvlpdu):
        BVLCI.update(bvlpdu, self)

    def decode(self, bvlpdu):
        BVLCI.update(self, bvlpdu)

    def bvlpdu_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        return key_value_contents(use_dict=use_dict, as_class=as_class, key_values=(('function', 'ReadBroadcastDistributionTable'), ))


register_bvlpdu_type(ReadBroadcastDistributionTable)

class ReadBroadcastDistributionTableAck(BVLPDU):
    _debug_contents = ('bvlciBDT', )
    messageType = BVLCI.readBroadcastDistributionTableAck

    def __init__(self, bdt=[], *args, **kwargs):
        super(ReadBroadcastDistributionTableAck, self).__init__(*args, **kwargs)
        self.bvlciFunction = BVLCI.readBroadcastDistributionTableAck
        self.bvlciLength = 4 + 10 * len(bdt)
        self.bvlciBDT = bdt

    def encode(self, bvlpdu):
        self.bvlciLength = 4 + 10 * len(self.bvlciBDT)
        BVLCI.update(bvlpdu, self)
        for bdte in self.bvlciBDT:
            bvlpdu.put_data(bdte.addrAddr)
            bvlpdu.put_long(bdte.addrMask)

    def decode(self, bvlpdu):
        BVLCI.update(self, bvlpdu)
        self.bvlciBDT = []
        while bvlpdu.pduData:
            bdte = Address(unpack_ip_addr(bvlpdu.get_data(6)))
            bdte.addrMask = bvlpdu.get_long()
            self.bvlciBDT.append(bdte)

    def bvlpdu_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        broadcast_distribution_table = []
        for bdte in self.bvlciBDT:
            broadcast_distribution_table.append(str(bdte))

        return key_value_contents(use_dict=use_dict, as_class=as_class, key_values=(
         ('function', 'ReadBroadcastDistributionTableAck'),
         (
          'bdt', broadcast_distribution_table)))


register_bvlpdu_type(ReadBroadcastDistributionTableAck)

class ForwardedNPDU(BVLPDU):
    _debug_contents = ('bvlciAddress', )
    messageType = BVLCI.forwardedNPDU

    def __init__(self, addr=None, *args, **kwargs):
        super(ForwardedNPDU, self).__init__(*args, **kwargs)
        self.bvlciFunction = BVLCI.forwardedNPDU
        self.bvlciLength = 10 + len(self.pduData)
        self.bvlciAddress = addr

    def encode(self, bvlpdu):
        self.bvlciLength = 10 + len(self.pduData)
        BVLCI.update(bvlpdu, self)
        bvlpdu.put_data(self.bvlciAddress.addrAddr)
        bvlpdu.put_data(self.pduData)

    def decode(self, bvlpdu):
        BVLCI.update(self, bvlpdu)
        self.bvlciAddress = Address(unpack_ip_addr(bvlpdu.get_data(6)))
        self.pduData = bvlpdu.get_data(len(bvlpdu.pduData))

    def bvlpdu_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        if use_dict is None:
            use_dict = as_class()
        key_value_contents(use_dict=use_dict, as_class=as_class, key_values=(
         ('function', 'ForwardedNPDU'),
         (
          'address', str(self.bvlciAddress))))
        PDUData.dict_contents(self, use_dict=use_dict, as_class=as_class)
        return use_dict


register_bvlpdu_type(ForwardedNPDU)

class FDTEntry(DebugContents):
    _debug_contents = ('fdAddress', 'fdTTL', 'fdRemain')

    def __init__(self):
        self.fdAddress = None
        self.fdTTL = None
        self.fdRemain = None
        return

    def __eq__(self, other):
        """Return true iff entries are identical."""
        return self.fdAddress == other.fdAddress and self.fdTTL == other.fdTTL and self.fdRemain == other.fdRemain

    def bvlpdu_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        if use_dict is None:
            use_dict = as_class()
        use_dict.__setitem__('address', str(self.fdAddress))
        use_dict.__setitem__('ttl', self.fdTTL)
        use_dict.__setitem__('remaining', self.fdRemain)
        return use_dict


class RegisterForeignDevice(BVLPDU):
    _debug_contents = ('bvlciTimeToLive', )
    messageType = BVLCI.registerForeignDevice

    def __init__(self, ttl=None, *args, **kwargs):
        super(RegisterForeignDevice, self).__init__(*args, **kwargs)
        self.bvlciFunction = BVLCI.registerForeignDevice
        self.bvlciLength = 6
        self.bvlciTimeToLive = ttl

    def encode(self, bvlpdu):
        BVLCI.update(bvlpdu, self)
        bvlpdu.put_short(self.bvlciTimeToLive)

    def decode(self, bvlpdu):
        BVLCI.update(self, bvlpdu)
        self.bvlciTimeToLive = bvlpdu.get_short()

    def bvlpdu_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        return key_value_contents(use_dict=use_dict, as_class=as_class, key_values=(
         ('function', 'RegisterForeignDevice'),
         (
          'ttl', self.bvlciTimeToLive)))


register_bvlpdu_type(RegisterForeignDevice)

class ReadForeignDeviceTable(BVLPDU):
    messageType = BVLCI.readForeignDeviceTable

    def __init__(self, ttl=None, *args, **kwargs):
        super(ReadForeignDeviceTable, self).__init__(*args, **kwargs)
        self.bvlciFunction = BVLCI.readForeignDeviceTable
        self.bvlciLength = 4

    def encode(self, bvlpdu):
        BVLCI.update(bvlpdu, self)

    def decode(self, bvlpdu):
        BVLCI.update(self, bvlpdu)

    def bvlpdu_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        return key_value_contents(use_dict=use_dict, as_class=as_class, key_values=(('function', 'ReadForeignDeviceTable'), ))


register_bvlpdu_type(ReadForeignDeviceTable)

class ReadForeignDeviceTableAck(BVLPDU):
    _debug_contents = ('bvlciFDT', )
    messageType = BVLCI.readForeignDeviceTableAck

    def __init__(self, fdt=[], *args, **kwargs):
        super(ReadForeignDeviceTableAck, self).__init__(*args, **kwargs)
        self.bvlciFunction = BVLCI.readForeignDeviceTableAck
        self.bvlciLength = 4 + 10 * len(fdt)
        self.bvlciFDT = fdt

    def encode(self, bvlpdu):
        BVLCI.update(bvlpdu, self)
        for fdte in self.bvlciFDT:
            bvlpdu.put_data(fdte.fdAddress.addrAddr)
            bvlpdu.put_short(fdte.fdTTL)
            bvlpdu.put_short(fdte.fdRemain)

    def decode(self, bvlpdu):
        BVLCI.update(self, bvlpdu)
        self.bvlciFDT = []
        while bvlpdu.pduData:
            fdte = FDTEntry()
            fdte.fdAddress = Address(unpack_ip_addr(bvlpdu.get_data(6)))
            fdte.fdTTL = bvlpdu.get_short()
            fdte.fdRemain = bvlpdu.get_short()
            self.bvlciFDT.append(fdte)

    def bvlpdu_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        foreign_device_table = []
        for fdte in self.bvlciFDT:
            foreign_device_table.append(fdte.bvlpdu_contents(as_class=as_class))

        return key_value_contents(use_dict=use_dict, as_class=as_class, key_values=(
         ('function', 'ReadForeignDeviceTableAck'),
         (
          'foreign_device_table', foreign_device_table)))


register_bvlpdu_type(ReadForeignDeviceTableAck)

class DeleteForeignDeviceTableEntry(BVLPDU):
    _debug_contents = ('bvlciAddress', )
    messageType = BVLCI.deleteForeignDeviceTableEntry

    def __init__(self, addr=None, *args, **kwargs):
        super(DeleteForeignDeviceTableEntry, self).__init__(*args, **kwargs)
        self.bvlciFunction = BVLCI.deleteForeignDeviceTableEntry
        self.bvlciLength = 10
        self.bvlciAddress = addr

    def encode(self, bvlpdu):
        BVLCI.update(bvlpdu, self)
        bvlpdu.put_data(self.bvlciAddress.addrAddr)

    def decode(self, bvlpdu):
        BVLCI.update(self, bvlpdu)
        self.bvlciAddress = Address(unpack_ip_addr(bvlpdu.get_data(6)))

    def bvlpdu_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        return key_value_contents(use_dict=use_dict, as_class=as_class, key_values=(
         ('function', 'DeleteForeignDeviceTableEntry'),
         (
          'address', str(self.bvlciAddress))))


register_bvlpdu_type(DeleteForeignDeviceTableEntry)

class DistributeBroadcastToNetwork(BVLPDU):
    messageType = BVLCI.distributeBroadcastToNetwork

    def __init__(self, *args, **kwargs):
        super(DistributeBroadcastToNetwork, self).__init__(*args, **kwargs)
        self.bvlciFunction = BVLCI.distributeBroadcastToNetwork
        self.bvlciLength = 4 + len(self.pduData)

    def encode(self, bvlpdu):
        self.bvlciLength = 4 + len(self.pduData)
        BVLCI.update(bvlpdu, self)
        bvlpdu.put_data(self.pduData)

    def decode(self, bvlpdu):
        BVLCI.update(self, bvlpdu)
        self.pduData = bvlpdu.get_data(len(bvlpdu.pduData))

    def bvlpdu_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        if use_dict is None:
            use_dict = as_class()
        key_value_contents(use_dict=use_dict, as_class=as_class, key_values=(('function', 'DistributeBroadcastToNetwork'), ))
        PDUData.dict_contents(self, use_dict=use_dict, as_class=as_class)
        return use_dict


register_bvlpdu_type(DistributeBroadcastToNetwork)

class OriginalUnicastNPDU(BVLPDU):
    messageType = BVLCI.originalUnicastNPDU

    def __init__(self, *args, **kwargs):
        super(OriginalUnicastNPDU, self).__init__(*args, **kwargs)
        self.bvlciFunction = BVLCI.originalUnicastNPDU
        self.bvlciLength = 4 + len(self.pduData)

    def encode(self, bvlpdu):
        self.bvlciLength = 4 + len(self.pduData)
        BVLCI.update(bvlpdu, self)
        bvlpdu.put_data(self.pduData)

    def decode(self, bvlpdu):
        BVLCI.update(self, bvlpdu)
        self.pduData = bvlpdu.get_data(len(bvlpdu.pduData))

    def bvlpdu_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        if use_dict is None:
            use_dict = as_class()
        key_value_contents(use_dict=use_dict, as_class=as_class, key_values=(('function', 'OriginalUnicastNPDU'), ))
        PDUData.dict_contents(self, use_dict=use_dict, as_class=as_class)
        return use_dict


register_bvlpdu_type(OriginalUnicastNPDU)

class OriginalBroadcastNPDU(BVLPDU):
    messageType = BVLCI.originalBroadcastNPDU

    def __init__(self, *args, **kwargs):
        super(OriginalBroadcastNPDU, self).__init__(*args, **kwargs)
        self.bvlciFunction = BVLCI.originalBroadcastNPDU
        self.bvlciLength = 4 + len(self.pduData)

    def encode(self, bvlpdu):
        self.bvlciLength = 4 + len(self.pduData)
        BVLCI.update(bvlpdu, self)
        bvlpdu.put_data(self.pduData)

    def decode(self, bvlpdu):
        BVLCI.update(self, bvlpdu)
        self.pduData = bvlpdu.get_data(len(bvlpdu.pduData))

    def bvlpdu_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        if use_dict is None:
            use_dict = as_class()
        key_value_contents(use_dict=use_dict, as_class=as_class, key_values=(('function', 'OriginalBroadcastNPDU'), ))
        PDUData.dict_contents(self, use_dict=use_dict, as_class=as_class)
        return use_dict


register_bvlpdu_type(OriginalBroadcastNPDU)