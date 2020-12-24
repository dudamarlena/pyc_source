# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wgzhao/Codes/easybase/py3/lib/python3.7/site-packages/easybase/hbase/ttypes.py
# Compiled at: 2019-09-05 21:58:25
# Size of source mod 2**32: 119404 bytes
from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec
import sys
from thrift.transport import TTransport
all_structs = []

class TDeleteType(object):
    __doc__ = '\n    Specify type of delete:\n     - DELETE_COLUMN means exactly one version will be removed,\n     - DELETE_COLUMNS means previous versions will also be removed.\n    '
    DELETE_COLUMN = 0
    DELETE_COLUMNS = 1
    DELETE_FAMILY = 2
    DELETE_FAMILY_VERSION = 3
    _VALUES_TO_NAMES = {0:'DELETE_COLUMN', 
     1:'DELETE_COLUMNS', 
     2:'DELETE_FAMILY', 
     3:'DELETE_FAMILY_VERSION'}
    _NAMES_TO_VALUES = {'DELETE_COLUMN':0, 
     'DELETE_COLUMNS':1, 
     'DELETE_FAMILY':2, 
     'DELETE_FAMILY_VERSION':3}


class TDurability(object):
    __doc__ = '\n    Specify Durability:\n     - SKIP_WAL means do not write the Mutation to the WAL.\n     - ASYNC_WAL means write the Mutation to the WAL asynchronously,\n     - SYNC_WAL means write the Mutation to the WAL synchronously,\n     - FSYNC_WAL means Write the Mutation to the WAL synchronously and force the entries to disk.\n    '
    USE_DEFAULT = 0
    SKIP_WAL = 1
    ASYNC_WAL = 2
    SYNC_WAL = 3
    FSYNC_WAL = 4
    _VALUES_TO_NAMES = {0:'USE_DEFAULT', 
     1:'SKIP_WAL', 
     2:'ASYNC_WAL', 
     3:'SYNC_WAL', 
     4:'FSYNC_WAL'}
    _NAMES_TO_VALUES = {'USE_DEFAULT':0, 
     'SKIP_WAL':1, 
     'ASYNC_WAL':2, 
     'SYNC_WAL':3, 
     'FSYNC_WAL':4}


class TConsistency(object):
    __doc__ = '\n    Specify Consistency:\n     - STRONG means reads only from primary region\n     - TIMELINE means reads might return values from secondary region replicas\n    '
    STRONG = 1
    TIMELINE = 2
    _VALUES_TO_NAMES = {1:'STRONG', 
     2:'TIMELINE'}
    _NAMES_TO_VALUES = {'STRONG':1, 
     'TIMELINE':2}


class TReadType(object):
    DEFAULT = 1
    STREAM = 2
    PREAD = 3
    _VALUES_TO_NAMES = {1:'DEFAULT', 
     2:'STREAM', 
     3:'PREAD'}
    _NAMES_TO_VALUES = {'DEFAULT':1, 
     'STREAM':2, 
     'PREAD':3}


class TCompareOperator(object):
    __doc__ = '\n    Thrift wrapper around\n    org.apache.hadoop.hbase.CompareOperator.\n    '
    LESS = 0
    LESS_OR_EQUAL = 1
    EQUAL = 2
    NOT_EQUAL = 3
    GREATER_OR_EQUAL = 4
    GREATER = 5
    NO_OP = 6
    _VALUES_TO_NAMES = {0:'LESS', 
     1:'LESS_OR_EQUAL', 
     2:'EQUAL', 
     3:'NOT_EQUAL', 
     4:'GREATER_OR_EQUAL', 
     5:'GREATER', 
     6:'NO_OP'}
    _NAMES_TO_VALUES = {'LESS':0, 
     'LESS_OR_EQUAL':1, 
     'EQUAL':2, 
     'NOT_EQUAL':3, 
     'GREATER_OR_EQUAL':4, 
     'GREATER':5, 
     'NO_OP':6}


class TBloomFilterType(object):
    __doc__ = '\n    Thrift wrapper around\n    org.apache.hadoop.hbase.regionserver.BloomType\n    '
    NONE = 0
    ROW = 1
    ROWCOL = 2
    ROWPREFIX_FIXED_LENGTH = 3
    _VALUES_TO_NAMES = {0:'NONE', 
     1:'ROW', 
     2:'ROWCOL', 
     3:'ROWPREFIX_FIXED_LENGTH'}
    _NAMES_TO_VALUES = {'NONE':0, 
     'ROW':1, 
     'ROWCOL':2, 
     'ROWPREFIX_FIXED_LENGTH':3}


class TCompressionAlgorithm(object):
    __doc__ = '\n    Thrift wrapper around\n    org.apache.hadoop.hbase.io.compress.Algorithm\n    '
    LZO = 0
    GZ = 1
    NONE = 2
    SNAPPY = 3
    LZ4 = 4
    BZIP2 = 5
    ZSTD = 6
    _VALUES_TO_NAMES = {0:'LZO', 
     1:'GZ', 
     2:'NONE', 
     3:'SNAPPY', 
     4:'LZ4', 
     5:'BZIP2', 
     6:'ZSTD'}
    _NAMES_TO_VALUES = {'LZO':0, 
     'GZ':1, 
     'NONE':2, 
     'SNAPPY':3, 
     'LZ4':4, 
     'BZIP2':5, 
     'ZSTD':6}


class TDataBlockEncoding(object):
    __doc__ = '\n    Thrift wrapper around\n    org.apache.hadoop.hbase.io.encoding.DataBlockEncoding\n    '
    NONE = 0
    PREFIX = 2
    DIFF = 3
    FAST_DIFF = 4
    ROW_INDEX_V1 = 7
    _VALUES_TO_NAMES = {0:'NONE', 
     2:'PREFIX', 
     3:'DIFF', 
     4:'FAST_DIFF', 
     7:'ROW_INDEX_V1'}
    _NAMES_TO_VALUES = {'NONE':0, 
     'PREFIX':2, 
     'DIFF':3, 
     'FAST_DIFF':4, 
     'ROW_INDEX_V1':7}


class TKeepDeletedCells(object):
    __doc__ = '\n    Thrift wrapper around\n    org.apache.hadoop.hbase.KeepDeletedCells\n    '
    FALSE = 0
    TRUE = 1
    TTL = 2
    _VALUES_TO_NAMES = {0:'FALSE', 
     1:'TRUE', 
     2:'TTL'}
    _NAMES_TO_VALUES = {'FALSE':0, 
     'TRUE':1, 
     'TTL':2}


class TTimeRange(object):
    __doc__ = '\n    Attributes:\n     - minStamp\n     - maxStamp\n    '

    def __init__(self, minStamp=None, maxStamp=None):
        self.minStamp = minStamp
        self.maxStamp = maxStamp

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.I64:
                    self.minStamp = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I64:
                    self.maxStamp = iprot.readI64()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TTimeRange')
        if self.minStamp is not None:
            oprot.writeFieldBegin('minStamp', TType.I64, 1)
            oprot.writeI64(self.minStamp)
            oprot.writeFieldEnd()
        if self.maxStamp is not None:
            oprot.writeFieldBegin('maxStamp', TType.I64, 2)
            oprot.writeI64(self.maxStamp)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.minStamp is None:
            raise TProtocolException(message='Required field minStamp is unset!')
        if self.maxStamp is None:
            raise TProtocolException(message='Required field maxStamp is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TColumn(object):
    __doc__ = '\n    Addresses a single cell or multiple cells\n    in a HBase table by column family and optionally\n    a column qualifier and timestamp\n\n    Attributes:\n     - family\n     - qualifier\n     - timestamp\n    '

    def __init__(self, family=None, qualifier=None, timestamp=None):
        self.family = family
        self.qualifier = qualifier
        self.timestamp = timestamp

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.family = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.qualifier = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I64:
                    self.timestamp = iprot.readI64()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TColumn')
        if self.family is not None:
            oprot.writeFieldBegin('family', TType.STRING, 1)
            oprot.writeBinary(self.family)
            oprot.writeFieldEnd()
        if self.qualifier is not None:
            oprot.writeFieldBegin('qualifier', TType.STRING, 2)
            oprot.writeBinary(self.qualifier)
            oprot.writeFieldEnd()
        if self.timestamp is not None:
            oprot.writeFieldBegin('timestamp', TType.I64, 3)
            oprot.writeI64(self.timestamp)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.family is None:
            raise TProtocolException(message='Required field family is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TColumnValue(object):
    __doc__ = '\n    Represents a single cell and its value.\n\n    Attributes:\n     - family\n     - qualifier\n     - value\n     - timestamp\n     - tags\n     - type\n    '

    def __init__(self, family=None, qualifier=None, value=None, timestamp=None, tags=None, type=None):
        self.family = family
        self.qualifier = qualifier
        self.value = value
        self.timestamp = timestamp
        self.tags = tags
        self.type = type

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.family = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 2:
                    if ftype == TType.STRING:
                        self.qualifier = iprot.readBinary()
                    else:
                        iprot.skip(ftype)
                else:
                    if fid == 3:
                        if ftype == TType.STRING:
                            self.value = iprot.readBinary()
                        else:
                            iprot.skip(ftype)
                    else:
                        if fid == 4:
                            if ftype == TType.I64:
                                self.timestamp = iprot.readI64()
                            else:
                                iprot.skip(ftype)
                        else:
                            if fid == 5:
                                if ftype == TType.STRING:
                                    self.tags = iprot.readBinary()
                                else:
                                    iprot.skip(ftype)
                            else:
                                if fid == 6:
                                    if ftype == TType.BYTE:
                                        self.type = iprot.readByte()
                                    else:
                                        iprot.skip(ftype)
                                else:
                                    iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TColumnValue')
        if self.family is not None:
            oprot.writeFieldBegin('family', TType.STRING, 1)
            oprot.writeBinary(self.family)
            oprot.writeFieldEnd()
        if self.qualifier is not None:
            oprot.writeFieldBegin('qualifier', TType.STRING, 2)
            oprot.writeBinary(self.qualifier)
            oprot.writeFieldEnd()
        if self.value is not None:
            oprot.writeFieldBegin('value', TType.STRING, 3)
            oprot.writeBinary(self.value)
            oprot.writeFieldEnd()
        if self.timestamp is not None:
            oprot.writeFieldBegin('timestamp', TType.I64, 4)
            oprot.writeI64(self.timestamp)
            oprot.writeFieldEnd()
        if self.tags is not None:
            oprot.writeFieldBegin('tags', TType.STRING, 5)
            oprot.writeBinary(self.tags)
            oprot.writeFieldEnd()
        if self.type is not None:
            oprot.writeFieldBegin('type', TType.BYTE, 6)
            oprot.writeByte(self.type)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.family is None:
            raise TProtocolException(message='Required field family is unset!')
        if self.qualifier is None:
            raise TProtocolException(message='Required field qualifier is unset!')
        if self.value is None:
            raise TProtocolException(message='Required field value is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TColumnIncrement(object):
    __doc__ = '\n    Represents a single cell and the amount to increment it by\n\n    Attributes:\n     - family\n     - qualifier\n     - amount\n    '

    def __init__(self, family=None, qualifier=None, amount=1):
        self.family = family
        self.qualifier = qualifier
        self.amount = amount

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.family = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.qualifier = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I64:
                    self.amount = iprot.readI64()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TColumnIncrement')
        if self.family is not None:
            oprot.writeFieldBegin('family', TType.STRING, 1)
            oprot.writeBinary(self.family)
            oprot.writeFieldEnd()
        if self.qualifier is not None:
            oprot.writeFieldBegin('qualifier', TType.STRING, 2)
            oprot.writeBinary(self.qualifier)
            oprot.writeFieldEnd()
        if self.amount is not None:
            oprot.writeFieldBegin('amount', TType.I64, 3)
            oprot.writeI64(self.amount)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.family is None:
            raise TProtocolException(message='Required field family is unset!')
        if self.qualifier is None:
            raise TProtocolException(message='Required field qualifier is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TResult(object):
    __doc__ = '\n    if no Result is found, row and columnValues will not be set.\n\n    Attributes:\n     - row\n     - columnValues\n     - stale\n     - partial\n    '

    def __init__(self, row=None, columnValues=None, stale=False, partial=False):
        self.row = row
        self.columnValues = columnValues
        self.stale = stale
        self.partial = partial

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.row = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 2:
                    if ftype == TType.LIST:
                        self.columnValues = []
                        _etype3, _size0 = iprot.readListBegin()
                        for _i4 in range(_size0):
                            _elem5 = TColumnValue()
                            _elem5.read(iprot)
                            self.columnValues.append(_elem5)

                        iprot.readListEnd()
                    else:
                        iprot.skip(ftype)
                else:
                    if fid == 3:
                        if ftype == TType.BOOL:
                            self.stale = iprot.readBool()
                        else:
                            iprot.skip(ftype)
                    else:
                        if fid == 4:
                            if ftype == TType.BOOL:
                                self.partial = iprot.readBool()
                            else:
                                iprot.skip(ftype)
                        else:
                            iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TResult')
        if self.row is not None:
            oprot.writeFieldBegin('row', TType.STRING, 1)
            oprot.writeBinary(self.row)
            oprot.writeFieldEnd()
        if self.columnValues is not None:
            oprot.writeFieldBegin('columnValues', TType.LIST, 2)
            oprot.writeListBegin(TType.STRUCT, len(self.columnValues))
            for iter6 in self.columnValues:
                iter6.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.stale is not None:
            oprot.writeFieldBegin('stale', TType.BOOL, 3)
            oprot.writeBool(self.stale)
            oprot.writeFieldEnd()
        if self.partial is not None:
            oprot.writeFieldBegin('partial', TType.BOOL, 4)
            oprot.writeBool(self.partial)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.columnValues is None:
            raise TProtocolException(message='Required field columnValues is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TAuthorization(object):
    __doc__ = '\n    Attributes:\n     - labels\n    '

    def __init__(self, labels=None):
        self.labels = labels

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.LIST:
                    self.labels = []
                    _etype10, _size7 = iprot.readListBegin()
                    for _i11 in range(_size7):
                        _elem12 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        self.labels.append(_elem12)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TAuthorization')
        if self.labels is not None:
            oprot.writeFieldBegin('labels', TType.LIST, 1)
            oprot.writeListBegin(TType.STRING, len(self.labels))
            for iter13 in self.labels:
                oprot.writeString(iter13.encode('utf-8') if sys.version_info[0] == 2 else iter13)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TCellVisibility(object):
    __doc__ = '\n    Attributes:\n     - expression\n    '

    def __init__(self, expression=None):
        self.expression = expression

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.expression = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TCellVisibility')
        if self.expression is not None:
            oprot.writeFieldBegin('expression', TType.STRING, 1)
            oprot.writeString(self.expression.encode('utf-8') if sys.version_info[0] == 2 else self.expression)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TGet(object):
    __doc__ = '\n    Used to perform Get operations on a single row.\n\n    The scope can be further narrowed down by specifying a list of\n    columns or column families.\n\n    To get everything for a row, instantiate a Get object with just the row to get.\n    To further define the scope of what to get you can add a timestamp or time range\n    with an optional maximum number of versions to return.\n\n    If you specify a time range and a timestamp the range is ignored.\n    Timestamps on TColumns are ignored.\n\n    Attributes:\n     - row\n     - columns\n     - timestamp\n     - timeRange\n     - maxVersions\n     - filterString\n     - attributes\n     - authorizations\n     - consistency\n     - targetReplicaId\n     - cacheBlocks\n     - storeLimit\n     - storeOffset\n     - existence_only\n     - filterBytes\n    '

    def __init__(self, row=None, columns=None, timestamp=None, timeRange=None, maxVersions=None, filterString=None, attributes=None, authorizations=None, consistency=None, targetReplicaId=None, cacheBlocks=None, storeLimit=None, storeOffset=None, existence_only=None, filterBytes=None):
        self.row = row
        self.columns = columns
        self.timestamp = timestamp
        self.timeRange = timeRange
        self.maxVersions = maxVersions
        self.filterString = filterString
        self.attributes = attributes
        self.authorizations = authorizations
        self.consistency = consistency
        self.targetReplicaId = targetReplicaId
        self.cacheBlocks = cacheBlocks
        self.storeLimit = storeLimit
        self.storeOffset = storeOffset
        self.existence_only = existence_only
        self.filterBytes = filterBytes

    def read--- This code section failed: ---

 L. 888         0  LOAD_FAST                'iprot'
                2  LOAD_ATTR                _fast_decode
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    60  'to 60'
               10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'iprot'
               14  LOAD_ATTR                trans
               16  LOAD_GLOBAL              TTransport
               18  LOAD_ATTR                CReadableTransport
               20  CALL_FUNCTION_2       2  '2 positional arguments'
               22  POP_JUMP_IF_FALSE    60  'to 60'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                thrift_spec
               28  LOAD_CONST               None
               30  COMPARE_OP               is-not
               32  POP_JUMP_IF_FALSE    60  'to 60'

 L. 889        34  LOAD_FAST                'iprot'
               36  LOAD_METHOD              _fast_decode
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'iprot'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                __class__
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                thrift_spec
               50  BUILD_LIST_2          2 
               52  CALL_METHOD_3         3  '3 positional arguments'
               54  POP_TOP          

 L. 890        56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM            32  '32'
             60_1  COME_FROM            22  '22'
             60_2  COME_FROM             8  '8'

 L. 891        60  LOAD_FAST                'iprot'
               62  LOAD_METHOD              readStructBegin
               64  CALL_METHOD_0         0  '0 positional arguments'
               66  POP_TOP          

 L. 892     68_70  SETUP_LOOP          966  'to 966'

 L. 893        72  LOAD_FAST                'iprot'
               74  LOAD_METHOD              readFieldBegin
               76  CALL_METHOD_0         0  '0 positional arguments'
               78  UNPACK_SEQUENCE_3     3 
               80  STORE_FAST               'fname'
               82  STORE_FAST               'ftype'
               84  STORE_FAST               'fid'

 L. 894        86  LOAD_FAST                'ftype'
               88  LOAD_GLOBAL              TType
               90  LOAD_ATTR                STOP
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L. 895        96  BREAK_LOOP       
             98_0  COME_FROM            94  '94'

 L. 896        98  LOAD_FAST                'fid'
              100  LOAD_CONST               1
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   142  'to 142'

 L. 897       106  LOAD_FAST                'ftype'
              108  LOAD_GLOBAL              TType
              110  LOAD_ATTR                STRING
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   128  'to 128'

 L. 898       116  LOAD_FAST                'iprot'
              118  LOAD_METHOD              readBinary
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  LOAD_FAST                'self'
              124  STORE_ATTR               row
              126  JUMP_FORWARD        954  'to 954'
            128_0  COME_FROM           114  '114'

 L. 900       128  LOAD_FAST                'iprot'
              130  LOAD_METHOD              skip
              132  LOAD_FAST                'ftype'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  POP_TOP          
          138_140  JUMP_FORWARD        954  'to 954'
            142_0  COME_FROM           104  '104'

 L. 901       142  LOAD_FAST                'fid'
              144  LOAD_CONST               2
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   248  'to 248'

 L. 902       150  LOAD_FAST                'ftype'
              152  LOAD_GLOBAL              TType
              154  LOAD_ATTR                LIST
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   234  'to 234'

 L. 903       160  BUILD_LIST_0          0 
              162  LOAD_FAST                'self'
              164  STORE_ATTR               columns

 L. 904       166  LOAD_FAST                'iprot'
              168  LOAD_METHOD              readListBegin
              170  CALL_METHOD_0         0  '0 positional arguments'
              172  UNPACK_SEQUENCE_2     2 
              174  STORE_FAST               '_etype17'
              176  STORE_FAST               '_size14'

 L. 905       178  SETUP_LOOP          224  'to 224'
              180  LOAD_GLOBAL              range
              182  LOAD_FAST                '_size14'
              184  CALL_FUNCTION_1       1  '1 positional argument'
              186  GET_ITER         
              188  FOR_ITER            222  'to 222'
              190  STORE_FAST               '_i18'

 L. 906       192  LOAD_GLOBAL              TColumn
              194  CALL_FUNCTION_0       0  '0 positional arguments'
              196  STORE_FAST               '_elem19'

 L. 907       198  LOAD_FAST                '_elem19'
              200  LOAD_METHOD              read
              202  LOAD_FAST                'iprot'
              204  CALL_METHOD_1         1  '1 positional argument'
              206  POP_TOP          

 L. 908       208  LOAD_FAST                'self'
              210  LOAD_ATTR                columns
              212  LOAD_METHOD              append
              214  LOAD_FAST                '_elem19'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  POP_TOP          
              220  JUMP_BACK           188  'to 188'
              222  POP_BLOCK        
            224_0  COME_FROM_LOOP      178  '178'

 L. 909       224  LOAD_FAST                'iprot'
              226  LOAD_METHOD              readListEnd
              228  CALL_METHOD_0         0  '0 positional arguments'
              230  POP_TOP          
              232  JUMP_FORWARD        954  'to 954'
            234_0  COME_FROM           158  '158'

 L. 911       234  LOAD_FAST                'iprot'
              236  LOAD_METHOD              skip
              238  LOAD_FAST                'ftype'
              240  CALL_METHOD_1         1  '1 positional argument'
              242  POP_TOP          
          244_246  JUMP_FORWARD        954  'to 954'
            248_0  COME_FROM           148  '148'

 L. 912       248  LOAD_FAST                'fid'
              250  LOAD_CONST               3
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   296  'to 296'

 L. 913       258  LOAD_FAST                'ftype'
              260  LOAD_GLOBAL              TType
              262  LOAD_ATTR                I64
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   282  'to 282'

 L. 914       270  LOAD_FAST                'iprot'
              272  LOAD_METHOD              readI64
              274  CALL_METHOD_0         0  '0 positional arguments'
              276  LOAD_FAST                'self'
              278  STORE_ATTR               timestamp
              280  JUMP_FORWARD        954  'to 954'
            282_0  COME_FROM           266  '266'

 L. 916       282  LOAD_FAST                'iprot'
              284  LOAD_METHOD              skip
              286  LOAD_FAST                'ftype'
              288  CALL_METHOD_1         1  '1 positional argument'
              290  POP_TOP          
          292_294  JUMP_FORWARD        954  'to 954'
            296_0  COME_FROM           254  '254'

 L. 917       296  LOAD_FAST                'fid'
              298  LOAD_CONST               4
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_FALSE   354  'to 354'

 L. 918       306  LOAD_FAST                'ftype'
              308  LOAD_GLOBAL              TType
              310  LOAD_ATTR                STRUCT
              312  COMPARE_OP               ==
          314_316  POP_JUMP_IF_FALSE   340  'to 340'

 L. 919       318  LOAD_GLOBAL              TTimeRange
              320  CALL_FUNCTION_0       0  '0 positional arguments'
              322  LOAD_FAST                'self'
              324  STORE_ATTR               timeRange

 L. 920       326  LOAD_FAST                'self'
              328  LOAD_ATTR                timeRange
              330  LOAD_METHOD              read
              332  LOAD_FAST                'iprot'
              334  CALL_METHOD_1         1  '1 positional argument'
              336  POP_TOP          
              338  JUMP_FORWARD        954  'to 954'
            340_0  COME_FROM           314  '314'

 L. 922       340  LOAD_FAST                'iprot'
              342  LOAD_METHOD              skip
              344  LOAD_FAST                'ftype'
              346  CALL_METHOD_1         1  '1 positional argument'
              348  POP_TOP          
          350_352  JUMP_FORWARD        954  'to 954'
            354_0  COME_FROM           302  '302'

 L. 923       354  LOAD_FAST                'fid'
              356  LOAD_CONST               5
              358  COMPARE_OP               ==
          360_362  POP_JUMP_IF_FALSE   402  'to 402'

 L. 924       364  LOAD_FAST                'ftype'
              366  LOAD_GLOBAL              TType
              368  LOAD_ATTR                I32
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_FALSE   388  'to 388'

 L. 925       376  LOAD_FAST                'iprot'
              378  LOAD_METHOD              readI32
              380  CALL_METHOD_0         0  '0 positional arguments'
              382  LOAD_FAST                'self'
              384  STORE_ATTR               maxVersions
              386  JUMP_FORWARD        954  'to 954'
            388_0  COME_FROM           372  '372'

 L. 927       388  LOAD_FAST                'iprot'
              390  LOAD_METHOD              skip
              392  LOAD_FAST                'ftype'
              394  CALL_METHOD_1         1  '1 positional argument'
              396  POP_TOP          
          398_400  JUMP_FORWARD        954  'to 954'
            402_0  COME_FROM           360  '360'

 L. 928       402  LOAD_FAST                'fid'
              404  LOAD_CONST               6
              406  COMPARE_OP               ==
          408_410  POP_JUMP_IF_FALSE   450  'to 450'

 L. 929       412  LOAD_FAST                'ftype'
              414  LOAD_GLOBAL              TType
              416  LOAD_ATTR                STRING
              418  COMPARE_OP               ==
          420_422  POP_JUMP_IF_FALSE   436  'to 436'

 L. 930       424  LOAD_FAST                'iprot'
              426  LOAD_METHOD              readBinary
              428  CALL_METHOD_0         0  '0 positional arguments'
              430  LOAD_FAST                'self'
              432  STORE_ATTR               filterString
              434  JUMP_FORWARD        954  'to 954'
            436_0  COME_FROM           420  '420'

 L. 932       436  LOAD_FAST                'iprot'
              438  LOAD_METHOD              skip
              440  LOAD_FAST                'ftype'
              442  CALL_METHOD_1         1  '1 positional argument'
              444  POP_TOP          
          446_448  JUMP_FORWARD        954  'to 954'
            450_0  COME_FROM           408  '408'

 L. 933       450  LOAD_FAST                'fid'
              452  LOAD_CONST               7
              454  COMPARE_OP               ==
          456_458  POP_JUMP_IF_FALSE   562  'to 562'

 L. 934       460  LOAD_FAST                'ftype'
              462  LOAD_GLOBAL              TType
              464  LOAD_ATTR                MAP
              466  COMPARE_OP               ==
          468_470  POP_JUMP_IF_FALSE   548  'to 548'

 L. 935       472  BUILD_MAP_0           0 
              474  LOAD_FAST                'self'
              476  STORE_ATTR               attributes

 L. 936       478  LOAD_FAST                'iprot'
              480  LOAD_METHOD              readMapBegin
              482  CALL_METHOD_0         0  '0 positional arguments'
              484  UNPACK_SEQUENCE_3     3 
              486  STORE_FAST               '_ktype21'
              488  STORE_FAST               '_vtype22'
              490  STORE_FAST               '_size20'

 L. 937       492  SETUP_LOOP          538  'to 538'
              494  LOAD_GLOBAL              range
              496  LOAD_FAST                '_size20'
              498  CALL_FUNCTION_1       1  '1 positional argument'
              500  GET_ITER         
              502  FOR_ITER            536  'to 536'
              504  STORE_FAST               '_i24'

 L. 938       506  LOAD_FAST                'iprot'
              508  LOAD_METHOD              readBinary
              510  CALL_METHOD_0         0  '0 positional arguments'
              512  STORE_FAST               '_key25'

 L. 939       514  LOAD_FAST                'iprot'
              516  LOAD_METHOD              readBinary
              518  CALL_METHOD_0         0  '0 positional arguments'
              520  STORE_FAST               '_val26'

 L. 940       522  LOAD_FAST                '_val26'
              524  LOAD_FAST                'self'
              526  LOAD_ATTR                attributes
              528  LOAD_FAST                '_key25'
              530  STORE_SUBSCR     
          532_534  JUMP_BACK           502  'to 502'
              536  POP_BLOCK        
            538_0  COME_FROM_LOOP      492  '492'

 L. 941       538  LOAD_FAST                'iprot'
              540  LOAD_METHOD              readMapEnd
              542  CALL_METHOD_0         0  '0 positional arguments'
              544  POP_TOP          
              546  JUMP_FORWARD        954  'to 954'
            548_0  COME_FROM           468  '468'

 L. 943       548  LOAD_FAST                'iprot'
              550  LOAD_METHOD              skip
              552  LOAD_FAST                'ftype'
              554  CALL_METHOD_1         1  '1 positional argument'
              556  POP_TOP          
          558_560  JUMP_FORWARD        954  'to 954'
            562_0  COME_FROM           456  '456'

 L. 944       562  LOAD_FAST                'fid'
              564  LOAD_CONST               8
              566  COMPARE_OP               ==
          568_570  POP_JUMP_IF_FALSE   620  'to 620'

 L. 945       572  LOAD_FAST                'ftype'
              574  LOAD_GLOBAL              TType
              576  LOAD_ATTR                STRUCT
              578  COMPARE_OP               ==
          580_582  POP_JUMP_IF_FALSE   606  'to 606'

 L. 946       584  LOAD_GLOBAL              TAuthorization
              586  CALL_FUNCTION_0       0  '0 positional arguments'
              588  LOAD_FAST                'self'
              590  STORE_ATTR               authorizations

 L. 947       592  LOAD_FAST                'self'
              594  LOAD_ATTR                authorizations
              596  LOAD_METHOD              read
              598  LOAD_FAST                'iprot'
              600  CALL_METHOD_1         1  '1 positional argument'
              602  POP_TOP          
              604  JUMP_FORWARD        954  'to 954'
            606_0  COME_FROM           580  '580'

 L. 949       606  LOAD_FAST                'iprot'
              608  LOAD_METHOD              skip
              610  LOAD_FAST                'ftype'
              612  CALL_METHOD_1         1  '1 positional argument'
              614  POP_TOP          
          616_618  JUMP_FORWARD        954  'to 954'
            620_0  COME_FROM           568  '568'

 L. 950       620  LOAD_FAST                'fid'
              622  LOAD_CONST               9
              624  COMPARE_OP               ==
          626_628  POP_JUMP_IF_FALSE   668  'to 668'

 L. 951       630  LOAD_FAST                'ftype'
              632  LOAD_GLOBAL              TType
              634  LOAD_ATTR                I32
              636  COMPARE_OP               ==
          638_640  POP_JUMP_IF_FALSE   654  'to 654'

 L. 952       642  LOAD_FAST                'iprot'
              644  LOAD_METHOD              readI32
              646  CALL_METHOD_0         0  '0 positional arguments'
              648  LOAD_FAST                'self'
              650  STORE_ATTR               consistency
              652  JUMP_FORWARD        954  'to 954'
            654_0  COME_FROM           638  '638'

 L. 954       654  LOAD_FAST                'iprot'
              656  LOAD_METHOD              skip
              658  LOAD_FAST                'ftype'
              660  CALL_METHOD_1         1  '1 positional argument'
              662  POP_TOP          
          664_666  JUMP_FORWARD        954  'to 954'
            668_0  COME_FROM           626  '626'

 L. 955       668  LOAD_FAST                'fid'
              670  LOAD_CONST               10
              672  COMPARE_OP               ==
          674_676  POP_JUMP_IF_FALSE   714  'to 714'

 L. 956       678  LOAD_FAST                'ftype'
              680  LOAD_GLOBAL              TType
              682  LOAD_ATTR                I32
              684  COMPARE_OP               ==
          686_688  POP_JUMP_IF_FALSE   702  'to 702'

 L. 957       690  LOAD_FAST                'iprot'
              692  LOAD_METHOD              readI32
              694  CALL_METHOD_0         0  '0 positional arguments'
              696  LOAD_FAST                'self'
              698  STORE_ATTR               targetReplicaId
              700  JUMP_FORWARD        712  'to 712'
            702_0  COME_FROM           686  '686'

 L. 959       702  LOAD_FAST                'iprot'
              704  LOAD_METHOD              skip
              706  LOAD_FAST                'ftype'
              708  CALL_METHOD_1         1  '1 positional argument'
              710  POP_TOP          
            712_0  COME_FROM           700  '700'
              712  JUMP_FORWARD        954  'to 954'
            714_0  COME_FROM           674  '674'

 L. 960       714  LOAD_FAST                'fid'
              716  LOAD_CONST               11
              718  COMPARE_OP               ==
          720_722  POP_JUMP_IF_FALSE   760  'to 760'

 L. 961       724  LOAD_FAST                'ftype'
              726  LOAD_GLOBAL              TType
              728  LOAD_ATTR                BOOL
              730  COMPARE_OP               ==
          732_734  POP_JUMP_IF_FALSE   748  'to 748'

 L. 962       736  LOAD_FAST                'iprot'
              738  LOAD_METHOD              readBool
              740  CALL_METHOD_0         0  '0 positional arguments'
              742  LOAD_FAST                'self'
              744  STORE_ATTR               cacheBlocks
              746  JUMP_FORWARD        758  'to 758'
            748_0  COME_FROM           732  '732'

 L. 964       748  LOAD_FAST                'iprot'
              750  LOAD_METHOD              skip
              752  LOAD_FAST                'ftype'
              754  CALL_METHOD_1         1  '1 positional argument'
              756  POP_TOP          
            758_0  COME_FROM           746  '746'
              758  JUMP_FORWARD        954  'to 954'
            760_0  COME_FROM           720  '720'

 L. 965       760  LOAD_FAST                'fid'
              762  LOAD_CONST               12
              764  COMPARE_OP               ==
          766_768  POP_JUMP_IF_FALSE   806  'to 806'

 L. 966       770  LOAD_FAST                'ftype'
              772  LOAD_GLOBAL              TType
              774  LOAD_ATTR                I32
              776  COMPARE_OP               ==
          778_780  POP_JUMP_IF_FALSE   794  'to 794'

 L. 967       782  LOAD_FAST                'iprot'
              784  LOAD_METHOD              readI32
              786  CALL_METHOD_0         0  '0 positional arguments'
              788  LOAD_FAST                'self'
              790  STORE_ATTR               storeLimit
              792  JUMP_FORWARD        804  'to 804'
            794_0  COME_FROM           778  '778'

 L. 969       794  LOAD_FAST                'iprot'
              796  LOAD_METHOD              skip
              798  LOAD_FAST                'ftype'
              800  CALL_METHOD_1         1  '1 positional argument'
              802  POP_TOP          
            804_0  COME_FROM           792  '792'
              804  JUMP_FORWARD        954  'to 954'
            806_0  COME_FROM           766  '766'

 L. 970       806  LOAD_FAST                'fid'
              808  LOAD_CONST               13
              810  COMPARE_OP               ==
          812_814  POP_JUMP_IF_FALSE   852  'to 852'

 L. 971       816  LOAD_FAST                'ftype'
              818  LOAD_GLOBAL              TType
              820  LOAD_ATTR                I32
              822  COMPARE_OP               ==
          824_826  POP_JUMP_IF_FALSE   840  'to 840'

 L. 972       828  LOAD_FAST                'iprot'
              830  LOAD_METHOD              readI32
              832  CALL_METHOD_0         0  '0 positional arguments'
              834  LOAD_FAST                'self'
              836  STORE_ATTR               storeOffset
              838  JUMP_FORWARD        850  'to 850'
            840_0  COME_FROM           824  '824'

 L. 974       840  LOAD_FAST                'iprot'
              842  LOAD_METHOD              skip
              844  LOAD_FAST                'ftype'
              846  CALL_METHOD_1         1  '1 positional argument'
              848  POP_TOP          
            850_0  COME_FROM           838  '838'
              850  JUMP_FORWARD        954  'to 954'
            852_0  COME_FROM           812  '812'

 L. 975       852  LOAD_FAST                'fid'
              854  LOAD_CONST               14
              856  COMPARE_OP               ==
          858_860  POP_JUMP_IF_FALSE   898  'to 898'

 L. 976       862  LOAD_FAST                'ftype'
              864  LOAD_GLOBAL              TType
              866  LOAD_ATTR                BOOL
              868  COMPARE_OP               ==
          870_872  POP_JUMP_IF_FALSE   886  'to 886'

 L. 977       874  LOAD_FAST                'iprot'
              876  LOAD_METHOD              readBool
              878  CALL_METHOD_0         0  '0 positional arguments'
              880  LOAD_FAST                'self'
              882  STORE_ATTR               existence_only
              884  JUMP_FORWARD        896  'to 896'
            886_0  COME_FROM           870  '870'

 L. 979       886  LOAD_FAST                'iprot'
              888  LOAD_METHOD              skip
              890  LOAD_FAST                'ftype'
              892  CALL_METHOD_1         1  '1 positional argument'
              894  POP_TOP          
            896_0  COME_FROM           884  '884'
              896  JUMP_FORWARD        954  'to 954'
            898_0  COME_FROM           858  '858'

 L. 980       898  LOAD_FAST                'fid'
              900  LOAD_CONST               15
              902  COMPARE_OP               ==
          904_906  POP_JUMP_IF_FALSE   944  'to 944'

 L. 981       908  LOAD_FAST                'ftype'
              910  LOAD_GLOBAL              TType
              912  LOAD_ATTR                STRING
              914  COMPARE_OP               ==
          916_918  POP_JUMP_IF_FALSE   932  'to 932'

 L. 982       920  LOAD_FAST                'iprot'
              922  LOAD_METHOD              readBinary
              924  CALL_METHOD_0         0  '0 positional arguments'
              926  LOAD_FAST                'self'
              928  STORE_ATTR               filterBytes
              930  JUMP_FORWARD        942  'to 942'
            932_0  COME_FROM           916  '916'

 L. 984       932  LOAD_FAST                'iprot'
              934  LOAD_METHOD              skip
              936  LOAD_FAST                'ftype'
              938  CALL_METHOD_1         1  '1 positional argument'
            940_0  COME_FROM           652  '652'
            940_1  COME_FROM           604  '604'
            940_2  COME_FROM           546  '546'
            940_3  COME_FROM           434  '434'
            940_4  COME_FROM           386  '386'
            940_5  COME_FROM           338  '338'
            940_6  COME_FROM           280  '280'
            940_7  COME_FROM           232  '232'
            940_8  COME_FROM           126  '126'
              940  POP_TOP          
            942_0  COME_FROM           930  '930'
              942  JUMP_FORWARD        954  'to 954'
            944_0  COME_FROM           904  '904'

 L. 986       944  LOAD_FAST                'iprot'
              946  LOAD_METHOD              skip
              948  LOAD_FAST                'ftype'
              950  CALL_METHOD_1         1  '1 positional argument'
              952  POP_TOP          
            954_0  COME_FROM           942  '942'
            954_1  COME_FROM           896  '896'
            954_2  COME_FROM           850  '850'
            954_3  COME_FROM           804  '804'
            954_4  COME_FROM           758  '758'
            954_5  COME_FROM           712  '712'
            954_6  COME_FROM           664  '664'
            954_7  COME_FROM           616  '616'
            954_8  COME_FROM           558  '558'
            954_9  COME_FROM           446  '446'
           954_10  COME_FROM           398  '398'
           954_11  COME_FROM           350  '350'
           954_12  COME_FROM           292  '292'
           954_13  COME_FROM           244  '244'
           954_14  COME_FROM           138  '138'

 L. 987       954  LOAD_FAST                'iprot'
              956  LOAD_METHOD              readFieldEnd
              958  CALL_METHOD_0         0  '0 positional arguments'
              960  POP_TOP          
              962  JUMP_BACK            72  'to 72'
              964  POP_BLOCK        
            966_0  COME_FROM_LOOP       68  '68'

 L. 988       966  LOAD_FAST                'iprot'
              968  LOAD_METHOD              readStructEnd
              970  CALL_METHOD_0         0  '0 positional arguments'
              972  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 940_0

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TGet')
        if self.row is not None:
            oprot.writeFieldBegin('row', TType.STRING, 1)
            oprot.writeBinary(self.row)
            oprot.writeFieldEnd()
        if self.columns is not None:
            oprot.writeFieldBegin('columns', TType.LIST, 2)
            oprot.writeListBegin(TType.STRUCT, len(self.columns))
            for iter27 in self.columns:
                iter27.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.timestamp is not None:
            oprot.writeFieldBegin('timestamp', TType.I64, 3)
            oprot.writeI64(self.timestamp)
            oprot.writeFieldEnd()
        if self.timeRange is not None:
            oprot.writeFieldBegin('timeRange', TType.STRUCT, 4)
            self.timeRange.write(oprot)
            oprot.writeFieldEnd()
        if self.maxVersions is not None:
            oprot.writeFieldBegin('maxVersions', TType.I32, 5)
            oprot.writeI32(self.maxVersions)
            oprot.writeFieldEnd()
        if self.filterString is not None:
            oprot.writeFieldBegin('filterString', TType.STRING, 6)
            oprot.writeBinary(self.filterString)
            oprot.writeFieldEnd()
        if self.attributes is not None:
            oprot.writeFieldBegin('attributes', TType.MAP, 7)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.attributes))
            for kiter28, viter29 in self.attributes.items():
                oprot.writeBinary(kiter28)
                oprot.writeBinary(viter29)

            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        if self.authorizations is not None:
            oprot.writeFieldBegin('authorizations', TType.STRUCT, 8)
            self.authorizations.write(oprot)
            oprot.writeFieldEnd()
        if self.consistency is not None:
            oprot.writeFieldBegin('consistency', TType.I32, 9)
            oprot.writeI32(self.consistency)
            oprot.writeFieldEnd()
        if self.targetReplicaId is not None:
            oprot.writeFieldBegin('targetReplicaId', TType.I32, 10)
            oprot.writeI32(self.targetReplicaId)
            oprot.writeFieldEnd()
        if self.cacheBlocks is not None:
            oprot.writeFieldBegin('cacheBlocks', TType.BOOL, 11)
            oprot.writeBool(self.cacheBlocks)
            oprot.writeFieldEnd()
        if self.storeLimit is not None:
            oprot.writeFieldBegin('storeLimit', TType.I32, 12)
            oprot.writeI32(self.storeLimit)
            oprot.writeFieldEnd()
        if self.storeOffset is not None:
            oprot.writeFieldBegin('storeOffset', TType.I32, 13)
            oprot.writeI32(self.storeOffset)
            oprot.writeFieldEnd()
        if self.existence_only is not None:
            oprot.writeFieldBegin('existence_only', TType.BOOL, 14)
            oprot.writeBool(self.existence_only)
            oprot.writeFieldEnd()
        if self.filterBytes is not None:
            oprot.writeFieldBegin('filterBytes', TType.STRING, 15)
            oprot.writeBinary(self.filterBytes)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.row is None:
            raise TProtocolException(message='Required field row is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TPut(object):
    __doc__ = "\n    Used to perform Put operations for a single row.\n\n    Add column values to this object and they'll be added.\n    You can provide a default timestamp if the column values\n    don't have one. If you don't provide a default timestamp\n    the current time is inserted.\n\n    You can specify how this Put should be written to the write-ahead Log (WAL)\n    by changing the durability. If you don't provide durability, it defaults to\n    column family's default setting for durability.\n\n    Attributes:\n     - row\n     - columnValues\n     - timestamp\n     - attributes\n     - durability\n     - cellVisibility\n    "

    def __init__(self, row=None, columnValues=None, timestamp=None, attributes=None, durability=None, cellVisibility=None):
        self.row = row
        self.columnValues = columnValues
        self.timestamp = timestamp
        self.attributes = attributes
        self.durability = durability
        self.cellVisibility = cellVisibility

    def read--- This code section failed: ---

 L.1114         0  LOAD_FAST                'iprot'
                2  LOAD_ATTR                _fast_decode
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    60  'to 60'
               10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'iprot'
               14  LOAD_ATTR                trans
               16  LOAD_GLOBAL              TTransport
               18  LOAD_ATTR                CReadableTransport
               20  CALL_FUNCTION_2       2  '2 positional arguments'
               22  POP_JUMP_IF_FALSE    60  'to 60'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                thrift_spec
               28  LOAD_CONST               None
               30  COMPARE_OP               is-not
               32  POP_JUMP_IF_FALSE    60  'to 60'

 L.1115        34  LOAD_FAST                'iprot'
               36  LOAD_METHOD              _fast_decode
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'iprot'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                __class__
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                thrift_spec
               50  BUILD_LIST_2          2 
               52  CALL_METHOD_3         3  '3 positional arguments'
               54  POP_TOP          

 L.1116        56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM            32  '32'
             60_1  COME_FROM            22  '22'
             60_2  COME_FROM             8  '8'

 L.1117        60  LOAD_FAST                'iprot'
               62  LOAD_METHOD              readStructBegin
               64  CALL_METHOD_0         0  '0 positional arguments'
               66  POP_TOP          

 L.1118     68_70  SETUP_LOOP          528  'to 528'

 L.1119        72  LOAD_FAST                'iprot'
               74  LOAD_METHOD              readFieldBegin
               76  CALL_METHOD_0         0  '0 positional arguments'
               78  UNPACK_SEQUENCE_3     3 
               80  STORE_FAST               'fname'
               82  STORE_FAST               'ftype'
               84  STORE_FAST               'fid'

 L.1120        86  LOAD_FAST                'ftype'
               88  LOAD_GLOBAL              TType
               90  LOAD_ATTR                STOP
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L.1121        96  BREAK_LOOP       
             98_0  COME_FROM            94  '94'

 L.1122        98  LOAD_FAST                'fid'
              100  LOAD_CONST               1
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   142  'to 142'

 L.1123       106  LOAD_FAST                'ftype'
              108  LOAD_GLOBAL              TType
              110  LOAD_ATTR                STRING
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   128  'to 128'

 L.1124       116  LOAD_FAST                'iprot'
              118  LOAD_METHOD              readBinary
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  LOAD_FAST                'self'
              124  STORE_ATTR               row
              126  JUMP_FORWARD        516  'to 516'
            128_0  COME_FROM           114  '114'

 L.1126       128  LOAD_FAST                'iprot'
              130  LOAD_METHOD              skip
              132  LOAD_FAST                'ftype'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  POP_TOP          
          138_140  JUMP_FORWARD        516  'to 516'
            142_0  COME_FROM           104  '104'

 L.1127       142  LOAD_FAST                'fid'
              144  LOAD_CONST               2
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   248  'to 248'

 L.1128       150  LOAD_FAST                'ftype'
              152  LOAD_GLOBAL              TType
              154  LOAD_ATTR                LIST
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   234  'to 234'

 L.1129       160  BUILD_LIST_0          0 
              162  LOAD_FAST                'self'
              164  STORE_ATTR               columnValues

 L.1130       166  LOAD_FAST                'iprot'
              168  LOAD_METHOD              readListBegin
              170  CALL_METHOD_0         0  '0 positional arguments'
              172  UNPACK_SEQUENCE_2     2 
              174  STORE_FAST               '_etype33'
              176  STORE_FAST               '_size30'

 L.1131       178  SETUP_LOOP          224  'to 224'
              180  LOAD_GLOBAL              range
              182  LOAD_FAST                '_size30'
              184  CALL_FUNCTION_1       1  '1 positional argument'
              186  GET_ITER         
              188  FOR_ITER            222  'to 222'
              190  STORE_FAST               '_i34'

 L.1132       192  LOAD_GLOBAL              TColumnValue
              194  CALL_FUNCTION_0       0  '0 positional arguments'
              196  STORE_FAST               '_elem35'

 L.1133       198  LOAD_FAST                '_elem35'
              200  LOAD_METHOD              read
              202  LOAD_FAST                'iprot'
              204  CALL_METHOD_1         1  '1 positional argument'
              206  POP_TOP          

 L.1134       208  LOAD_FAST                'self'
              210  LOAD_ATTR                columnValues
              212  LOAD_METHOD              append
              214  LOAD_FAST                '_elem35'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  POP_TOP          
              220  JUMP_BACK           188  'to 188'
              222  POP_BLOCK        
            224_0  COME_FROM_LOOP      178  '178'

 L.1135       224  LOAD_FAST                'iprot'
              226  LOAD_METHOD              readListEnd
              228  CALL_METHOD_0         0  '0 positional arguments'
              230  POP_TOP          
              232  JUMP_FORWARD        516  'to 516'
            234_0  COME_FROM           158  '158'

 L.1137       234  LOAD_FAST                'iprot'
              236  LOAD_METHOD              skip
              238  LOAD_FAST                'ftype'
              240  CALL_METHOD_1         1  '1 positional argument'
              242  POP_TOP          
          244_246  JUMP_FORWARD        516  'to 516'
            248_0  COME_FROM           148  '148'

 L.1138       248  LOAD_FAST                'fid'
              250  LOAD_CONST               3
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   294  'to 294'

 L.1139       258  LOAD_FAST                'ftype'
              260  LOAD_GLOBAL              TType
              262  LOAD_ATTR                I64
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   282  'to 282'

 L.1140       270  LOAD_FAST                'iprot'
              272  LOAD_METHOD              readI64
              274  CALL_METHOD_0         0  '0 positional arguments'
              276  LOAD_FAST                'self'
              278  STORE_ATTR               timestamp
              280  JUMP_FORWARD        292  'to 292'
            282_0  COME_FROM           266  '266'

 L.1142       282  LOAD_FAST                'iprot'
              284  LOAD_METHOD              skip
              286  LOAD_FAST                'ftype'
              288  CALL_METHOD_1         1  '1 positional argument'
              290  POP_TOP          
            292_0  COME_FROM           280  '280'
              292  JUMP_FORWARD        516  'to 516'
            294_0  COME_FROM           254  '254'

 L.1143       294  LOAD_FAST                'fid'
              296  LOAD_CONST               5
              298  COMPARE_OP               ==
          300_302  POP_JUMP_IF_FALSE   404  'to 404'

 L.1144       304  LOAD_FAST                'ftype'
              306  LOAD_GLOBAL              TType
              308  LOAD_ATTR                MAP
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_FALSE   392  'to 392'

 L.1145       316  BUILD_MAP_0           0 
              318  LOAD_FAST                'self'
              320  STORE_ATTR               attributes

 L.1146       322  LOAD_FAST                'iprot'
              324  LOAD_METHOD              readMapBegin
              326  CALL_METHOD_0         0  '0 positional arguments'
              328  UNPACK_SEQUENCE_3     3 
              330  STORE_FAST               '_ktype37'
              332  STORE_FAST               '_vtype38'
              334  STORE_FAST               '_size36'

 L.1147       336  SETUP_LOOP          382  'to 382'
              338  LOAD_GLOBAL              range
              340  LOAD_FAST                '_size36'
              342  CALL_FUNCTION_1       1  '1 positional argument'
              344  GET_ITER         
              346  FOR_ITER            380  'to 380'
              348  STORE_FAST               '_i40'

 L.1148       350  LOAD_FAST                'iprot'
              352  LOAD_METHOD              readBinary
              354  CALL_METHOD_0         0  '0 positional arguments'
              356  STORE_FAST               '_key41'

 L.1149       358  LOAD_FAST                'iprot'
              360  LOAD_METHOD              readBinary
              362  CALL_METHOD_0         0  '0 positional arguments'
              364  STORE_FAST               '_val42'

 L.1150       366  LOAD_FAST                '_val42'
              368  LOAD_FAST                'self'
              370  LOAD_ATTR                attributes
              372  LOAD_FAST                '_key41'
              374  STORE_SUBSCR     
          376_378  JUMP_BACK           346  'to 346'
              380  POP_BLOCK        
            382_0  COME_FROM_LOOP      336  '336'

 L.1151       382  LOAD_FAST                'iprot'
              384  LOAD_METHOD              readMapEnd
              386  CALL_METHOD_0         0  '0 positional arguments'
              388  POP_TOP          
              390  JUMP_FORWARD        402  'to 402'
            392_0  COME_FROM           312  '312'

 L.1153       392  LOAD_FAST                'iprot'
              394  LOAD_METHOD              skip
              396  LOAD_FAST                'ftype'
              398  CALL_METHOD_1         1  '1 positional argument'
              400  POP_TOP          
            402_0  COME_FROM           390  '390'
              402  JUMP_FORWARD        516  'to 516'
            404_0  COME_FROM           300  '300'

 L.1154       404  LOAD_FAST                'fid'
              406  LOAD_CONST               6
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   450  'to 450'

 L.1155       414  LOAD_FAST                'ftype'
              416  LOAD_GLOBAL              TType
              418  LOAD_ATTR                I32
              420  COMPARE_OP               ==
          422_424  POP_JUMP_IF_FALSE   438  'to 438'

 L.1156       426  LOAD_FAST                'iprot'
              428  LOAD_METHOD              readI32
              430  CALL_METHOD_0         0  '0 positional arguments'
              432  LOAD_FAST                'self'
              434  STORE_ATTR               durability
              436  JUMP_FORWARD        448  'to 448'
            438_0  COME_FROM           422  '422'

 L.1158       438  LOAD_FAST                'iprot'
              440  LOAD_METHOD              skip
              442  LOAD_FAST                'ftype'
              444  CALL_METHOD_1         1  '1 positional argument'
              446  POP_TOP          
            448_0  COME_FROM           436  '436'
              448  JUMP_FORWARD        516  'to 516'
            450_0  COME_FROM           410  '410'

 L.1159       450  LOAD_FAST                'fid'
              452  LOAD_CONST               7
              454  COMPARE_OP               ==
          456_458  POP_JUMP_IF_FALSE   506  'to 506'

 L.1160       460  LOAD_FAST                'ftype'
              462  LOAD_GLOBAL              TType
              464  LOAD_ATTR                STRUCT
              466  COMPARE_OP               ==
          468_470  POP_JUMP_IF_FALSE   494  'to 494'

 L.1161       472  LOAD_GLOBAL              TCellVisibility
              474  CALL_FUNCTION_0       0  '0 positional arguments'
              476  LOAD_FAST                'self'
              478  STORE_ATTR               cellVisibility

 L.1162       480  LOAD_FAST                'self'
              482  LOAD_ATTR                cellVisibility
              484  LOAD_METHOD              read
              486  LOAD_FAST                'iprot'
              488  CALL_METHOD_1         1  '1 positional argument'
              490  POP_TOP          
              492  JUMP_FORWARD        504  'to 504'
            494_0  COME_FROM           468  '468'

 L.1164       494  LOAD_FAST                'iprot'
              496  LOAD_METHOD              skip
              498  LOAD_FAST                'ftype'
              500  CALL_METHOD_1         1  '1 positional argument'
            502_0  COME_FROM           232  '232'
            502_1  COME_FROM           126  '126'
              502  POP_TOP          
            504_0  COME_FROM           492  '492'
              504  JUMP_FORWARD        516  'to 516'
            506_0  COME_FROM           456  '456'

 L.1166       506  LOAD_FAST                'iprot'
              508  LOAD_METHOD              skip
              510  LOAD_FAST                'ftype'
              512  CALL_METHOD_1         1  '1 positional argument'
              514  POP_TOP          
            516_0  COME_FROM           504  '504'
            516_1  COME_FROM           448  '448'
            516_2  COME_FROM           402  '402'
            516_3  COME_FROM           292  '292'
            516_4  COME_FROM           244  '244'
            516_5  COME_FROM           138  '138'

 L.1167       516  LOAD_FAST                'iprot'
              518  LOAD_METHOD              readFieldEnd
              520  CALL_METHOD_0         0  '0 positional arguments'
              522  POP_TOP          
              524  JUMP_BACK            72  'to 72'
              526  POP_BLOCK        
            528_0  COME_FROM_LOOP       68  '68'

 L.1168       528  LOAD_FAST                'iprot'
              530  LOAD_METHOD              readStructEnd
              532  CALL_METHOD_0         0  '0 positional arguments'
              534  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 502_0

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TPut')
        if self.row is not None:
            oprot.writeFieldBegin('row', TType.STRING, 1)
            oprot.writeBinary(self.row)
            oprot.writeFieldEnd()
        if self.columnValues is not None:
            oprot.writeFieldBegin('columnValues', TType.LIST, 2)
            oprot.writeListBegin(TType.STRUCT, len(self.columnValues))
            for iter43 in self.columnValues:
                iter43.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.timestamp is not None:
            oprot.writeFieldBegin('timestamp', TType.I64, 3)
            oprot.writeI64(self.timestamp)
            oprot.writeFieldEnd()
        if self.attributes is not None:
            oprot.writeFieldBegin('attributes', TType.MAP, 5)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.attributes))
            for kiter44, viter45 in self.attributes.items():
                oprot.writeBinary(kiter44)
                oprot.writeBinary(viter45)

            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        if self.durability is not None:
            oprot.writeFieldBegin('durability', TType.I32, 6)
            oprot.writeI32(self.durability)
            oprot.writeFieldEnd()
        if self.cellVisibility is not None:
            oprot.writeFieldBegin('cellVisibility', TType.STRUCT, 7)
            self.cellVisibility.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.row is None:
            raise TProtocolException(message='Required field row is unset!')
        if self.columnValues is None:
            raise TProtocolException(message='Required field columnValues is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TDelete(object):
    __doc__ = "\n    Used to perform Delete operations on a single row.\n\n    The scope can be further narrowed down by specifying a list of\n    columns or column families as TColumns.\n\n    Specifying only a family in a TColumn will delete the whole family.\n    If a timestamp is specified all versions with a timestamp less than\n    or equal to this will be deleted. If no timestamp is specified the\n    current time will be used.\n\n    Specifying a family and a column qualifier in a TColumn will delete only\n    this qualifier. If a timestamp is specified only versions equal\n    to this timestamp will be deleted. If no timestamp is specified the\n    most recent version will be deleted.  To delete all previous versions,\n    specify the DELETE_COLUMNS TDeleteType.\n\n    The top level timestamp is only used if a complete row should be deleted\n    (i.e. no columns are passed) and if it is specified it works the same way\n    as if you had added a TColumn for every column family and this timestamp\n    (i.e. all versions older than or equal in all column families will be deleted)\n\n    You can specify how this Delete should be written to the write-ahead Log (WAL)\n    by changing the durability. If you don't provide durability, it defaults to\n    column family's default setting for durability.\n\n    Attributes:\n     - row\n     - columns\n     - timestamp\n     - deleteType\n     - attributes\n     - durability\n    "

    def __init__(self, row=None, columns=None, timestamp=None, deleteType=1, attributes=None, durability=None):
        self.row = row
        self.columns = columns
        self.timestamp = timestamp
        self.deleteType = deleteType
        self.attributes = attributes
        self.durability = durability

    def read--- This code section failed: ---

 L.1274         0  LOAD_FAST                'iprot'
                2  LOAD_ATTR                _fast_decode
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    60  'to 60'
               10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'iprot'
               14  LOAD_ATTR                trans
               16  LOAD_GLOBAL              TTransport
               18  LOAD_ATTR                CReadableTransport
               20  CALL_FUNCTION_2       2  '2 positional arguments'
               22  POP_JUMP_IF_FALSE    60  'to 60'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                thrift_spec
               28  LOAD_CONST               None
               30  COMPARE_OP               is-not
               32  POP_JUMP_IF_FALSE    60  'to 60'

 L.1275        34  LOAD_FAST                'iprot'
               36  LOAD_METHOD              _fast_decode
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'iprot'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                __class__
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                thrift_spec
               50  BUILD_LIST_2          2 
               52  CALL_METHOD_3         3  '3 positional arguments'
               54  POP_TOP          

 L.1276        56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM            32  '32'
             60_1  COME_FROM            22  '22'
             60_2  COME_FROM             8  '8'

 L.1277        60  LOAD_FAST                'iprot'
               62  LOAD_METHOD              readStructBegin
               64  CALL_METHOD_0         0  '0 positional arguments'
               66  POP_TOP          

 L.1278     68_70  SETUP_LOOP          518  'to 518'

 L.1279        72  LOAD_FAST                'iprot'
               74  LOAD_METHOD              readFieldBegin
               76  CALL_METHOD_0         0  '0 positional arguments'
               78  UNPACK_SEQUENCE_3     3 
               80  STORE_FAST               'fname'
               82  STORE_FAST               'ftype'
               84  STORE_FAST               'fid'

 L.1280        86  LOAD_FAST                'ftype'
               88  LOAD_GLOBAL              TType
               90  LOAD_ATTR                STOP
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L.1281        96  BREAK_LOOP       
             98_0  COME_FROM            94  '94'

 L.1282        98  LOAD_FAST                'fid'
              100  LOAD_CONST               1
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   142  'to 142'

 L.1283       106  LOAD_FAST                'ftype'
              108  LOAD_GLOBAL              TType
              110  LOAD_ATTR                STRING
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   128  'to 128'

 L.1284       116  LOAD_FAST                'iprot'
              118  LOAD_METHOD              readBinary
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  LOAD_FAST                'self'
              124  STORE_ATTR               row
              126  JUMP_FORWARD        506  'to 506'
            128_0  COME_FROM           114  '114'

 L.1286       128  LOAD_FAST                'iprot'
              130  LOAD_METHOD              skip
              132  LOAD_FAST                'ftype'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  POP_TOP          
          138_140  JUMP_FORWARD        506  'to 506'
            142_0  COME_FROM           104  '104'

 L.1287       142  LOAD_FAST                'fid'
              144  LOAD_CONST               2
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   248  'to 248'

 L.1288       150  LOAD_FAST                'ftype'
              152  LOAD_GLOBAL              TType
              154  LOAD_ATTR                LIST
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   234  'to 234'

 L.1289       160  BUILD_LIST_0          0 
              162  LOAD_FAST                'self'
              164  STORE_ATTR               columns

 L.1290       166  LOAD_FAST                'iprot'
              168  LOAD_METHOD              readListBegin
              170  CALL_METHOD_0         0  '0 positional arguments'
              172  UNPACK_SEQUENCE_2     2 
              174  STORE_FAST               '_etype49'
              176  STORE_FAST               '_size46'

 L.1291       178  SETUP_LOOP          224  'to 224'
              180  LOAD_GLOBAL              range
              182  LOAD_FAST                '_size46'
              184  CALL_FUNCTION_1       1  '1 positional argument'
              186  GET_ITER         
              188  FOR_ITER            222  'to 222'
              190  STORE_FAST               '_i50'

 L.1292       192  LOAD_GLOBAL              TColumn
              194  CALL_FUNCTION_0       0  '0 positional arguments'
              196  STORE_FAST               '_elem51'

 L.1293       198  LOAD_FAST                '_elem51'
              200  LOAD_METHOD              read
              202  LOAD_FAST                'iprot'
              204  CALL_METHOD_1         1  '1 positional argument'
              206  POP_TOP          

 L.1294       208  LOAD_FAST                'self'
              210  LOAD_ATTR                columns
              212  LOAD_METHOD              append
              214  LOAD_FAST                '_elem51'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  POP_TOP          
              220  JUMP_BACK           188  'to 188'
              222  POP_BLOCK        
            224_0  COME_FROM_LOOP      178  '178'

 L.1295       224  LOAD_FAST                'iprot'
              226  LOAD_METHOD              readListEnd
              228  CALL_METHOD_0         0  '0 positional arguments'
              230  POP_TOP          
              232  JUMP_FORWARD        506  'to 506'
            234_0  COME_FROM           158  '158'

 L.1297       234  LOAD_FAST                'iprot'
              236  LOAD_METHOD              skip
              238  LOAD_FAST                'ftype'
              240  CALL_METHOD_1         1  '1 positional argument'
              242  POP_TOP          
          244_246  JUMP_FORWARD        506  'to 506'
            248_0  COME_FROM           148  '148'

 L.1298       248  LOAD_FAST                'fid'
              250  LOAD_CONST               3
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   294  'to 294'

 L.1299       258  LOAD_FAST                'ftype'
              260  LOAD_GLOBAL              TType
              262  LOAD_ATTR                I64
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   282  'to 282'

 L.1300       270  LOAD_FAST                'iprot'
              272  LOAD_METHOD              readI64
              274  CALL_METHOD_0         0  '0 positional arguments'
              276  LOAD_FAST                'self'
              278  STORE_ATTR               timestamp
              280  JUMP_FORWARD        292  'to 292'
            282_0  COME_FROM           266  '266'

 L.1302       282  LOAD_FAST                'iprot'
              284  LOAD_METHOD              skip
              286  LOAD_FAST                'ftype'
              288  CALL_METHOD_1         1  '1 positional argument'
              290  POP_TOP          
            292_0  COME_FROM           280  '280'
              292  JUMP_FORWARD        506  'to 506'
            294_0  COME_FROM           254  '254'

 L.1303       294  LOAD_FAST                'fid'
              296  LOAD_CONST               4
              298  COMPARE_OP               ==
          300_302  POP_JUMP_IF_FALSE   340  'to 340'

 L.1304       304  LOAD_FAST                'ftype'
              306  LOAD_GLOBAL              TType
              308  LOAD_ATTR                I32
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_FALSE   328  'to 328'

 L.1305       316  LOAD_FAST                'iprot'
              318  LOAD_METHOD              readI32
              320  CALL_METHOD_0         0  '0 positional arguments'
              322  LOAD_FAST                'self'
              324  STORE_ATTR               deleteType
              326  JUMP_FORWARD        338  'to 338'
            328_0  COME_FROM           312  '312'

 L.1307       328  LOAD_FAST                'iprot'
              330  LOAD_METHOD              skip
              332  LOAD_FAST                'ftype'
              334  CALL_METHOD_1         1  '1 positional argument'
              336  POP_TOP          
            338_0  COME_FROM           326  '326'
              338  JUMP_FORWARD        506  'to 506'
            340_0  COME_FROM           300  '300'

 L.1308       340  LOAD_FAST                'fid'
              342  LOAD_CONST               6
              344  COMPARE_OP               ==
          346_348  POP_JUMP_IF_FALSE   450  'to 450'

 L.1309       350  LOAD_FAST                'ftype'
              352  LOAD_GLOBAL              TType
              354  LOAD_ATTR                MAP
              356  COMPARE_OP               ==
          358_360  POP_JUMP_IF_FALSE   438  'to 438'

 L.1310       362  BUILD_MAP_0           0 
              364  LOAD_FAST                'self'
              366  STORE_ATTR               attributes

 L.1311       368  LOAD_FAST                'iprot'
              370  LOAD_METHOD              readMapBegin
              372  CALL_METHOD_0         0  '0 positional arguments'
              374  UNPACK_SEQUENCE_3     3 
              376  STORE_FAST               '_ktype53'
              378  STORE_FAST               '_vtype54'
              380  STORE_FAST               '_size52'

 L.1312       382  SETUP_LOOP          428  'to 428'
              384  LOAD_GLOBAL              range
              386  LOAD_FAST                '_size52'
              388  CALL_FUNCTION_1       1  '1 positional argument'
              390  GET_ITER         
              392  FOR_ITER            426  'to 426'
              394  STORE_FAST               '_i56'

 L.1313       396  LOAD_FAST                'iprot'
              398  LOAD_METHOD              readBinary
              400  CALL_METHOD_0         0  '0 positional arguments'
              402  STORE_FAST               '_key57'

 L.1314       404  LOAD_FAST                'iprot'
              406  LOAD_METHOD              readBinary
              408  CALL_METHOD_0         0  '0 positional arguments'
              410  STORE_FAST               '_val58'

 L.1315       412  LOAD_FAST                '_val58'
              414  LOAD_FAST                'self'
              416  LOAD_ATTR                attributes
              418  LOAD_FAST                '_key57'
              420  STORE_SUBSCR     
          422_424  JUMP_BACK           392  'to 392'
              426  POP_BLOCK        
            428_0  COME_FROM_LOOP      382  '382'

 L.1316       428  LOAD_FAST                'iprot'
              430  LOAD_METHOD              readMapEnd
              432  CALL_METHOD_0         0  '0 positional arguments'
              434  POP_TOP          
              436  JUMP_FORWARD        448  'to 448'
            438_0  COME_FROM           358  '358'

 L.1318       438  LOAD_FAST                'iprot'
              440  LOAD_METHOD              skip
              442  LOAD_FAST                'ftype'
              444  CALL_METHOD_1         1  '1 positional argument'
              446  POP_TOP          
            448_0  COME_FROM           436  '436'
              448  JUMP_FORWARD        506  'to 506'
            450_0  COME_FROM           346  '346'

 L.1319       450  LOAD_FAST                'fid'
              452  LOAD_CONST               7
              454  COMPARE_OP               ==
          456_458  POP_JUMP_IF_FALSE   496  'to 496'

 L.1320       460  LOAD_FAST                'ftype'
              462  LOAD_GLOBAL              TType
              464  LOAD_ATTR                I32
              466  COMPARE_OP               ==
          468_470  POP_JUMP_IF_FALSE   484  'to 484'

 L.1321       472  LOAD_FAST                'iprot'
              474  LOAD_METHOD              readI32
              476  CALL_METHOD_0         0  '0 positional arguments'
              478  LOAD_FAST                'self'
              480  STORE_ATTR               durability
              482  JUMP_FORWARD        494  'to 494'
            484_0  COME_FROM           468  '468'

 L.1323       484  LOAD_FAST                'iprot'
              486  LOAD_METHOD              skip
              488  LOAD_FAST                'ftype'
              490  CALL_METHOD_1         1  '1 positional argument'
            492_0  COME_FROM           232  '232'
            492_1  COME_FROM           126  '126'
              492  POP_TOP          
            494_0  COME_FROM           482  '482'
              494  JUMP_FORWARD        506  'to 506'
            496_0  COME_FROM           456  '456'

 L.1325       496  LOAD_FAST                'iprot'
              498  LOAD_METHOD              skip
              500  LOAD_FAST                'ftype'
              502  CALL_METHOD_1         1  '1 positional argument'
              504  POP_TOP          
            506_0  COME_FROM           494  '494'
            506_1  COME_FROM           448  '448'
            506_2  COME_FROM           338  '338'
            506_3  COME_FROM           292  '292'
            506_4  COME_FROM           244  '244'
            506_5  COME_FROM           138  '138'

 L.1326       506  LOAD_FAST                'iprot'
              508  LOAD_METHOD              readFieldEnd
              510  CALL_METHOD_0         0  '0 positional arguments'
              512  POP_TOP          
              514  JUMP_BACK            72  'to 72'
              516  POP_BLOCK        
            518_0  COME_FROM_LOOP       68  '68'

 L.1327       518  LOAD_FAST                'iprot'
              520  LOAD_METHOD              readStructEnd
              522  CALL_METHOD_0         0  '0 positional arguments'
              524  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 492_0

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TDelete')
        if self.row is not None:
            oprot.writeFieldBegin('row', TType.STRING, 1)
            oprot.writeBinary(self.row)
            oprot.writeFieldEnd()
        if self.columns is not None:
            oprot.writeFieldBegin('columns', TType.LIST, 2)
            oprot.writeListBegin(TType.STRUCT, len(self.columns))
            for iter59 in self.columns:
                iter59.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.timestamp is not None:
            oprot.writeFieldBegin('timestamp', TType.I64, 3)
            oprot.writeI64(self.timestamp)
            oprot.writeFieldEnd()
        if self.deleteType is not None:
            oprot.writeFieldBegin('deleteType', TType.I32, 4)
            oprot.writeI32(self.deleteType)
            oprot.writeFieldEnd()
        if self.attributes is not None:
            oprot.writeFieldBegin('attributes', TType.MAP, 6)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.attributes))
            for kiter60, viter61 in self.attributes.items():
                oprot.writeBinary(kiter60)
                oprot.writeBinary(viter61)

            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        if self.durability is not None:
            oprot.writeFieldBegin('durability', TType.I32, 7)
            oprot.writeI32(self.durability)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.row is None:
            raise TProtocolException(message='Required field row is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TIncrement(object):
    __doc__ = "\n    Used to perform Increment operations for a single row.\n\n    You can specify how this Increment should be written to the write-ahead Log (WAL)\n    by changing the durability. If you don't provide durability, it defaults to\n    column family's default setting for durability.\n\n    Attributes:\n     - row\n     - columns\n     - attributes\n     - durability\n     - cellVisibility\n     - returnResults\n    "

    def __init__(self, row=None, columns=None, attributes=None, durability=None, cellVisibility=None, returnResults=None):
        self.row = row
        self.columns = columns
        self.attributes = attributes
        self.durability = durability
        self.cellVisibility = cellVisibility
        self.returnResults = returnResults

    def read--- This code section failed: ---

 L.1412         0  LOAD_FAST                'iprot'
                2  LOAD_ATTR                _fast_decode
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    60  'to 60'
               10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'iprot'
               14  LOAD_ATTR                trans
               16  LOAD_GLOBAL              TTransport
               18  LOAD_ATTR                CReadableTransport
               20  CALL_FUNCTION_2       2  '2 positional arguments'
               22  POP_JUMP_IF_FALSE    60  'to 60'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                thrift_spec
               28  LOAD_CONST               None
               30  COMPARE_OP               is-not
               32  POP_JUMP_IF_FALSE    60  'to 60'

 L.1413        34  LOAD_FAST                'iprot'
               36  LOAD_METHOD              _fast_decode
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'iprot'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                __class__
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                thrift_spec
               50  BUILD_LIST_2          2 
               52  CALL_METHOD_3         3  '3 positional arguments'
               54  POP_TOP          

 L.1414        56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM            32  '32'
             60_1  COME_FROM            22  '22'
             60_2  COME_FROM             8  '8'

 L.1415        60  LOAD_FAST                'iprot'
               62  LOAD_METHOD              readStructBegin
               64  CALL_METHOD_0         0  '0 positional arguments'
               66  POP_TOP          

 L.1416     68_70  SETUP_LOOP          528  'to 528'

 L.1417        72  LOAD_FAST                'iprot'
               74  LOAD_METHOD              readFieldBegin
               76  CALL_METHOD_0         0  '0 positional arguments'
               78  UNPACK_SEQUENCE_3     3 
               80  STORE_FAST               'fname'
               82  STORE_FAST               'ftype'
               84  STORE_FAST               'fid'

 L.1418        86  LOAD_FAST                'ftype'
               88  LOAD_GLOBAL              TType
               90  LOAD_ATTR                STOP
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L.1419        96  BREAK_LOOP       
             98_0  COME_FROM            94  '94'

 L.1420        98  LOAD_FAST                'fid'
              100  LOAD_CONST               1
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   142  'to 142'

 L.1421       106  LOAD_FAST                'ftype'
              108  LOAD_GLOBAL              TType
              110  LOAD_ATTR                STRING
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   128  'to 128'

 L.1422       116  LOAD_FAST                'iprot'
              118  LOAD_METHOD              readBinary
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  LOAD_FAST                'self'
              124  STORE_ATTR               row
              126  JUMP_FORWARD        516  'to 516'
            128_0  COME_FROM           114  '114'

 L.1424       128  LOAD_FAST                'iprot'
              130  LOAD_METHOD              skip
              132  LOAD_FAST                'ftype'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  POP_TOP          
          138_140  JUMP_FORWARD        516  'to 516'
            142_0  COME_FROM           104  '104'

 L.1425       142  LOAD_FAST                'fid'
              144  LOAD_CONST               2
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   248  'to 248'

 L.1426       150  LOAD_FAST                'ftype'
              152  LOAD_GLOBAL              TType
              154  LOAD_ATTR                LIST
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   234  'to 234'

 L.1427       160  BUILD_LIST_0          0 
              162  LOAD_FAST                'self'
              164  STORE_ATTR               columns

 L.1428       166  LOAD_FAST                'iprot'
              168  LOAD_METHOD              readListBegin
              170  CALL_METHOD_0         0  '0 positional arguments'
              172  UNPACK_SEQUENCE_2     2 
              174  STORE_FAST               '_etype65'
              176  STORE_FAST               '_size62'

 L.1429       178  SETUP_LOOP          224  'to 224'
              180  LOAD_GLOBAL              range
              182  LOAD_FAST                '_size62'
              184  CALL_FUNCTION_1       1  '1 positional argument'
              186  GET_ITER         
              188  FOR_ITER            222  'to 222'
              190  STORE_FAST               '_i66'

 L.1430       192  LOAD_GLOBAL              TColumnIncrement
              194  CALL_FUNCTION_0       0  '0 positional arguments'
              196  STORE_FAST               '_elem67'

 L.1431       198  LOAD_FAST                '_elem67'
              200  LOAD_METHOD              read
              202  LOAD_FAST                'iprot'
              204  CALL_METHOD_1         1  '1 positional argument'
              206  POP_TOP          

 L.1432       208  LOAD_FAST                'self'
              210  LOAD_ATTR                columns
              212  LOAD_METHOD              append
              214  LOAD_FAST                '_elem67'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  POP_TOP          
              220  JUMP_BACK           188  'to 188'
              222  POP_BLOCK        
            224_0  COME_FROM_LOOP      178  '178'

 L.1433       224  LOAD_FAST                'iprot'
              226  LOAD_METHOD              readListEnd
              228  CALL_METHOD_0         0  '0 positional arguments'
              230  POP_TOP          
              232  JUMP_FORWARD        516  'to 516'
            234_0  COME_FROM           158  '158'

 L.1435       234  LOAD_FAST                'iprot'
              236  LOAD_METHOD              skip
              238  LOAD_FAST                'ftype'
              240  CALL_METHOD_1         1  '1 positional argument'
              242  POP_TOP          
          244_246  JUMP_FORWARD        516  'to 516'
            248_0  COME_FROM           148  '148'

 L.1436       248  LOAD_FAST                'fid'
              250  LOAD_CONST               4
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   358  'to 358'

 L.1437       258  LOAD_FAST                'ftype'
              260  LOAD_GLOBAL              TType
              262  LOAD_ATTR                MAP
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   346  'to 346'

 L.1438       270  BUILD_MAP_0           0 
              272  LOAD_FAST                'self'
              274  STORE_ATTR               attributes

 L.1439       276  LOAD_FAST                'iprot'
              278  LOAD_METHOD              readMapBegin
              280  CALL_METHOD_0         0  '0 positional arguments'
              282  UNPACK_SEQUENCE_3     3 
              284  STORE_FAST               '_ktype69'
              286  STORE_FAST               '_vtype70'
              288  STORE_FAST               '_size68'

 L.1440       290  SETUP_LOOP          336  'to 336'
              292  LOAD_GLOBAL              range
              294  LOAD_FAST                '_size68'
              296  CALL_FUNCTION_1       1  '1 positional argument'
              298  GET_ITER         
              300  FOR_ITER            334  'to 334'
              302  STORE_FAST               '_i72'

 L.1441       304  LOAD_FAST                'iprot'
              306  LOAD_METHOD              readBinary
              308  CALL_METHOD_0         0  '0 positional arguments'
              310  STORE_FAST               '_key73'

 L.1442       312  LOAD_FAST                'iprot'
              314  LOAD_METHOD              readBinary
              316  CALL_METHOD_0         0  '0 positional arguments'
              318  STORE_FAST               '_val74'

 L.1443       320  LOAD_FAST                '_val74'
              322  LOAD_FAST                'self'
              324  LOAD_ATTR                attributes
              326  LOAD_FAST                '_key73'
              328  STORE_SUBSCR     
          330_332  JUMP_BACK           300  'to 300'
              334  POP_BLOCK        
            336_0  COME_FROM_LOOP      290  '290'

 L.1444       336  LOAD_FAST                'iprot'
              338  LOAD_METHOD              readMapEnd
              340  CALL_METHOD_0         0  '0 positional arguments'
              342  POP_TOP          
              344  JUMP_FORWARD        356  'to 356'
            346_0  COME_FROM           266  '266'

 L.1446       346  LOAD_FAST                'iprot'
              348  LOAD_METHOD              skip
              350  LOAD_FAST                'ftype'
              352  CALL_METHOD_1         1  '1 positional argument'
              354  POP_TOP          
            356_0  COME_FROM           344  '344'
              356  JUMP_FORWARD        516  'to 516'
            358_0  COME_FROM           254  '254'

 L.1447       358  LOAD_FAST                'fid'
              360  LOAD_CONST               5
              362  COMPARE_OP               ==
          364_366  POP_JUMP_IF_FALSE   404  'to 404'

 L.1448       368  LOAD_FAST                'ftype'
              370  LOAD_GLOBAL              TType
              372  LOAD_ATTR                I32
              374  COMPARE_OP               ==
          376_378  POP_JUMP_IF_FALSE   392  'to 392'

 L.1449       380  LOAD_FAST                'iprot'
              382  LOAD_METHOD              readI32
              384  CALL_METHOD_0         0  '0 positional arguments'
              386  LOAD_FAST                'self'
              388  STORE_ATTR               durability
              390  JUMP_FORWARD        402  'to 402'
            392_0  COME_FROM           376  '376'

 L.1451       392  LOAD_FAST                'iprot'
              394  LOAD_METHOD              skip
              396  LOAD_FAST                'ftype'
              398  CALL_METHOD_1         1  '1 positional argument'
              400  POP_TOP          
            402_0  COME_FROM           390  '390'
              402  JUMP_FORWARD        516  'to 516'
            404_0  COME_FROM           364  '364'

 L.1452       404  LOAD_FAST                'fid'
              406  LOAD_CONST               6
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   460  'to 460'

 L.1453       414  LOAD_FAST                'ftype'
              416  LOAD_GLOBAL              TType
              418  LOAD_ATTR                STRUCT
              420  COMPARE_OP               ==
          422_424  POP_JUMP_IF_FALSE   448  'to 448'

 L.1454       426  LOAD_GLOBAL              TCellVisibility
              428  CALL_FUNCTION_0       0  '0 positional arguments'
              430  LOAD_FAST                'self'
              432  STORE_ATTR               cellVisibility

 L.1455       434  LOAD_FAST                'self'
              436  LOAD_ATTR                cellVisibility
              438  LOAD_METHOD              read
              440  LOAD_FAST                'iprot'
              442  CALL_METHOD_1         1  '1 positional argument'
              444  POP_TOP          
              446  JUMP_FORWARD        458  'to 458'
            448_0  COME_FROM           422  '422'

 L.1457       448  LOAD_FAST                'iprot'
              450  LOAD_METHOD              skip
              452  LOAD_FAST                'ftype'
              454  CALL_METHOD_1         1  '1 positional argument'
              456  POP_TOP          
            458_0  COME_FROM           446  '446'
              458  JUMP_FORWARD        516  'to 516'
            460_0  COME_FROM           410  '410'

 L.1458       460  LOAD_FAST                'fid'
              462  LOAD_CONST               7
              464  COMPARE_OP               ==
          466_468  POP_JUMP_IF_FALSE   506  'to 506'

 L.1459       470  LOAD_FAST                'ftype'
              472  LOAD_GLOBAL              TType
              474  LOAD_ATTR                BOOL
              476  COMPARE_OP               ==
          478_480  POP_JUMP_IF_FALSE   494  'to 494'

 L.1460       482  LOAD_FAST                'iprot'
              484  LOAD_METHOD              readBool
              486  CALL_METHOD_0         0  '0 positional arguments'
              488  LOAD_FAST                'self'
              490  STORE_ATTR               returnResults
              492  JUMP_FORWARD        504  'to 504'
            494_0  COME_FROM           478  '478'

 L.1462       494  LOAD_FAST                'iprot'
              496  LOAD_METHOD              skip
              498  LOAD_FAST                'ftype'
              500  CALL_METHOD_1         1  '1 positional argument'
            502_0  COME_FROM           232  '232'
            502_1  COME_FROM           126  '126'
              502  POP_TOP          
            504_0  COME_FROM           492  '492'
              504  JUMP_FORWARD        516  'to 516'
            506_0  COME_FROM           466  '466'

 L.1464       506  LOAD_FAST                'iprot'
              508  LOAD_METHOD              skip
              510  LOAD_FAST                'ftype'
              512  CALL_METHOD_1         1  '1 positional argument'
              514  POP_TOP          
            516_0  COME_FROM           504  '504'
            516_1  COME_FROM           458  '458'
            516_2  COME_FROM           402  '402'
            516_3  COME_FROM           356  '356'
            516_4  COME_FROM           244  '244'
            516_5  COME_FROM           138  '138'

 L.1465       516  LOAD_FAST                'iprot'
              518  LOAD_METHOD              readFieldEnd
              520  CALL_METHOD_0         0  '0 positional arguments'
              522  POP_TOP          
              524  JUMP_BACK            72  'to 72'
              526  POP_BLOCK        
            528_0  COME_FROM_LOOP       68  '68'

 L.1466       528  LOAD_FAST                'iprot'
              530  LOAD_METHOD              readStructEnd
              532  CALL_METHOD_0         0  '0 positional arguments'
              534  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 502_0

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TIncrement')
        if self.row is not None:
            oprot.writeFieldBegin('row', TType.STRING, 1)
            oprot.writeBinary(self.row)
            oprot.writeFieldEnd()
        if self.columns is not None:
            oprot.writeFieldBegin('columns', TType.LIST, 2)
            oprot.writeListBegin(TType.STRUCT, len(self.columns))
            for iter75 in self.columns:
                iter75.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.attributes is not None:
            oprot.writeFieldBegin('attributes', TType.MAP, 4)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.attributes))
            for kiter76, viter77 in self.attributes.items():
                oprot.writeBinary(kiter76)
                oprot.writeBinary(viter77)

            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        if self.durability is not None:
            oprot.writeFieldBegin('durability', TType.I32, 5)
            oprot.writeI32(self.durability)
            oprot.writeFieldEnd()
        if self.cellVisibility is not None:
            oprot.writeFieldBegin('cellVisibility', TType.STRUCT, 6)
            self.cellVisibility.write(oprot)
            oprot.writeFieldEnd()
        if self.returnResults is not None:
            oprot.writeFieldBegin('returnResults', TType.BOOL, 7)
            oprot.writeBool(self.returnResults)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.row is None:
            raise TProtocolException(message='Required field row is unset!')
        if self.columns is None:
            raise TProtocolException(message='Required field columns is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TAppend(object):
    __doc__ = '\n    Attributes:\n     - row\n     - columns\n     - attributes\n     - durability\n     - cellVisibility\n     - returnResults\n    '

    def __init__(self, row=None, columns=None, attributes=None, durability=None, cellVisibility=None, returnResults=None):
        self.row = row
        self.columns = columns
        self.attributes = attributes
        self.durability = durability
        self.cellVisibility = cellVisibility
        self.returnResults = returnResults

    def read--- This code section failed: ---

 L.1547         0  LOAD_FAST                'iprot'
                2  LOAD_ATTR                _fast_decode
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    60  'to 60'
               10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'iprot'
               14  LOAD_ATTR                trans
               16  LOAD_GLOBAL              TTransport
               18  LOAD_ATTR                CReadableTransport
               20  CALL_FUNCTION_2       2  '2 positional arguments'
               22  POP_JUMP_IF_FALSE    60  'to 60'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                thrift_spec
               28  LOAD_CONST               None
               30  COMPARE_OP               is-not
               32  POP_JUMP_IF_FALSE    60  'to 60'

 L.1548        34  LOAD_FAST                'iprot'
               36  LOAD_METHOD              _fast_decode
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'iprot'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                __class__
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                thrift_spec
               50  BUILD_LIST_2          2 
               52  CALL_METHOD_3         3  '3 positional arguments'
               54  POP_TOP          

 L.1549        56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM            32  '32'
             60_1  COME_FROM            22  '22'
             60_2  COME_FROM             8  '8'

 L.1550        60  LOAD_FAST                'iprot'
               62  LOAD_METHOD              readStructBegin
               64  CALL_METHOD_0         0  '0 positional arguments'
               66  POP_TOP          

 L.1551     68_70  SETUP_LOOP          528  'to 528'

 L.1552        72  LOAD_FAST                'iprot'
               74  LOAD_METHOD              readFieldBegin
               76  CALL_METHOD_0         0  '0 positional arguments'
               78  UNPACK_SEQUENCE_3     3 
               80  STORE_FAST               'fname'
               82  STORE_FAST               'ftype'
               84  STORE_FAST               'fid'

 L.1553        86  LOAD_FAST                'ftype'
               88  LOAD_GLOBAL              TType
               90  LOAD_ATTR                STOP
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L.1554        96  BREAK_LOOP       
             98_0  COME_FROM            94  '94'

 L.1555        98  LOAD_FAST                'fid'
              100  LOAD_CONST               1
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   142  'to 142'

 L.1556       106  LOAD_FAST                'ftype'
              108  LOAD_GLOBAL              TType
              110  LOAD_ATTR                STRING
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   128  'to 128'

 L.1557       116  LOAD_FAST                'iprot'
              118  LOAD_METHOD              readBinary
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  LOAD_FAST                'self'
              124  STORE_ATTR               row
              126  JUMP_FORWARD        516  'to 516'
            128_0  COME_FROM           114  '114'

 L.1559       128  LOAD_FAST                'iprot'
              130  LOAD_METHOD              skip
              132  LOAD_FAST                'ftype'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  POP_TOP          
          138_140  JUMP_FORWARD        516  'to 516'
            142_0  COME_FROM           104  '104'

 L.1560       142  LOAD_FAST                'fid'
              144  LOAD_CONST               2
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   248  'to 248'

 L.1561       150  LOAD_FAST                'ftype'
              152  LOAD_GLOBAL              TType
              154  LOAD_ATTR                LIST
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   234  'to 234'

 L.1562       160  BUILD_LIST_0          0 
              162  LOAD_FAST                'self'
              164  STORE_ATTR               columns

 L.1563       166  LOAD_FAST                'iprot'
              168  LOAD_METHOD              readListBegin
              170  CALL_METHOD_0         0  '0 positional arguments'
              172  UNPACK_SEQUENCE_2     2 
              174  STORE_FAST               '_etype81'
              176  STORE_FAST               '_size78'

 L.1564       178  SETUP_LOOP          224  'to 224'
              180  LOAD_GLOBAL              range
              182  LOAD_FAST                '_size78'
              184  CALL_FUNCTION_1       1  '1 positional argument'
              186  GET_ITER         
              188  FOR_ITER            222  'to 222'
              190  STORE_FAST               '_i82'

 L.1565       192  LOAD_GLOBAL              TColumnValue
              194  CALL_FUNCTION_0       0  '0 positional arguments'
              196  STORE_FAST               '_elem83'

 L.1566       198  LOAD_FAST                '_elem83'
              200  LOAD_METHOD              read
              202  LOAD_FAST                'iprot'
              204  CALL_METHOD_1         1  '1 positional argument'
              206  POP_TOP          

 L.1567       208  LOAD_FAST                'self'
              210  LOAD_ATTR                columns
              212  LOAD_METHOD              append
              214  LOAD_FAST                '_elem83'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  POP_TOP          
              220  JUMP_BACK           188  'to 188'
              222  POP_BLOCK        
            224_0  COME_FROM_LOOP      178  '178'

 L.1568       224  LOAD_FAST                'iprot'
              226  LOAD_METHOD              readListEnd
              228  CALL_METHOD_0         0  '0 positional arguments'
              230  POP_TOP          
              232  JUMP_FORWARD        516  'to 516'
            234_0  COME_FROM           158  '158'

 L.1570       234  LOAD_FAST                'iprot'
              236  LOAD_METHOD              skip
              238  LOAD_FAST                'ftype'
              240  CALL_METHOD_1         1  '1 positional argument'
              242  POP_TOP          
          244_246  JUMP_FORWARD        516  'to 516'
            248_0  COME_FROM           148  '148'

 L.1571       248  LOAD_FAST                'fid'
              250  LOAD_CONST               3
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   358  'to 358'

 L.1572       258  LOAD_FAST                'ftype'
              260  LOAD_GLOBAL              TType
              262  LOAD_ATTR                MAP
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   346  'to 346'

 L.1573       270  BUILD_MAP_0           0 
              272  LOAD_FAST                'self'
              274  STORE_ATTR               attributes

 L.1574       276  LOAD_FAST                'iprot'
              278  LOAD_METHOD              readMapBegin
              280  CALL_METHOD_0         0  '0 positional arguments'
              282  UNPACK_SEQUENCE_3     3 
              284  STORE_FAST               '_ktype85'
              286  STORE_FAST               '_vtype86'
              288  STORE_FAST               '_size84'

 L.1575       290  SETUP_LOOP          336  'to 336'
              292  LOAD_GLOBAL              range
              294  LOAD_FAST                '_size84'
              296  CALL_FUNCTION_1       1  '1 positional argument'
              298  GET_ITER         
              300  FOR_ITER            334  'to 334'
              302  STORE_FAST               '_i88'

 L.1576       304  LOAD_FAST                'iprot'
              306  LOAD_METHOD              readBinary
              308  CALL_METHOD_0         0  '0 positional arguments'
              310  STORE_FAST               '_key89'

 L.1577       312  LOAD_FAST                'iprot'
              314  LOAD_METHOD              readBinary
              316  CALL_METHOD_0         0  '0 positional arguments'
              318  STORE_FAST               '_val90'

 L.1578       320  LOAD_FAST                '_val90'
              322  LOAD_FAST                'self'
              324  LOAD_ATTR                attributes
              326  LOAD_FAST                '_key89'
              328  STORE_SUBSCR     
          330_332  JUMP_BACK           300  'to 300'
              334  POP_BLOCK        
            336_0  COME_FROM_LOOP      290  '290'

 L.1579       336  LOAD_FAST                'iprot'
              338  LOAD_METHOD              readMapEnd
              340  CALL_METHOD_0         0  '0 positional arguments'
              342  POP_TOP          
              344  JUMP_FORWARD        356  'to 356'
            346_0  COME_FROM           266  '266'

 L.1581       346  LOAD_FAST                'iprot'
              348  LOAD_METHOD              skip
              350  LOAD_FAST                'ftype'
              352  CALL_METHOD_1         1  '1 positional argument'
              354  POP_TOP          
            356_0  COME_FROM           344  '344'
              356  JUMP_FORWARD        516  'to 516'
            358_0  COME_FROM           254  '254'

 L.1582       358  LOAD_FAST                'fid'
              360  LOAD_CONST               4
              362  COMPARE_OP               ==
          364_366  POP_JUMP_IF_FALSE   404  'to 404'

 L.1583       368  LOAD_FAST                'ftype'
              370  LOAD_GLOBAL              TType
              372  LOAD_ATTR                I32
              374  COMPARE_OP               ==
          376_378  POP_JUMP_IF_FALSE   392  'to 392'

 L.1584       380  LOAD_FAST                'iprot'
              382  LOAD_METHOD              readI32
              384  CALL_METHOD_0         0  '0 positional arguments'
              386  LOAD_FAST                'self'
              388  STORE_ATTR               durability
              390  JUMP_FORWARD        402  'to 402'
            392_0  COME_FROM           376  '376'

 L.1586       392  LOAD_FAST                'iprot'
              394  LOAD_METHOD              skip
              396  LOAD_FAST                'ftype'
              398  CALL_METHOD_1         1  '1 positional argument'
              400  POP_TOP          
            402_0  COME_FROM           390  '390'
              402  JUMP_FORWARD        516  'to 516'
            404_0  COME_FROM           364  '364'

 L.1587       404  LOAD_FAST                'fid'
              406  LOAD_CONST               5
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   460  'to 460'

 L.1588       414  LOAD_FAST                'ftype'
              416  LOAD_GLOBAL              TType
              418  LOAD_ATTR                STRUCT
              420  COMPARE_OP               ==
          422_424  POP_JUMP_IF_FALSE   448  'to 448'

 L.1589       426  LOAD_GLOBAL              TCellVisibility
              428  CALL_FUNCTION_0       0  '0 positional arguments'
              430  LOAD_FAST                'self'
              432  STORE_ATTR               cellVisibility

 L.1590       434  LOAD_FAST                'self'
              436  LOAD_ATTR                cellVisibility
              438  LOAD_METHOD              read
              440  LOAD_FAST                'iprot'
              442  CALL_METHOD_1         1  '1 positional argument'
              444  POP_TOP          
              446  JUMP_FORWARD        458  'to 458'
            448_0  COME_FROM           422  '422'

 L.1592       448  LOAD_FAST                'iprot'
              450  LOAD_METHOD              skip
              452  LOAD_FAST                'ftype'
              454  CALL_METHOD_1         1  '1 positional argument'
              456  POP_TOP          
            458_0  COME_FROM           446  '446'
              458  JUMP_FORWARD        516  'to 516'
            460_0  COME_FROM           410  '410'

 L.1593       460  LOAD_FAST                'fid'
              462  LOAD_CONST               6
              464  COMPARE_OP               ==
          466_468  POP_JUMP_IF_FALSE   506  'to 506'

 L.1594       470  LOAD_FAST                'ftype'
              472  LOAD_GLOBAL              TType
              474  LOAD_ATTR                BOOL
              476  COMPARE_OP               ==
          478_480  POP_JUMP_IF_FALSE   494  'to 494'

 L.1595       482  LOAD_FAST                'iprot'
              484  LOAD_METHOD              readBool
              486  CALL_METHOD_0         0  '0 positional arguments'
              488  LOAD_FAST                'self'
              490  STORE_ATTR               returnResults
              492  JUMP_FORWARD        504  'to 504'
            494_0  COME_FROM           478  '478'

 L.1597       494  LOAD_FAST                'iprot'
              496  LOAD_METHOD              skip
              498  LOAD_FAST                'ftype'
              500  CALL_METHOD_1         1  '1 positional argument'
            502_0  COME_FROM           232  '232'
            502_1  COME_FROM           126  '126'
              502  POP_TOP          
            504_0  COME_FROM           492  '492'
              504  JUMP_FORWARD        516  'to 516'
            506_0  COME_FROM           466  '466'

 L.1599       506  LOAD_FAST                'iprot'
              508  LOAD_METHOD              skip
              510  LOAD_FAST                'ftype'
              512  CALL_METHOD_1         1  '1 positional argument'
              514  POP_TOP          
            516_0  COME_FROM           504  '504'
            516_1  COME_FROM           458  '458'
            516_2  COME_FROM           402  '402'
            516_3  COME_FROM           356  '356'
            516_4  COME_FROM           244  '244'
            516_5  COME_FROM           138  '138'

 L.1600       516  LOAD_FAST                'iprot'
              518  LOAD_METHOD              readFieldEnd
              520  CALL_METHOD_0         0  '0 positional arguments'
              522  POP_TOP          
              524  JUMP_BACK            72  'to 72'
              526  POP_BLOCK        
            528_0  COME_FROM_LOOP       68  '68'

 L.1601       528  LOAD_FAST                'iprot'
              530  LOAD_METHOD              readStructEnd
              532  CALL_METHOD_0         0  '0 positional arguments'
              534  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 502_0

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TAppend')
        if self.row is not None:
            oprot.writeFieldBegin('row', TType.STRING, 1)
            oprot.writeBinary(self.row)
            oprot.writeFieldEnd()
        if self.columns is not None:
            oprot.writeFieldBegin('columns', TType.LIST, 2)
            oprot.writeListBegin(TType.STRUCT, len(self.columns))
            for iter91 in self.columns:
                iter91.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.attributes is not None:
            oprot.writeFieldBegin('attributes', TType.MAP, 3)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.attributes))
            for kiter92, viter93 in self.attributes.items():
                oprot.writeBinary(kiter92)
                oprot.writeBinary(viter93)

            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        if self.durability is not None:
            oprot.writeFieldBegin('durability', TType.I32, 4)
            oprot.writeI32(self.durability)
            oprot.writeFieldEnd()
        if self.cellVisibility is not None:
            oprot.writeFieldBegin('cellVisibility', TType.STRUCT, 5)
            self.cellVisibility.write(oprot)
            oprot.writeFieldEnd()
        if self.returnResults is not None:
            oprot.writeFieldBegin('returnResults', TType.BOOL, 6)
            oprot.writeBool(self.returnResults)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.row is None:
            raise TProtocolException(message='Required field row is unset!')
        if self.columns is None:
            raise TProtocolException(message='Required field columns is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TScan(object):
    __doc__ = '\n    Any timestamps in the columns are ignored but the colFamTimeRangeMap included, use timeRange to select by timestamp.\n    Max versions defaults to 1.\n\n    Attributes:\n     - startRow\n     - stopRow\n     - columns\n     - caching\n     - maxVersions\n     - timeRange\n     - filterString\n     - batchSize\n     - attributes\n     - authorizations\n     - reversed\n     - cacheBlocks\n     - colFamTimeRangeMap\n     - readType\n     - limit\n     - consistency\n     - targetReplicaId\n     - filterBytes\n    '

    def __init__(self, startRow=None, stopRow=None, columns=None, caching=None, maxVersions=1, timeRange=None, filterString=None, batchSize=None, attributes=None, authorizations=None, reversed=None, cacheBlocks=None, colFamTimeRangeMap=None, readType=None, limit=None, consistency=None, targetReplicaId=None, filterBytes=None):
        self.startRow = startRow
        self.stopRow = stopRow
        self.columns = columns
        self.caching = caching
        self.maxVersions = maxVersions
        self.timeRange = timeRange
        self.filterString = filterString
        self.batchSize = batchSize
        self.attributes = attributes
        self.authorizations = authorizations
        self.reversed = reversed
        self.cacheBlocks = cacheBlocks
        self.colFamTimeRangeMap = colFamTimeRangeMap
        self.readType = readType
        self.limit = limit
        self.consistency = consistency
        self.targetReplicaId = targetReplicaId
        self.filterBytes = filterBytes

    def read--- This code section failed: ---

 L.1709         0  LOAD_FAST                'iprot'
                2  LOAD_ATTR                _fast_decode
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    60  'to 60'
               10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'iprot'
               14  LOAD_ATTR                trans
               16  LOAD_GLOBAL              TTransport
               18  LOAD_ATTR                CReadableTransport
               20  CALL_FUNCTION_2       2  '2 positional arguments'
               22  POP_JUMP_IF_FALSE    60  'to 60'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                thrift_spec
               28  LOAD_CONST               None
               30  COMPARE_OP               is-not
               32  POP_JUMP_IF_FALSE    60  'to 60'

 L.1710        34  LOAD_FAST                'iprot'
               36  LOAD_METHOD              _fast_decode
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'iprot'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                __class__
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                thrift_spec
               50  BUILD_LIST_2          2 
               52  CALL_METHOD_3         3  '3 positional arguments'
               54  POP_TOP          

 L.1711        56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM            32  '32'
             60_1  COME_FROM            22  '22'
             60_2  COME_FROM             8  '8'

 L.1712        60  LOAD_FAST                'iprot'
               62  LOAD_METHOD              readStructBegin
               64  CALL_METHOD_0         0  '0 positional arguments'
               66  POP_TOP          

 L.1713     68_70  SETUP_LOOP         1182  'to 1182'

 L.1714        72  LOAD_FAST                'iprot'
               74  LOAD_METHOD              readFieldBegin
               76  CALL_METHOD_0         0  '0 positional arguments'
               78  UNPACK_SEQUENCE_3     3 
               80  STORE_FAST               'fname'
               82  STORE_FAST               'ftype'
               84  STORE_FAST               'fid'

 L.1715        86  LOAD_FAST                'ftype'
               88  LOAD_GLOBAL              TType
               90  LOAD_ATTR                STOP
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L.1716        96  BREAK_LOOP       
             98_0  COME_FROM            94  '94'

 L.1717        98  LOAD_FAST                'fid'
              100  LOAD_CONST               1
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   142  'to 142'

 L.1718       106  LOAD_FAST                'ftype'
              108  LOAD_GLOBAL              TType
              110  LOAD_ATTR                STRING
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   128  'to 128'

 L.1719       116  LOAD_FAST                'iprot'
              118  LOAD_METHOD              readBinary
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  LOAD_FAST                'self'
              124  STORE_ATTR               startRow
              126  JUMP_FORWARD       1170  'to 1170'
            128_0  COME_FROM           114  '114'

 L.1721       128  LOAD_FAST                'iprot'
              130  LOAD_METHOD              skip
              132  LOAD_FAST                'ftype'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  POP_TOP          
          138_140  JUMP_FORWARD       1170  'to 1170'
            142_0  COME_FROM           104  '104'

 L.1722       142  LOAD_FAST                'fid'
              144  LOAD_CONST               2
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   186  'to 186'

 L.1723       150  LOAD_FAST                'ftype'
              152  LOAD_GLOBAL              TType
              154  LOAD_ATTR                STRING
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   172  'to 172'

 L.1724       160  LOAD_FAST                'iprot'
              162  LOAD_METHOD              readBinary
              164  CALL_METHOD_0         0  '0 positional arguments'
              166  LOAD_FAST                'self'
              168  STORE_ATTR               stopRow
              170  JUMP_FORWARD       1170  'to 1170'
            172_0  COME_FROM           158  '158'

 L.1726       172  LOAD_FAST                'iprot'
              174  LOAD_METHOD              skip
              176  LOAD_FAST                'ftype'
              178  CALL_METHOD_1         1  '1 positional argument'
              180  POP_TOP          
          182_184  JUMP_FORWARD       1170  'to 1170'
            186_0  COME_FROM           148  '148'

 L.1727       186  LOAD_FAST                'fid'
              188  LOAD_CONST               3
              190  COMPARE_OP               ==
          192_194  POP_JUMP_IF_FALSE   296  'to 296'

 L.1728       196  LOAD_FAST                'ftype'
              198  LOAD_GLOBAL              TType
              200  LOAD_ATTR                LIST
              202  COMPARE_OP               ==
          204_206  POP_JUMP_IF_FALSE   282  'to 282'

 L.1729       208  BUILD_LIST_0          0 
              210  LOAD_FAST                'self'
              212  STORE_ATTR               columns

 L.1730       214  LOAD_FAST                'iprot'
              216  LOAD_METHOD              readListBegin
              218  CALL_METHOD_0         0  '0 positional arguments'
              220  UNPACK_SEQUENCE_2     2 
              222  STORE_FAST               '_etype97'
              224  STORE_FAST               '_size94'

 L.1731       226  SETUP_LOOP          272  'to 272'
              228  LOAD_GLOBAL              range
              230  LOAD_FAST                '_size94'
              232  CALL_FUNCTION_1       1  '1 positional argument'
              234  GET_ITER         
              236  FOR_ITER            270  'to 270'
              238  STORE_FAST               '_i98'

 L.1732       240  LOAD_GLOBAL              TColumn
              242  CALL_FUNCTION_0       0  '0 positional arguments'
              244  STORE_FAST               '_elem99'

 L.1733       246  LOAD_FAST                '_elem99'
              248  LOAD_METHOD              read
              250  LOAD_FAST                'iprot'
              252  CALL_METHOD_1         1  '1 positional argument'
              254  POP_TOP          

 L.1734       256  LOAD_FAST                'self'
              258  LOAD_ATTR                columns
              260  LOAD_METHOD              append
              262  LOAD_FAST                '_elem99'
              264  CALL_METHOD_1         1  '1 positional argument'
              266  POP_TOP          
              268  JUMP_BACK           236  'to 236'
              270  POP_BLOCK        
            272_0  COME_FROM_LOOP      226  '226'

 L.1735       272  LOAD_FAST                'iprot'
              274  LOAD_METHOD              readListEnd
              276  CALL_METHOD_0         0  '0 positional arguments'
              278  POP_TOP          
              280  JUMP_FORWARD       1170  'to 1170'
            282_0  COME_FROM           204  '204'

 L.1737       282  LOAD_FAST                'iprot'
              284  LOAD_METHOD              skip
              286  LOAD_FAST                'ftype'
              288  CALL_METHOD_1         1  '1 positional argument'
              290  POP_TOP          
          292_294  JUMP_FORWARD       1170  'to 1170'
            296_0  COME_FROM           192  '192'

 L.1738       296  LOAD_FAST                'fid'
              298  LOAD_CONST               4
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_FALSE   344  'to 344'

 L.1739       306  LOAD_FAST                'ftype'
              308  LOAD_GLOBAL              TType
              310  LOAD_ATTR                I32
              312  COMPARE_OP               ==
          314_316  POP_JUMP_IF_FALSE   330  'to 330'

 L.1740       318  LOAD_FAST                'iprot'
              320  LOAD_METHOD              readI32
              322  CALL_METHOD_0         0  '0 positional arguments'
              324  LOAD_FAST                'self'
              326  STORE_ATTR               caching
              328  JUMP_FORWARD       1170  'to 1170'
            330_0  COME_FROM           314  '314'

 L.1742       330  LOAD_FAST                'iprot'
              332  LOAD_METHOD              skip
              334  LOAD_FAST                'ftype'
              336  CALL_METHOD_1         1  '1 positional argument'
              338  POP_TOP          
          340_342  JUMP_FORWARD       1170  'to 1170'
            344_0  COME_FROM           302  '302'

 L.1743       344  LOAD_FAST                'fid'
              346  LOAD_CONST               5
              348  COMPARE_OP               ==
          350_352  POP_JUMP_IF_FALSE   392  'to 392'

 L.1744       354  LOAD_FAST                'ftype'
              356  LOAD_GLOBAL              TType
              358  LOAD_ATTR                I32
              360  COMPARE_OP               ==
          362_364  POP_JUMP_IF_FALSE   378  'to 378'

 L.1745       366  LOAD_FAST                'iprot'
              368  LOAD_METHOD              readI32
              370  CALL_METHOD_0         0  '0 positional arguments'
              372  LOAD_FAST                'self'
              374  STORE_ATTR               maxVersions
              376  JUMP_FORWARD       1170  'to 1170'
            378_0  COME_FROM           362  '362'

 L.1747       378  LOAD_FAST                'iprot'
              380  LOAD_METHOD              skip
              382  LOAD_FAST                'ftype'
              384  CALL_METHOD_1         1  '1 positional argument'
              386  POP_TOP          
          388_390  JUMP_FORWARD       1170  'to 1170'
            392_0  COME_FROM           350  '350'

 L.1748       392  LOAD_FAST                'fid'
              394  LOAD_CONST               6
              396  COMPARE_OP               ==
          398_400  POP_JUMP_IF_FALSE   450  'to 450'

 L.1749       402  LOAD_FAST                'ftype'
              404  LOAD_GLOBAL              TType
              406  LOAD_ATTR                STRUCT
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   436  'to 436'

 L.1750       414  LOAD_GLOBAL              TTimeRange
              416  CALL_FUNCTION_0       0  '0 positional arguments'
              418  LOAD_FAST                'self'
              420  STORE_ATTR               timeRange

 L.1751       422  LOAD_FAST                'self'
              424  LOAD_ATTR                timeRange
              426  LOAD_METHOD              read
              428  LOAD_FAST                'iprot'
              430  CALL_METHOD_1         1  '1 positional argument'
              432  POP_TOP          
              434  JUMP_FORWARD       1170  'to 1170'
            436_0  COME_FROM           410  '410'

 L.1753       436  LOAD_FAST                'iprot'
              438  LOAD_METHOD              skip
              440  LOAD_FAST                'ftype'
              442  CALL_METHOD_1         1  '1 positional argument'
              444  POP_TOP          
          446_448  JUMP_FORWARD       1170  'to 1170'
            450_0  COME_FROM           398  '398'

 L.1754       450  LOAD_FAST                'fid'
              452  LOAD_CONST               7
              454  COMPARE_OP               ==
          456_458  POP_JUMP_IF_FALSE   498  'to 498'

 L.1755       460  LOAD_FAST                'ftype'
              462  LOAD_GLOBAL              TType
              464  LOAD_ATTR                STRING
              466  COMPARE_OP               ==
          468_470  POP_JUMP_IF_FALSE   484  'to 484'

 L.1756       472  LOAD_FAST                'iprot'
              474  LOAD_METHOD              readBinary
              476  CALL_METHOD_0         0  '0 positional arguments'
              478  LOAD_FAST                'self'
              480  STORE_ATTR               filterString
              482  JUMP_FORWARD       1170  'to 1170'
            484_0  COME_FROM           468  '468'

 L.1758       484  LOAD_FAST                'iprot'
              486  LOAD_METHOD              skip
              488  LOAD_FAST                'ftype'
              490  CALL_METHOD_1         1  '1 positional argument'
              492  POP_TOP          
          494_496  JUMP_FORWARD       1170  'to 1170'
            498_0  COME_FROM           456  '456'

 L.1759       498  LOAD_FAST                'fid'
              500  LOAD_CONST               8
              502  COMPARE_OP               ==
          504_506  POP_JUMP_IF_FALSE   546  'to 546'

 L.1760       508  LOAD_FAST                'ftype'
              510  LOAD_GLOBAL              TType
              512  LOAD_ATTR                I32
              514  COMPARE_OP               ==
          516_518  POP_JUMP_IF_FALSE   532  'to 532'

 L.1761       520  LOAD_FAST                'iprot'
              522  LOAD_METHOD              readI32
              524  CALL_METHOD_0         0  '0 positional arguments'
              526  LOAD_FAST                'self'
              528  STORE_ATTR               batchSize
              530  JUMP_FORWARD       1170  'to 1170'
            532_0  COME_FROM           516  '516'

 L.1763       532  LOAD_FAST                'iprot'
              534  LOAD_METHOD              skip
              536  LOAD_FAST                'ftype'
              538  CALL_METHOD_1         1  '1 positional argument'
              540  POP_TOP          
          542_544  JUMP_FORWARD       1170  'to 1170'
            546_0  COME_FROM           504  '504'

 L.1764       546  LOAD_FAST                'fid'
              548  LOAD_CONST               9
              550  COMPARE_OP               ==
          552_554  POP_JUMP_IF_FALSE   658  'to 658'

 L.1765       556  LOAD_FAST                'ftype'
              558  LOAD_GLOBAL              TType
              560  LOAD_ATTR                MAP
              562  COMPARE_OP               ==
          564_566  POP_JUMP_IF_FALSE   644  'to 644'

 L.1766       568  BUILD_MAP_0           0 
              570  LOAD_FAST                'self'
              572  STORE_ATTR               attributes

 L.1767       574  LOAD_FAST                'iprot'
              576  LOAD_METHOD              readMapBegin
              578  CALL_METHOD_0         0  '0 positional arguments'
              580  UNPACK_SEQUENCE_3     3 
              582  STORE_FAST               '_ktype101'
              584  STORE_FAST               '_vtype102'
              586  STORE_FAST               '_size100'

 L.1768       588  SETUP_LOOP          634  'to 634'
              590  LOAD_GLOBAL              range
              592  LOAD_FAST                '_size100'
              594  CALL_FUNCTION_1       1  '1 positional argument'
              596  GET_ITER         
              598  FOR_ITER            632  'to 632'
              600  STORE_FAST               '_i104'

 L.1769       602  LOAD_FAST                'iprot'
              604  LOAD_METHOD              readBinary
              606  CALL_METHOD_0         0  '0 positional arguments'
              608  STORE_FAST               '_key105'

 L.1770       610  LOAD_FAST                'iprot'
              612  LOAD_METHOD              readBinary
              614  CALL_METHOD_0         0  '0 positional arguments'
              616  STORE_FAST               '_val106'

 L.1771       618  LOAD_FAST                '_val106'
              620  LOAD_FAST                'self'
              622  LOAD_ATTR                attributes
              624  LOAD_FAST                '_key105'
              626  STORE_SUBSCR     
          628_630  JUMP_BACK           598  'to 598'
              632  POP_BLOCK        
            634_0  COME_FROM_LOOP      588  '588'

 L.1772       634  LOAD_FAST                'iprot'
              636  LOAD_METHOD              readMapEnd
              638  CALL_METHOD_0         0  '0 positional arguments'
              640  POP_TOP          
              642  JUMP_FORWARD       1170  'to 1170'
            644_0  COME_FROM           564  '564'

 L.1774       644  LOAD_FAST                'iprot'
              646  LOAD_METHOD              skip
              648  LOAD_FAST                'ftype'
              650  CALL_METHOD_1         1  '1 positional argument'
              652  POP_TOP          
          654_656  JUMP_FORWARD       1170  'to 1170'
            658_0  COME_FROM           552  '552'

 L.1775       658  LOAD_FAST                'fid'
              660  LOAD_CONST               10
              662  COMPARE_OP               ==
          664_666  POP_JUMP_IF_FALSE   716  'to 716'

 L.1776       668  LOAD_FAST                'ftype'
              670  LOAD_GLOBAL              TType
              672  LOAD_ATTR                STRUCT
              674  COMPARE_OP               ==
          676_678  POP_JUMP_IF_FALSE   702  'to 702'

 L.1777       680  LOAD_GLOBAL              TAuthorization
              682  CALL_FUNCTION_0       0  '0 positional arguments'
              684  LOAD_FAST                'self'
              686  STORE_ATTR               authorizations

 L.1778       688  LOAD_FAST                'self'
              690  LOAD_ATTR                authorizations
              692  LOAD_METHOD              read
              694  LOAD_FAST                'iprot'
              696  CALL_METHOD_1         1  '1 positional argument'
              698  POP_TOP          
              700  JUMP_FORWARD       1170  'to 1170'
            702_0  COME_FROM           676  '676'

 L.1780       702  LOAD_FAST                'iprot'
              704  LOAD_METHOD              skip
              706  LOAD_FAST                'ftype'
              708  CALL_METHOD_1         1  '1 positional argument'
              710  POP_TOP          
          712_714  JUMP_FORWARD       1170  'to 1170'
            716_0  COME_FROM           664  '664'

 L.1781       716  LOAD_FAST                'fid'
              718  LOAD_CONST               11
              720  COMPARE_OP               ==
          722_724  POP_JUMP_IF_FALSE   764  'to 764'

 L.1782       726  LOAD_FAST                'ftype'
              728  LOAD_GLOBAL              TType
              730  LOAD_ATTR                BOOL
              732  COMPARE_OP               ==
          734_736  POP_JUMP_IF_FALSE   750  'to 750'

 L.1783       738  LOAD_FAST                'iprot'
              740  LOAD_METHOD              readBool
              742  CALL_METHOD_0         0  '0 positional arguments'
              744  LOAD_FAST                'self'
              746  STORE_ATTR               reversed
              748  JUMP_FORWARD       1170  'to 1170'
            750_0  COME_FROM           734  '734'

 L.1785       750  LOAD_FAST                'iprot'
              752  LOAD_METHOD              skip
              754  LOAD_FAST                'ftype'
              756  CALL_METHOD_1         1  '1 positional argument'
              758  POP_TOP          
          760_762  JUMP_FORWARD       1170  'to 1170'
            764_0  COME_FROM           722  '722'

 L.1786       764  LOAD_FAST                'fid'
              766  LOAD_CONST               12
              768  COMPARE_OP               ==
          770_772  POP_JUMP_IF_FALSE   812  'to 812'

 L.1787       774  LOAD_FAST                'ftype'
              776  LOAD_GLOBAL              TType
              778  LOAD_ATTR                BOOL
              780  COMPARE_OP               ==
          782_784  POP_JUMP_IF_FALSE   798  'to 798'

 L.1788       786  LOAD_FAST                'iprot'
              788  LOAD_METHOD              readBool
              790  CALL_METHOD_0         0  '0 positional arguments'
              792  LOAD_FAST                'self'
              794  STORE_ATTR               cacheBlocks
              796  JUMP_FORWARD       1170  'to 1170'
            798_0  COME_FROM           782  '782'

 L.1790       798  LOAD_FAST                'iprot'
              800  LOAD_METHOD              skip
              802  LOAD_FAST                'ftype'
              804  CALL_METHOD_1         1  '1 positional argument'
              806  POP_TOP          
          808_810  JUMP_FORWARD       1170  'to 1170'
            812_0  COME_FROM           770  '770'

 L.1791       812  LOAD_FAST                'fid'
              814  LOAD_CONST               13
              816  COMPARE_OP               ==
          818_820  POP_JUMP_IF_FALSE   930  'to 930'

 L.1792       822  LOAD_FAST                'ftype'
              824  LOAD_GLOBAL              TType
              826  LOAD_ATTR                MAP
              828  COMPARE_OP               ==
          830_832  POP_JUMP_IF_FALSE   918  'to 918'

 L.1793       834  BUILD_MAP_0           0 
              836  LOAD_FAST                'self'
              838  STORE_ATTR               colFamTimeRangeMap

 L.1794       840  LOAD_FAST                'iprot'
              842  LOAD_METHOD              readMapBegin
              844  CALL_METHOD_0         0  '0 positional arguments'
              846  UNPACK_SEQUENCE_3     3 
              848  STORE_FAST               '_ktype108'
              850  STORE_FAST               '_vtype109'
              852  STORE_FAST               '_size107'

 L.1795       854  SETUP_LOOP          908  'to 908'
              856  LOAD_GLOBAL              range
              858  LOAD_FAST                '_size107'
              860  CALL_FUNCTION_1       1  '1 positional argument'
              862  GET_ITER         
              864  FOR_ITER            906  'to 906'
              866  STORE_FAST               '_i111'

 L.1796       868  LOAD_FAST                'iprot'
              870  LOAD_METHOD              readBinary
              872  CALL_METHOD_0         0  '0 positional arguments'
              874  STORE_FAST               '_key112'

 L.1797       876  LOAD_GLOBAL              TTimeRange
              878  CALL_FUNCTION_0       0  '0 positional arguments'
              880  STORE_FAST               '_val113'

 L.1798       882  LOAD_FAST                '_val113'
              884  LOAD_METHOD              read
              886  LOAD_FAST                'iprot'
              888  CALL_METHOD_1         1  '1 positional argument'
              890  POP_TOP          

 L.1799       892  LOAD_FAST                '_val113'
              894  LOAD_FAST                'self'
              896  LOAD_ATTR                colFamTimeRangeMap
              898  LOAD_FAST                '_key112'
              900  STORE_SUBSCR     
          902_904  JUMP_BACK           864  'to 864'
              906  POP_BLOCK        
            908_0  COME_FROM_LOOP      854  '854'

 L.1800       908  LOAD_FAST                'iprot'
              910  LOAD_METHOD              readMapEnd
              912  CALL_METHOD_0         0  '0 positional arguments'
              914  POP_TOP          
              916  JUMP_FORWARD        928  'to 928'
            918_0  COME_FROM           830  '830'

 L.1802       918  LOAD_FAST                'iprot'
              920  LOAD_METHOD              skip
              922  LOAD_FAST                'ftype'
              924  CALL_METHOD_1         1  '1 positional argument'
              926  POP_TOP          
            928_0  COME_FROM           916  '916'
              928  JUMP_FORWARD       1170  'to 1170'
            930_0  COME_FROM           818  '818'

 L.1803       930  LOAD_FAST                'fid'
              932  LOAD_CONST               14
              934  COMPARE_OP               ==
          936_938  POP_JUMP_IF_FALSE   976  'to 976'

 L.1804       940  LOAD_FAST                'ftype'
              942  LOAD_GLOBAL              TType
              944  LOAD_ATTR                I32
              946  COMPARE_OP               ==
          948_950  POP_JUMP_IF_FALSE   964  'to 964'

 L.1805       952  LOAD_FAST                'iprot'
              954  LOAD_METHOD              readI32
              956  CALL_METHOD_0         0  '0 positional arguments'
              958  LOAD_FAST                'self'
              960  STORE_ATTR               readType
              962  JUMP_FORWARD        974  'to 974'
            964_0  COME_FROM           948  '948'

 L.1807       964  LOAD_FAST                'iprot'
              966  LOAD_METHOD              skip
              968  LOAD_FAST                'ftype'
              970  CALL_METHOD_1         1  '1 positional argument'
              972  POP_TOP          
            974_0  COME_FROM           962  '962'
              974  JUMP_FORWARD       1170  'to 1170'
            976_0  COME_FROM           936  '936'

 L.1808       976  LOAD_FAST                'fid'
              978  LOAD_CONST               15
              980  COMPARE_OP               ==
          982_984  POP_JUMP_IF_FALSE  1022  'to 1022'

 L.1809       986  LOAD_FAST                'ftype'
              988  LOAD_GLOBAL              TType
              990  LOAD_ATTR                I32
              992  COMPARE_OP               ==
          994_996  POP_JUMP_IF_FALSE  1010  'to 1010'

 L.1810       998  LOAD_FAST                'iprot'
             1000  LOAD_METHOD              readI32
             1002  CALL_METHOD_0         0  '0 positional arguments'
             1004  LOAD_FAST                'self'
             1006  STORE_ATTR               limit
             1008  JUMP_FORWARD       1020  'to 1020'
           1010_0  COME_FROM           994  '994'

 L.1812      1010  LOAD_FAST                'iprot'
             1012  LOAD_METHOD              skip
             1014  LOAD_FAST                'ftype'
             1016  CALL_METHOD_1         1  '1 positional argument'
             1018  POP_TOP          
           1020_0  COME_FROM          1008  '1008'
             1020  JUMP_FORWARD       1170  'to 1170'
           1022_0  COME_FROM           982  '982'

 L.1813      1022  LOAD_FAST                'fid'
             1024  LOAD_CONST               16
             1026  COMPARE_OP               ==
         1028_1030  POP_JUMP_IF_FALSE  1068  'to 1068'

 L.1814      1032  LOAD_FAST                'ftype'
             1034  LOAD_GLOBAL              TType
             1036  LOAD_ATTR                I32
             1038  COMPARE_OP               ==
         1040_1042  POP_JUMP_IF_FALSE  1056  'to 1056'

 L.1815      1044  LOAD_FAST                'iprot'
             1046  LOAD_METHOD              readI32
             1048  CALL_METHOD_0         0  '0 positional arguments'
             1050  LOAD_FAST                'self'
             1052  STORE_ATTR               consistency
             1054  JUMP_FORWARD       1066  'to 1066'
           1056_0  COME_FROM          1040  '1040'

 L.1817      1056  LOAD_FAST                'iprot'
             1058  LOAD_METHOD              skip
             1060  LOAD_FAST                'ftype'
             1062  CALL_METHOD_1         1  '1 positional argument'
             1064  POP_TOP          
           1066_0  COME_FROM          1054  '1054'
             1066  JUMP_FORWARD       1170  'to 1170'
           1068_0  COME_FROM          1028  '1028'

 L.1818      1068  LOAD_FAST                'fid'
             1070  LOAD_CONST               17
             1072  COMPARE_OP               ==
         1074_1076  POP_JUMP_IF_FALSE  1114  'to 1114'

 L.1819      1078  LOAD_FAST                'ftype'
             1080  LOAD_GLOBAL              TType
             1082  LOAD_ATTR                I32
             1084  COMPARE_OP               ==
         1086_1088  POP_JUMP_IF_FALSE  1102  'to 1102'

 L.1820      1090  LOAD_FAST                'iprot'
             1092  LOAD_METHOD              readI32
             1094  CALL_METHOD_0         0  '0 positional arguments'
             1096  LOAD_FAST                'self'
             1098  STORE_ATTR               targetReplicaId
             1100  JUMP_FORWARD       1112  'to 1112'
           1102_0  COME_FROM          1086  '1086'

 L.1822      1102  LOAD_FAST                'iprot'
             1104  LOAD_METHOD              skip
             1106  LOAD_FAST                'ftype'
             1108  CALL_METHOD_1         1  '1 positional argument'
             1110  POP_TOP          
           1112_0  COME_FROM          1100  '1100'
             1112  JUMP_FORWARD       1170  'to 1170'
           1114_0  COME_FROM          1074  '1074'

 L.1823      1114  LOAD_FAST                'fid'
             1116  LOAD_CONST               18
             1118  COMPARE_OP               ==
         1120_1122  POP_JUMP_IF_FALSE  1160  'to 1160'

 L.1824      1124  LOAD_FAST                'ftype'
             1126  LOAD_GLOBAL              TType
             1128  LOAD_ATTR                STRING
             1130  COMPARE_OP               ==
         1132_1134  POP_JUMP_IF_FALSE  1148  'to 1148'

 L.1825      1136  LOAD_FAST                'iprot'
             1138  LOAD_METHOD              readBinary
             1140  CALL_METHOD_0         0  '0 positional arguments'
             1142  LOAD_FAST                'self'
             1144  STORE_ATTR               filterBytes
             1146  JUMP_FORWARD       1158  'to 1158'
           1148_0  COME_FROM          1132  '1132'

 L.1827      1148  LOAD_FAST                'iprot'
             1150  LOAD_METHOD              skip
             1152  LOAD_FAST                'ftype'
             1154  CALL_METHOD_1         1  '1 positional argument'
           1156_0  COME_FROM           796  '796'
           1156_1  COME_FROM           748  '748'
           1156_2  COME_FROM           700  '700'
           1156_3  COME_FROM           642  '642'
           1156_4  COME_FROM           530  '530'
           1156_5  COME_FROM           482  '482'
           1156_6  COME_FROM           434  '434'
           1156_7  COME_FROM           376  '376'
           1156_8  COME_FROM           328  '328'
           1156_9  COME_FROM           280  '280'
          1156_10  COME_FROM           170  '170'
          1156_11  COME_FROM           126  '126'
             1156  POP_TOP          
           1158_0  COME_FROM          1146  '1146'
             1158  JUMP_FORWARD       1170  'to 1170'
           1160_0  COME_FROM          1120  '1120'

 L.1829      1160  LOAD_FAST                'iprot'
             1162  LOAD_METHOD              skip
             1164  LOAD_FAST                'ftype'
             1166  CALL_METHOD_1         1  '1 positional argument'
             1168  POP_TOP          
           1170_0  COME_FROM          1158  '1158'
           1170_1  COME_FROM          1112  '1112'
           1170_2  COME_FROM          1066  '1066'
           1170_3  COME_FROM          1020  '1020'
           1170_4  COME_FROM           974  '974'
           1170_5  COME_FROM           928  '928'
           1170_6  COME_FROM           808  '808'
           1170_7  COME_FROM           760  '760'
           1170_8  COME_FROM           712  '712'
           1170_9  COME_FROM           654  '654'
          1170_10  COME_FROM           542  '542'
          1170_11  COME_FROM           494  '494'
          1170_12  COME_FROM           446  '446'
          1170_13  COME_FROM           388  '388'
          1170_14  COME_FROM           340  '340'
          1170_15  COME_FROM           292  '292'
          1170_16  COME_FROM           182  '182'
          1170_17  COME_FROM           138  '138'

 L.1830      1170  LOAD_FAST                'iprot'
             1172  LOAD_METHOD              readFieldEnd
             1174  CALL_METHOD_0         0  '0 positional arguments'
             1176  POP_TOP          
             1178  JUMP_BACK            72  'to 72'
             1180  POP_BLOCK        
           1182_0  COME_FROM_LOOP       68  '68'

 L.1831      1182  LOAD_FAST                'iprot'
             1184  LOAD_METHOD              readStructEnd
             1186  CALL_METHOD_0         0  '0 positional arguments'
             1188  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 1156_0

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TScan')
        if self.startRow is not None:
            oprot.writeFieldBegin('startRow', TType.STRING, 1)
            oprot.writeBinary(self.startRow)
            oprot.writeFieldEnd()
        if self.stopRow is not None:
            oprot.writeFieldBegin('stopRow', TType.STRING, 2)
            oprot.writeBinary(self.stopRow)
            oprot.writeFieldEnd()
        if self.columns is not None:
            oprot.writeFieldBegin('columns', TType.LIST, 3)
            oprot.writeListBegin(TType.STRUCT, len(self.columns))
            for iter114 in self.columns:
                iter114.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.caching is not None:
            oprot.writeFieldBegin('caching', TType.I32, 4)
            oprot.writeI32(self.caching)
            oprot.writeFieldEnd()
        if self.maxVersions is not None:
            oprot.writeFieldBegin('maxVersions', TType.I32, 5)
            oprot.writeI32(self.maxVersions)
            oprot.writeFieldEnd()
        if self.timeRange is not None:
            oprot.writeFieldBegin('timeRange', TType.STRUCT, 6)
            self.timeRange.write(oprot)
            oprot.writeFieldEnd()
        if self.filterString is not None:
            oprot.writeFieldBegin('filterString', TType.STRING, 7)
            oprot.writeBinary(self.filterString)
            oprot.writeFieldEnd()
        if self.batchSize is not None:
            oprot.writeFieldBegin('batchSize', TType.I32, 8)
            oprot.writeI32(self.batchSize)
            oprot.writeFieldEnd()
        if self.attributes is not None:
            oprot.writeFieldBegin('attributes', TType.MAP, 9)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.attributes))
            for kiter115, viter116 in self.attributes.items():
                oprot.writeBinary(kiter115)
                oprot.writeBinary(viter116)

            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        if self.authorizations is not None:
            oprot.writeFieldBegin('authorizations', TType.STRUCT, 10)
            self.authorizations.write(oprot)
            oprot.writeFieldEnd()
        if self.reversed is not None:
            oprot.writeFieldBegin('reversed', TType.BOOL, 11)
            oprot.writeBool(self.reversed)
            oprot.writeFieldEnd()
        if self.cacheBlocks is not None:
            oprot.writeFieldBegin('cacheBlocks', TType.BOOL, 12)
            oprot.writeBool(self.cacheBlocks)
            oprot.writeFieldEnd()
        if self.colFamTimeRangeMap is not None:
            oprot.writeFieldBegin('colFamTimeRangeMap', TType.MAP, 13)
            oprot.writeMapBegin(TType.STRING, TType.STRUCT, len(self.colFamTimeRangeMap))
            for kiter117, viter118 in self.colFamTimeRangeMap.items():
                oprot.writeBinary(kiter117)
                viter118.write(oprot)

            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        if self.readType is not None:
            oprot.writeFieldBegin('readType', TType.I32, 14)
            oprot.writeI32(self.readType)
            oprot.writeFieldEnd()
        if self.limit is not None:
            oprot.writeFieldBegin('limit', TType.I32, 15)
            oprot.writeI32(self.limit)
            oprot.writeFieldEnd()
        if self.consistency is not None:
            oprot.writeFieldBegin('consistency', TType.I32, 16)
            oprot.writeI32(self.consistency)
            oprot.writeFieldEnd()
        if self.targetReplicaId is not None:
            oprot.writeFieldBegin('targetReplicaId', TType.I32, 17)
            oprot.writeI32(self.targetReplicaId)
            oprot.writeFieldEnd()
        if self.filterBytes is not None:
            oprot.writeFieldBegin('filterBytes', TType.STRING, 18)
            oprot.writeBinary(self.filterBytes)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TMutation(object):
    __doc__ = '\n    Atomic mutation for the specified row. It can be either Put or Delete.\n\n    Attributes:\n     - put\n     - deleteSingle\n    '

    def __init__(self, put=None, deleteSingle=None):
        self.put = put
        self.deleteSingle = deleteSingle

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.put = TPut()
                    self.put.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.deleteSingle = TDelete()
                    self.deleteSingle.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TMutation')
        if self.put is not None:
            oprot.writeFieldBegin('put', TType.STRUCT, 1)
            self.put.write(oprot)
            oprot.writeFieldEnd()
        if self.deleteSingle is not None:
            oprot.writeFieldBegin('deleteSingle', TType.STRUCT, 2)
            self.deleteSingle.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TRowMutations(object):
    __doc__ = '\n    A TRowMutations object is used to apply a number of Mutations to a single row.\n\n    Attributes:\n     - row\n     - mutations\n    '

    def __init__(self, row=None, mutations=None):
        self.row = row
        self.mutations = mutations

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.row = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.LIST:
                    self.mutations = []
                    _etype122, _size119 = iprot.readListBegin()
                    for _i123 in range(_size119):
                        _elem124 = TMutation()
                        _elem124.read(iprot)
                        self.mutations.append(_elem124)

                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TRowMutations')
        if self.row is not None:
            oprot.writeFieldBegin('row', TType.STRING, 1)
            oprot.writeBinary(self.row)
            oprot.writeFieldEnd()
        if self.mutations is not None:
            oprot.writeFieldBegin('mutations', TType.LIST, 2)
            oprot.writeListBegin(TType.STRUCT, len(self.mutations))
            for iter125 in self.mutations:
                iter125.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.row is None:
            raise TProtocolException(message='Required field row is unset!')
        if self.mutations is None:
            raise TProtocolException(message='Required field mutations is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class THRegionInfo(object):
    __doc__ = '\n    Attributes:\n     - regionId\n     - tableName\n     - startKey\n     - endKey\n     - offline\n     - split\n     - replicaId\n    '

    def __init__(self, regionId=None, tableName=None, startKey=None, endKey=None, offline=None, split=None, replicaId=None):
        self.regionId = regionId
        self.tableName = tableName
        self.startKey = startKey
        self.endKey = endKey
        self.offline = offline
        self.split = split
        self.replicaId = replicaId

    def read--- This code section failed: ---

 L.2115         0  LOAD_FAST                'iprot'
                2  LOAD_ATTR                _fast_decode
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    60  'to 60'
               10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'iprot'
               14  LOAD_ATTR                trans
               16  LOAD_GLOBAL              TTransport
               18  LOAD_ATTR                CReadableTransport
               20  CALL_FUNCTION_2       2  '2 positional arguments'
               22  POP_JUMP_IF_FALSE    60  'to 60'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                thrift_spec
               28  LOAD_CONST               None
               30  COMPARE_OP               is-not
               32  POP_JUMP_IF_FALSE    60  'to 60'

 L.2116        34  LOAD_FAST                'iprot'
               36  LOAD_METHOD              _fast_decode
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'iprot'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                __class__
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                thrift_spec
               50  BUILD_LIST_2          2 
               52  CALL_METHOD_3         3  '3 positional arguments'
               54  POP_TOP          

 L.2117        56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM            32  '32'
             60_1  COME_FROM            22  '22'
             60_2  COME_FROM             8  '8'

 L.2118        60  LOAD_FAST                'iprot'
               62  LOAD_METHOD              readStructBegin
               64  CALL_METHOD_0         0  '0 positional arguments'
               66  POP_TOP          

 L.2119     68_70  SETUP_LOOP          432  'to 432'

 L.2120        72  LOAD_FAST                'iprot'
               74  LOAD_METHOD              readFieldBegin
               76  CALL_METHOD_0         0  '0 positional arguments'
               78  UNPACK_SEQUENCE_3     3 
               80  STORE_FAST               'fname'
               82  STORE_FAST               'ftype'
               84  STORE_FAST               'fid'

 L.2121        86  LOAD_FAST                'ftype'
               88  LOAD_GLOBAL              TType
               90  LOAD_ATTR                STOP
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L.2122        96  BREAK_LOOP       
             98_0  COME_FROM            94  '94'

 L.2123        98  LOAD_FAST                'fid'
              100  LOAD_CONST               1
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   142  'to 142'

 L.2124       106  LOAD_FAST                'ftype'
              108  LOAD_GLOBAL              TType
              110  LOAD_ATTR                I64
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   128  'to 128'

 L.2125       116  LOAD_FAST                'iprot'
              118  LOAD_METHOD              readI64
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  LOAD_FAST                'self'
              124  STORE_ATTR               regionId
              126  JUMP_FORWARD        420  'to 420'
            128_0  COME_FROM           114  '114'

 L.2127       128  LOAD_FAST                'iprot'
              130  LOAD_METHOD              skip
              132  LOAD_FAST                'ftype'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  POP_TOP          
          138_140  JUMP_FORWARD        420  'to 420'
            142_0  COME_FROM           104  '104'

 L.2128       142  LOAD_FAST                'fid'
              144  LOAD_CONST               2
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   184  'to 184'

 L.2129       150  LOAD_FAST                'ftype'
              152  LOAD_GLOBAL              TType
              154  LOAD_ATTR                STRING
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   172  'to 172'

 L.2130       160  LOAD_FAST                'iprot'
              162  LOAD_METHOD              readBinary
              164  CALL_METHOD_0         0  '0 positional arguments'
              166  LOAD_FAST                'self'
              168  STORE_ATTR               tableName
              170  JUMP_FORWARD        182  'to 182'
            172_0  COME_FROM           158  '158'

 L.2132       172  LOAD_FAST                'iprot'
              174  LOAD_METHOD              skip
              176  LOAD_FAST                'ftype'
              178  CALL_METHOD_1         1  '1 positional argument'
              180  POP_TOP          
            182_0  COME_FROM           170  '170'
              182  JUMP_FORWARD        420  'to 420'
            184_0  COME_FROM           148  '148'

 L.2133       184  LOAD_FAST                'fid'
              186  LOAD_CONST               3
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   226  'to 226'

 L.2134       192  LOAD_FAST                'ftype'
              194  LOAD_GLOBAL              TType
              196  LOAD_ATTR                STRING
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   214  'to 214'

 L.2135       202  LOAD_FAST                'iprot'
              204  LOAD_METHOD              readBinary
              206  CALL_METHOD_0         0  '0 positional arguments'
              208  LOAD_FAST                'self'
              210  STORE_ATTR               startKey
              212  JUMP_FORWARD        224  'to 224'
            214_0  COME_FROM           200  '200'

 L.2137       214  LOAD_FAST                'iprot'
              216  LOAD_METHOD              skip
              218  LOAD_FAST                'ftype'
              220  CALL_METHOD_1         1  '1 positional argument'
              222  POP_TOP          
            224_0  COME_FROM           212  '212'
              224  JUMP_FORWARD        420  'to 420'
            226_0  COME_FROM           190  '190'

 L.2138       226  LOAD_FAST                'fid'
              228  LOAD_CONST               4
              230  COMPARE_OP               ==
          232_234  POP_JUMP_IF_FALSE   272  'to 272'

 L.2139       236  LOAD_FAST                'ftype'
              238  LOAD_GLOBAL              TType
              240  LOAD_ATTR                STRING
              242  COMPARE_OP               ==
          244_246  POP_JUMP_IF_FALSE   260  'to 260'

 L.2140       248  LOAD_FAST                'iprot'
              250  LOAD_METHOD              readBinary
              252  CALL_METHOD_0         0  '0 positional arguments'
              254  LOAD_FAST                'self'
              256  STORE_ATTR               endKey
              258  JUMP_FORWARD        270  'to 270'
            260_0  COME_FROM           244  '244'

 L.2142       260  LOAD_FAST                'iprot'
              262  LOAD_METHOD              skip
              264  LOAD_FAST                'ftype'
              266  CALL_METHOD_1         1  '1 positional argument'
              268  POP_TOP          
            270_0  COME_FROM           258  '258'
              270  JUMP_FORWARD        420  'to 420'
            272_0  COME_FROM           232  '232'

 L.2143       272  LOAD_FAST                'fid'
              274  LOAD_CONST               5
              276  COMPARE_OP               ==
          278_280  POP_JUMP_IF_FALSE   318  'to 318'

 L.2144       282  LOAD_FAST                'ftype'
              284  LOAD_GLOBAL              TType
              286  LOAD_ATTR                BOOL
              288  COMPARE_OP               ==
          290_292  POP_JUMP_IF_FALSE   306  'to 306'

 L.2145       294  LOAD_FAST                'iprot'
              296  LOAD_METHOD              readBool
              298  CALL_METHOD_0         0  '0 positional arguments'
              300  LOAD_FAST                'self'
              302  STORE_ATTR               offline
              304  JUMP_FORWARD        316  'to 316'
            306_0  COME_FROM           290  '290'

 L.2147       306  LOAD_FAST                'iprot'
              308  LOAD_METHOD              skip
              310  LOAD_FAST                'ftype'
              312  CALL_METHOD_1         1  '1 positional argument'
              314  POP_TOP          
            316_0  COME_FROM           304  '304'
              316  JUMP_FORWARD        420  'to 420'
            318_0  COME_FROM           278  '278'

 L.2148       318  LOAD_FAST                'fid'
              320  LOAD_CONST               6
              322  COMPARE_OP               ==
          324_326  POP_JUMP_IF_FALSE   364  'to 364'

 L.2149       328  LOAD_FAST                'ftype'
              330  LOAD_GLOBAL              TType
              332  LOAD_ATTR                BOOL
              334  COMPARE_OP               ==
          336_338  POP_JUMP_IF_FALSE   352  'to 352'

 L.2150       340  LOAD_FAST                'iprot'
              342  LOAD_METHOD              readBool
              344  CALL_METHOD_0         0  '0 positional arguments'
              346  LOAD_FAST                'self'
              348  STORE_ATTR               split
              350  JUMP_FORWARD        362  'to 362'
            352_0  COME_FROM           336  '336'

 L.2152       352  LOAD_FAST                'iprot'
              354  LOAD_METHOD              skip
              356  LOAD_FAST                'ftype'
              358  CALL_METHOD_1         1  '1 positional argument'
              360  POP_TOP          
            362_0  COME_FROM           350  '350'
              362  JUMP_FORWARD        420  'to 420'
            364_0  COME_FROM           324  '324'

 L.2153       364  LOAD_FAST                'fid'
              366  LOAD_CONST               7
              368  COMPARE_OP               ==
          370_372  POP_JUMP_IF_FALSE   410  'to 410'

 L.2154       374  LOAD_FAST                'ftype'
              376  LOAD_GLOBAL              TType
              378  LOAD_ATTR                I32
              380  COMPARE_OP               ==
          382_384  POP_JUMP_IF_FALSE   398  'to 398'

 L.2155       386  LOAD_FAST                'iprot'
              388  LOAD_METHOD              readI32
              390  CALL_METHOD_0         0  '0 positional arguments'
              392  LOAD_FAST                'self'
              394  STORE_ATTR               replicaId
              396  JUMP_FORWARD        408  'to 408'
            398_0  COME_FROM           382  '382'

 L.2157       398  LOAD_FAST                'iprot'
              400  LOAD_METHOD              skip
              402  LOAD_FAST                'ftype'
              404  CALL_METHOD_1         1  '1 positional argument'
            406_0  COME_FROM           126  '126'
              406  POP_TOP          
            408_0  COME_FROM           396  '396'
              408  JUMP_FORWARD        420  'to 420'
            410_0  COME_FROM           370  '370'

 L.2159       410  LOAD_FAST                'iprot'
              412  LOAD_METHOD              skip
              414  LOAD_FAST                'ftype'
              416  CALL_METHOD_1         1  '1 positional argument'
              418  POP_TOP          
            420_0  COME_FROM           408  '408'
            420_1  COME_FROM           362  '362'
            420_2  COME_FROM           316  '316'
            420_3  COME_FROM           270  '270'
            420_4  COME_FROM           224  '224'
            420_5  COME_FROM           182  '182'
            420_6  COME_FROM           138  '138'

 L.2160       420  LOAD_FAST                'iprot'
              422  LOAD_METHOD              readFieldEnd
              424  CALL_METHOD_0         0  '0 positional arguments'
              426  POP_TOP          
              428  JUMP_BACK            72  'to 72'
              430  POP_BLOCK        
            432_0  COME_FROM_LOOP       68  '68'

 L.2161       432  LOAD_FAST                'iprot'
              434  LOAD_METHOD              readStructEnd
              436  CALL_METHOD_0         0  '0 positional arguments'
              438  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 406_0

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('THRegionInfo')
        if self.regionId is not None:
            oprot.writeFieldBegin('regionId', TType.I64, 1)
            oprot.writeI64(self.regionId)
            oprot.writeFieldEnd()
        if self.tableName is not None:
            oprot.writeFieldBegin('tableName', TType.STRING, 2)
            oprot.writeBinary(self.tableName)
            oprot.writeFieldEnd()
        if self.startKey is not None:
            oprot.writeFieldBegin('startKey', TType.STRING, 3)
            oprot.writeBinary(self.startKey)
            oprot.writeFieldEnd()
        if self.endKey is not None:
            oprot.writeFieldBegin('endKey', TType.STRING, 4)
            oprot.writeBinary(self.endKey)
            oprot.writeFieldEnd()
        if self.offline is not None:
            oprot.writeFieldBegin('offline', TType.BOOL, 5)
            oprot.writeBool(self.offline)
            oprot.writeFieldEnd()
        if self.split is not None:
            oprot.writeFieldBegin('split', TType.BOOL, 6)
            oprot.writeBool(self.split)
            oprot.writeFieldEnd()
        if self.replicaId is not None:
            oprot.writeFieldBegin('replicaId', TType.I32, 7)
            oprot.writeI32(self.replicaId)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.regionId is None:
            raise TProtocolException(message='Required field regionId is unset!')
        if self.tableName is None:
            raise TProtocolException(message='Required field tableName is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TServerName(object):
    __doc__ = '\n    Attributes:\n     - hostName\n     - port\n     - startCode\n    '

    def __init__(self, hostName=None, port=None, startCode=None):
        self.hostName = hostName
        self.port = port
        self.startCode = startCode

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.hostName = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 2:
                    if ftype == TType.I32:
                        self.port = iprot.readI32()
                    else:
                        iprot.skip(ftype)
                else:
                    if fid == 3:
                        if ftype == TType.I64:
                            self.startCode = iprot.readI64()
                        else:
                            iprot.skip(ftype)
                    else:
                        iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TServerName')
        if self.hostName is not None:
            oprot.writeFieldBegin('hostName', TType.STRING, 1)
            oprot.writeString(self.hostName.encode('utf-8') if sys.version_info[0] == 2 else self.hostName)
            oprot.writeFieldEnd()
        if self.port is not None:
            oprot.writeFieldBegin('port', TType.I32, 2)
            oprot.writeI32(self.port)
            oprot.writeFieldEnd()
        if self.startCode is not None:
            oprot.writeFieldBegin('startCode', TType.I64, 3)
            oprot.writeI64(self.startCode)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.hostName is None:
            raise TProtocolException(message='Required field hostName is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class THRegionLocation(object):
    __doc__ = '\n    Attributes:\n     - serverName\n     - regionInfo\n    '

    def __init__(self, serverName=None, regionInfo=None):
        self.serverName = serverName
        self.regionInfo = regionInfo

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.serverName = TServerName()
                    self.serverName.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.regionInfo = THRegionInfo()
                    self.regionInfo.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('THRegionLocation')
        if self.serverName is not None:
            oprot.writeFieldBegin('serverName', TType.STRUCT, 1)
            self.serverName.write(oprot)
            oprot.writeFieldEnd()
        if self.regionInfo is not None:
            oprot.writeFieldBegin('regionInfo', TType.STRUCT, 2)
            self.regionInfo.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.serverName is None:
            raise TProtocolException(message='Required field serverName is unset!')
        if self.regionInfo is None:
            raise TProtocolException(message='Required field regionInfo is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TTableName(object):
    __doc__ = '\n    Thrift wrapper around\n    org.apache.hadoop.hbase.TableName\n\n    Attributes:\n     - ns: namespace name\n     - qualifier: tablename\n    '

    def __init__(self, ns=None, qualifier=None):
        self.ns = ns
        self.qualifier = qualifier

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.ns = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.qualifier = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TTableName')
        if self.ns is not None:
            oprot.writeFieldBegin('ns', TType.STRING, 1)
            oprot.writeBinary(self.ns)
            oprot.writeFieldEnd()
        if self.qualifier is not None:
            oprot.writeFieldBegin('qualifier', TType.STRING, 2)
            oprot.writeBinary(self.qualifier)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.qualifier is None:
            raise TProtocolException(message='Required field qualifier is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TColumnFamilyDescriptor(object):
    __doc__ = '\n    Thrift wrapper around\n    org.apache.hadoop.hbase.client.ColumnFamilyDescriptor\n\n    Attributes:\n     - name\n     - attributes\n     - configuration\n     - blockSize\n     - bloomnFilterType\n     - compressionType\n     - dfsReplication\n     - dataBlockEncoding\n     - keepDeletedCells\n     - maxVersions\n     - minVersions\n     - scope\n     - timeToLive\n     - blockCacheEnabled\n     - cacheBloomsOnWrite\n     - cacheDataOnWrite\n     - cacheIndexesOnWrite\n     - compressTags\n     - evictBlocksOnClose\n     - inMemory\n    '

    def __init__(self, name=None, attributes=None, configuration=None, blockSize=None, bloomnFilterType=None, compressionType=None, dfsReplication=None, dataBlockEncoding=None, keepDeletedCells=None, maxVersions=None, minVersions=None, scope=None, timeToLive=None, blockCacheEnabled=None, cacheBloomsOnWrite=None, cacheDataOnWrite=None, cacheIndexesOnWrite=None, compressTags=None, evictBlocksOnClose=None, inMemory=None):
        self.name = name
        self.attributes = attributes
        self.configuration = configuration
        self.blockSize = blockSize
        self.bloomnFilterType = bloomnFilterType
        self.compressionType = compressionType
        self.dfsReplication = dfsReplication
        self.dataBlockEncoding = dataBlockEncoding
        self.keepDeletedCells = keepDeletedCells
        self.maxVersions = maxVersions
        self.minVersions = minVersions
        self.scope = scope
        self.timeToLive = timeToLive
        self.blockCacheEnabled = blockCacheEnabled
        self.cacheBloomsOnWrite = cacheBloomsOnWrite
        self.cacheDataOnWrite = cacheDataOnWrite
        self.cacheIndexesOnWrite = cacheIndexesOnWrite
        self.compressTags = compressTags
        self.evictBlocksOnClose = evictBlocksOnClose
        self.inMemory = inMemory

    def read--- This code section failed: ---

 L.2495         0  LOAD_FAST                'iprot'
                2  LOAD_ATTR                _fast_decode
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    60  'to 60'
               10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'iprot'
               14  LOAD_ATTR                trans
               16  LOAD_GLOBAL              TTransport
               18  LOAD_ATTR                CReadableTransport
               20  CALL_FUNCTION_2       2  '2 positional arguments'
               22  POP_JUMP_IF_FALSE    60  'to 60'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                thrift_spec
               28  LOAD_CONST               None
               30  COMPARE_OP               is-not
               32  POP_JUMP_IF_FALSE    60  'to 60'

 L.2496        34  LOAD_FAST                'iprot'
               36  LOAD_METHOD              _fast_decode
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'iprot'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                __class__
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                thrift_spec
               50  BUILD_LIST_2          2 
               52  CALL_METHOD_3         3  '3 positional arguments'
               54  POP_TOP          

 L.2497        56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM            32  '32'
             60_1  COME_FROM            22  '22'
             60_2  COME_FROM             8  '8'

 L.2498        60  LOAD_FAST                'iprot'
               62  LOAD_METHOD              readStructBegin
               64  CALL_METHOD_0         0  '0 positional arguments'
               66  POP_TOP          

 L.2499     68_70  SETUP_LOOP         1246  'to 1246'

 L.2500        72  LOAD_FAST                'iprot'
               74  LOAD_METHOD              readFieldBegin
               76  CALL_METHOD_0         0  '0 positional arguments'
               78  UNPACK_SEQUENCE_3     3 
               80  STORE_FAST               'fname'
               82  STORE_FAST               'ftype'
               84  STORE_FAST               'fid'

 L.2501        86  LOAD_FAST                'ftype'
               88  LOAD_GLOBAL              TType
               90  LOAD_ATTR                STOP
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L.2502        96  BREAK_LOOP       
             98_0  COME_FROM            94  '94'

 L.2503        98  LOAD_FAST                'fid'
              100  LOAD_CONST               1
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   142  'to 142'

 L.2504       106  LOAD_FAST                'ftype'
              108  LOAD_GLOBAL              TType
              110  LOAD_ATTR                STRING
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   128  'to 128'

 L.2505       116  LOAD_FAST                'iprot'
              118  LOAD_METHOD              readBinary
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  LOAD_FAST                'self'
              124  STORE_ATTR               name
              126  JUMP_FORWARD       1234  'to 1234'
            128_0  COME_FROM           114  '114'

 L.2507       128  LOAD_FAST                'iprot'
              130  LOAD_METHOD              skip
              132  LOAD_FAST                'ftype'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  POP_TOP          
          138_140  JUMP_FORWARD       1234  'to 1234'
            142_0  COME_FROM           104  '104'

 L.2508       142  LOAD_FAST                'fid'
              144  LOAD_CONST               2
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   248  'to 248'

 L.2509       150  LOAD_FAST                'ftype'
              152  LOAD_GLOBAL              TType
              154  LOAD_ATTR                MAP
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   234  'to 234'

 L.2510       160  BUILD_MAP_0           0 
              162  LOAD_FAST                'self'
              164  STORE_ATTR               attributes

 L.2511       166  LOAD_FAST                'iprot'
              168  LOAD_METHOD              readMapBegin
              170  CALL_METHOD_0         0  '0 positional arguments'
              172  UNPACK_SEQUENCE_3     3 
              174  STORE_FAST               '_ktype127'
              176  STORE_FAST               '_vtype128'
              178  STORE_FAST               '_size126'

 L.2512       180  SETUP_LOOP          224  'to 224'
              182  LOAD_GLOBAL              range
              184  LOAD_FAST                '_size126'
              186  CALL_FUNCTION_1       1  '1 positional argument'
              188  GET_ITER         
              190  FOR_ITER            222  'to 222'
              192  STORE_FAST               '_i130'

 L.2513       194  LOAD_FAST                'iprot'
              196  LOAD_METHOD              readBinary
              198  CALL_METHOD_0         0  '0 positional arguments'
              200  STORE_FAST               '_key131'

 L.2514       202  LOAD_FAST                'iprot'
              204  LOAD_METHOD              readBinary
              206  CALL_METHOD_0         0  '0 positional arguments'
              208  STORE_FAST               '_val132'

 L.2515       210  LOAD_FAST                '_val132'
              212  LOAD_FAST                'self'
              214  LOAD_ATTR                attributes
              216  LOAD_FAST                '_key131'
              218  STORE_SUBSCR     
              220  JUMP_BACK           190  'to 190'
              222  POP_BLOCK        
            224_0  COME_FROM_LOOP      180  '180'

 L.2516       224  LOAD_FAST                'iprot'
              226  LOAD_METHOD              readMapEnd
              228  CALL_METHOD_0         0  '0 positional arguments'
              230  POP_TOP          
              232  JUMP_FORWARD       1234  'to 1234'
            234_0  COME_FROM           158  '158'

 L.2518       234  LOAD_FAST                'iprot'
              236  LOAD_METHOD              skip
              238  LOAD_FAST                'ftype'
              240  CALL_METHOD_1         1  '1 positional argument'
              242  POP_TOP          
          244_246  JUMP_FORWARD       1234  'to 1234'
            248_0  COME_FROM           148  '148'

 L.2519       248  LOAD_FAST                'fid'
              250  LOAD_CONST               3
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   420  'to 420'

 L.2520       258  LOAD_FAST                'ftype'
              260  LOAD_GLOBAL              TType
              262  LOAD_ATTR                MAP
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   406  'to 406'

 L.2521       270  BUILD_MAP_0           0 
              272  LOAD_FAST                'self'
              274  STORE_ATTR               configuration

 L.2522       276  LOAD_FAST                'iprot'
              278  LOAD_METHOD              readMapBegin
              280  CALL_METHOD_0         0  '0 positional arguments'
              282  UNPACK_SEQUENCE_3     3 
              284  STORE_FAST               '_ktype134'
              286  STORE_FAST               '_vtype135'
              288  STORE_FAST               '_size133'

 L.2523       290  SETUP_LOOP          396  'to 396'
              292  LOAD_GLOBAL              range
              294  LOAD_FAST                '_size133'
              296  CALL_FUNCTION_1       1  '1 positional argument'
              298  GET_ITER         
              300  FOR_ITER            394  'to 394'
              302  STORE_FAST               '_i137'

 L.2524       304  LOAD_GLOBAL              sys
              306  LOAD_ATTR                version_info
              308  LOAD_CONST               0
              310  BINARY_SUBSCR    
              312  LOAD_CONST               2
              314  COMPARE_OP               ==
          316_318  POP_JUMP_IF_FALSE   334  'to 334'
              320  LOAD_FAST                'iprot'
              322  LOAD_METHOD              readString
              324  CALL_METHOD_0         0  '0 positional arguments'
              326  LOAD_METHOD              decode
              328  LOAD_STR                 'utf-8'
              330  CALL_METHOD_1         1  '1 positional argument'
              332  JUMP_FORWARD        340  'to 340'
            334_0  COME_FROM           316  '316'
              334  LOAD_FAST                'iprot'
              336  LOAD_METHOD              readString
              338  CALL_METHOD_0         0  '0 positional arguments'
            340_0  COME_FROM           332  '332'
              340  STORE_FAST               '_key138'

 L.2525       342  LOAD_GLOBAL              sys
              344  LOAD_ATTR                version_info
              346  LOAD_CONST               0
              348  BINARY_SUBSCR    
              350  LOAD_CONST               2
              352  COMPARE_OP               ==
          354_356  POP_JUMP_IF_FALSE   372  'to 372'
              358  LOAD_FAST                'iprot'
              360  LOAD_METHOD              readString
              362  CALL_METHOD_0         0  '0 positional arguments'
              364  LOAD_METHOD              decode
              366  LOAD_STR                 'utf-8'
              368  CALL_METHOD_1         1  '1 positional argument'
              370  JUMP_FORWARD        378  'to 378'
            372_0  COME_FROM           354  '354'
              372  LOAD_FAST                'iprot'
              374  LOAD_METHOD              readString
              376  CALL_METHOD_0         0  '0 positional arguments'
            378_0  COME_FROM           370  '370'
              378  STORE_FAST               '_val139'

 L.2526       380  LOAD_FAST                '_val139'
              382  LOAD_FAST                'self'
              384  LOAD_ATTR                configuration
              386  LOAD_FAST                '_key138'
              388  STORE_SUBSCR     
          390_392  JUMP_BACK           300  'to 300'
              394  POP_BLOCK        
            396_0  COME_FROM_LOOP      290  '290'

 L.2527       396  LOAD_FAST                'iprot'
              398  LOAD_METHOD              readMapEnd
              400  CALL_METHOD_0         0  '0 positional arguments'
              402  POP_TOP          
              404  JUMP_FORWARD       1234  'to 1234'
            406_0  COME_FROM           266  '266'

 L.2529       406  LOAD_FAST                'iprot'
              408  LOAD_METHOD              skip
              410  LOAD_FAST                'ftype'
              412  CALL_METHOD_1         1  '1 positional argument'
              414  POP_TOP          
          416_418  JUMP_FORWARD       1234  'to 1234'
            420_0  COME_FROM           254  '254'

 L.2530       420  LOAD_FAST                'fid'
              422  LOAD_CONST               4
              424  COMPARE_OP               ==
          426_428  POP_JUMP_IF_FALSE   468  'to 468'

 L.2531       430  LOAD_FAST                'ftype'
              432  LOAD_GLOBAL              TType
              434  LOAD_ATTR                I32
              436  COMPARE_OP               ==
          438_440  POP_JUMP_IF_FALSE   454  'to 454'

 L.2532       442  LOAD_FAST                'iprot'
              444  LOAD_METHOD              readI32
              446  CALL_METHOD_0         0  '0 positional arguments'
              448  LOAD_FAST                'self'
              450  STORE_ATTR               blockSize
              452  JUMP_FORWARD       1234  'to 1234'
            454_0  COME_FROM           438  '438'

 L.2534       454  LOAD_FAST                'iprot'
              456  LOAD_METHOD              skip
              458  LOAD_FAST                'ftype'
              460  CALL_METHOD_1         1  '1 positional argument'
              462  POP_TOP          
          464_466  JUMP_FORWARD       1234  'to 1234'
            468_0  COME_FROM           426  '426'

 L.2535       468  LOAD_FAST                'fid'
              470  LOAD_CONST               5
              472  COMPARE_OP               ==
          474_476  POP_JUMP_IF_FALSE   516  'to 516'

 L.2536       478  LOAD_FAST                'ftype'
              480  LOAD_GLOBAL              TType
              482  LOAD_ATTR                I32
              484  COMPARE_OP               ==
          486_488  POP_JUMP_IF_FALSE   502  'to 502'

 L.2537       490  LOAD_FAST                'iprot'
              492  LOAD_METHOD              readI32
              494  CALL_METHOD_0         0  '0 positional arguments'
              496  LOAD_FAST                'self'
              498  STORE_ATTR               bloomnFilterType
              500  JUMP_FORWARD       1234  'to 1234'
            502_0  COME_FROM           486  '486'

 L.2539       502  LOAD_FAST                'iprot'
              504  LOAD_METHOD              skip
              506  LOAD_FAST                'ftype'
              508  CALL_METHOD_1         1  '1 positional argument'
              510  POP_TOP          
          512_514  JUMP_FORWARD       1234  'to 1234'
            516_0  COME_FROM           474  '474'

 L.2540       516  LOAD_FAST                'fid'
              518  LOAD_CONST               6
              520  COMPARE_OP               ==
          522_524  POP_JUMP_IF_FALSE   564  'to 564'

 L.2541       526  LOAD_FAST                'ftype'
              528  LOAD_GLOBAL              TType
              530  LOAD_ATTR                I32
              532  COMPARE_OP               ==
          534_536  POP_JUMP_IF_FALSE   550  'to 550'

 L.2542       538  LOAD_FAST                'iprot'
              540  LOAD_METHOD              readI32
              542  CALL_METHOD_0         0  '0 positional arguments'
              544  LOAD_FAST                'self'
              546  STORE_ATTR               compressionType
              548  JUMP_FORWARD       1234  'to 1234'
            550_0  COME_FROM           534  '534'

 L.2544       550  LOAD_FAST                'iprot'
              552  LOAD_METHOD              skip
              554  LOAD_FAST                'ftype'
              556  CALL_METHOD_1         1  '1 positional argument'
              558  POP_TOP          
          560_562  JUMP_FORWARD       1234  'to 1234'
            564_0  COME_FROM           522  '522'

 L.2545       564  LOAD_FAST                'fid'
              566  LOAD_CONST               7
              568  COMPARE_OP               ==
          570_572  POP_JUMP_IF_FALSE   612  'to 612'

 L.2546       574  LOAD_FAST                'ftype'
              576  LOAD_GLOBAL              TType
              578  LOAD_ATTR                I16
              580  COMPARE_OP               ==
          582_584  POP_JUMP_IF_FALSE   598  'to 598'

 L.2547       586  LOAD_FAST                'iprot'
              588  LOAD_METHOD              readI16
              590  CALL_METHOD_0         0  '0 positional arguments'
              592  LOAD_FAST                'self'
              594  STORE_ATTR               dfsReplication
              596  JUMP_FORWARD       1234  'to 1234'
            598_0  COME_FROM           582  '582'

 L.2549       598  LOAD_FAST                'iprot'
              600  LOAD_METHOD              skip
              602  LOAD_FAST                'ftype'
              604  CALL_METHOD_1         1  '1 positional argument'
              606  POP_TOP          
          608_610  JUMP_FORWARD       1234  'to 1234'
            612_0  COME_FROM           570  '570'

 L.2550       612  LOAD_FAST                'fid'
              614  LOAD_CONST               8
              616  COMPARE_OP               ==
          618_620  POP_JUMP_IF_FALSE   660  'to 660'

 L.2551       622  LOAD_FAST                'ftype'
              624  LOAD_GLOBAL              TType
              626  LOAD_ATTR                I32
              628  COMPARE_OP               ==
          630_632  POP_JUMP_IF_FALSE   646  'to 646'

 L.2552       634  LOAD_FAST                'iprot'
              636  LOAD_METHOD              readI32
              638  CALL_METHOD_0         0  '0 positional arguments'
              640  LOAD_FAST                'self'
              642  STORE_ATTR               dataBlockEncoding
              644  JUMP_FORWARD       1234  'to 1234'
            646_0  COME_FROM           630  '630'

 L.2554       646  LOAD_FAST                'iprot'
              648  LOAD_METHOD              skip
              650  LOAD_FAST                'ftype'
              652  CALL_METHOD_1         1  '1 positional argument'
              654  POP_TOP          
          656_658  JUMP_FORWARD       1234  'to 1234'
            660_0  COME_FROM           618  '618'

 L.2555       660  LOAD_FAST                'fid'
              662  LOAD_CONST               9
              664  COMPARE_OP               ==
          666_668  POP_JUMP_IF_FALSE   708  'to 708'

 L.2556       670  LOAD_FAST                'ftype'
              672  LOAD_GLOBAL              TType
              674  LOAD_ATTR                I32
              676  COMPARE_OP               ==
          678_680  POP_JUMP_IF_FALSE   694  'to 694'

 L.2557       682  LOAD_FAST                'iprot'
              684  LOAD_METHOD              readI32
              686  CALL_METHOD_0         0  '0 positional arguments'
              688  LOAD_FAST                'self'
              690  STORE_ATTR               keepDeletedCells
              692  JUMP_FORWARD       1234  'to 1234'
            694_0  COME_FROM           678  '678'

 L.2559       694  LOAD_FAST                'iprot'
              696  LOAD_METHOD              skip
              698  LOAD_FAST                'ftype'
              700  CALL_METHOD_1         1  '1 positional argument'
              702  POP_TOP          
          704_706  JUMP_FORWARD       1234  'to 1234'
            708_0  COME_FROM           666  '666'

 L.2560       708  LOAD_FAST                'fid'
              710  LOAD_CONST               10
              712  COMPARE_OP               ==
          714_716  POP_JUMP_IF_FALSE   756  'to 756'

 L.2561       718  LOAD_FAST                'ftype'
              720  LOAD_GLOBAL              TType
              722  LOAD_ATTR                I32
              724  COMPARE_OP               ==
          726_728  POP_JUMP_IF_FALSE   742  'to 742'

 L.2562       730  LOAD_FAST                'iprot'
              732  LOAD_METHOD              readI32
              734  CALL_METHOD_0         0  '0 positional arguments'
              736  LOAD_FAST                'self'
              738  STORE_ATTR               maxVersions
              740  JUMP_FORWARD       1234  'to 1234'
            742_0  COME_FROM           726  '726'

 L.2564       742  LOAD_FAST                'iprot'
              744  LOAD_METHOD              skip
              746  LOAD_FAST                'ftype'
              748  CALL_METHOD_1         1  '1 positional argument'
              750  POP_TOP          
          752_754  JUMP_FORWARD       1234  'to 1234'
            756_0  COME_FROM           714  '714'

 L.2565       756  LOAD_FAST                'fid'
              758  LOAD_CONST               11
              760  COMPARE_OP               ==
          762_764  POP_JUMP_IF_FALSE   804  'to 804'

 L.2566       766  LOAD_FAST                'ftype'
              768  LOAD_GLOBAL              TType
              770  LOAD_ATTR                I32
              772  COMPARE_OP               ==
          774_776  POP_JUMP_IF_FALSE   790  'to 790'

 L.2567       778  LOAD_FAST                'iprot'
              780  LOAD_METHOD              readI32
              782  CALL_METHOD_0         0  '0 positional arguments'
              784  LOAD_FAST                'self'
              786  STORE_ATTR               minVersions
              788  JUMP_FORWARD       1234  'to 1234'
            790_0  COME_FROM           774  '774'

 L.2569       790  LOAD_FAST                'iprot'
              792  LOAD_METHOD              skip
              794  LOAD_FAST                'ftype'
              796  CALL_METHOD_1         1  '1 positional argument'
              798  POP_TOP          
          800_802  JUMP_FORWARD       1234  'to 1234'
            804_0  COME_FROM           762  '762'

 L.2570       804  LOAD_FAST                'fid'
              806  LOAD_CONST               12
              808  COMPARE_OP               ==
          810_812  POP_JUMP_IF_FALSE   852  'to 852'

 L.2571       814  LOAD_FAST                'ftype'
              816  LOAD_GLOBAL              TType
              818  LOAD_ATTR                I32
              820  COMPARE_OP               ==
          822_824  POP_JUMP_IF_FALSE   838  'to 838'

 L.2572       826  LOAD_FAST                'iprot'
              828  LOAD_METHOD              readI32
              830  CALL_METHOD_0         0  '0 positional arguments'
              832  LOAD_FAST                'self'
              834  STORE_ATTR               scope
              836  JUMP_FORWARD       1234  'to 1234'
            838_0  COME_FROM           822  '822'

 L.2574       838  LOAD_FAST                'iprot'
              840  LOAD_METHOD              skip
              842  LOAD_FAST                'ftype'
              844  CALL_METHOD_1         1  '1 positional argument'
              846  POP_TOP          
          848_850  JUMP_FORWARD       1234  'to 1234'
            852_0  COME_FROM           810  '810'

 L.2575       852  LOAD_FAST                'fid'
              854  LOAD_CONST               13
              856  COMPARE_OP               ==
          858_860  POP_JUMP_IF_FALSE   900  'to 900'

 L.2576       862  LOAD_FAST                'ftype'
              864  LOAD_GLOBAL              TType
              866  LOAD_ATTR                I32
              868  COMPARE_OP               ==
          870_872  POP_JUMP_IF_FALSE   886  'to 886'

 L.2577       874  LOAD_FAST                'iprot'
              876  LOAD_METHOD              readI32
              878  CALL_METHOD_0         0  '0 positional arguments'
              880  LOAD_FAST                'self'
              882  STORE_ATTR               timeToLive
              884  JUMP_FORWARD       1234  'to 1234'
            886_0  COME_FROM           870  '870'

 L.2579       886  LOAD_FAST                'iprot'
              888  LOAD_METHOD              skip
              890  LOAD_FAST                'ftype'
              892  CALL_METHOD_1         1  '1 positional argument'
              894  POP_TOP          
          896_898  JUMP_FORWARD       1234  'to 1234'
            900_0  COME_FROM           858  '858'

 L.2580       900  LOAD_FAST                'fid'
              902  LOAD_CONST               14
              904  COMPARE_OP               ==
          906_908  POP_JUMP_IF_FALSE   948  'to 948'

 L.2581       910  LOAD_FAST                'ftype'
              912  LOAD_GLOBAL              TType
              914  LOAD_ATTR                BOOL
              916  COMPARE_OP               ==
          918_920  POP_JUMP_IF_FALSE   934  'to 934'

 L.2582       922  LOAD_FAST                'iprot'
              924  LOAD_METHOD              readBool
              926  CALL_METHOD_0         0  '0 positional arguments'
              928  LOAD_FAST                'self'
              930  STORE_ATTR               blockCacheEnabled
              932  JUMP_FORWARD       1234  'to 1234'
            934_0  COME_FROM           918  '918'

 L.2584       934  LOAD_FAST                'iprot'
              936  LOAD_METHOD              skip
              938  LOAD_FAST                'ftype'
              940  CALL_METHOD_1         1  '1 positional argument'
              942  POP_TOP          
          944_946  JUMP_FORWARD       1234  'to 1234'
            948_0  COME_FROM           906  '906'

 L.2585       948  LOAD_FAST                'fid'
              950  LOAD_CONST               15
              952  COMPARE_OP               ==
          954_956  POP_JUMP_IF_FALSE   994  'to 994'

 L.2586       958  LOAD_FAST                'ftype'
              960  LOAD_GLOBAL              TType
              962  LOAD_ATTR                BOOL
              964  COMPARE_OP               ==
          966_968  POP_JUMP_IF_FALSE   982  'to 982'

 L.2587       970  LOAD_FAST                'iprot'
              972  LOAD_METHOD              readBool
              974  CALL_METHOD_0         0  '0 positional arguments'
              976  LOAD_FAST                'self'
              978  STORE_ATTR               cacheBloomsOnWrite
              980  JUMP_FORWARD        992  'to 992'
            982_0  COME_FROM           966  '966'

 L.2589       982  LOAD_FAST                'iprot'
              984  LOAD_METHOD              skip
              986  LOAD_FAST                'ftype'
              988  CALL_METHOD_1         1  '1 positional argument'
              990  POP_TOP          
            992_0  COME_FROM           980  '980'
              992  JUMP_FORWARD       1234  'to 1234'
            994_0  COME_FROM           954  '954'

 L.2590       994  LOAD_FAST                'fid'
              996  LOAD_CONST               16
              998  COMPARE_OP               ==
         1000_1002  POP_JUMP_IF_FALSE  1040  'to 1040'

 L.2591      1004  LOAD_FAST                'ftype'
             1006  LOAD_GLOBAL              TType
             1008  LOAD_ATTR                BOOL
             1010  COMPARE_OP               ==
         1012_1014  POP_JUMP_IF_FALSE  1028  'to 1028'

 L.2592      1016  LOAD_FAST                'iprot'
             1018  LOAD_METHOD              readBool
             1020  CALL_METHOD_0         0  '0 positional arguments'
             1022  LOAD_FAST                'self'
             1024  STORE_ATTR               cacheDataOnWrite
             1026  JUMP_FORWARD       1038  'to 1038'
           1028_0  COME_FROM          1012  '1012'

 L.2594      1028  LOAD_FAST                'iprot'
             1030  LOAD_METHOD              skip
             1032  LOAD_FAST                'ftype'
             1034  CALL_METHOD_1         1  '1 positional argument'
             1036  POP_TOP          
           1038_0  COME_FROM          1026  '1026'
             1038  JUMP_FORWARD       1234  'to 1234'
           1040_0  COME_FROM          1000  '1000'

 L.2595      1040  LOAD_FAST                'fid'
             1042  LOAD_CONST               17
             1044  COMPARE_OP               ==
         1046_1048  POP_JUMP_IF_FALSE  1086  'to 1086'

 L.2596      1050  LOAD_FAST                'ftype'
             1052  LOAD_GLOBAL              TType
             1054  LOAD_ATTR                BOOL
             1056  COMPARE_OP               ==
         1058_1060  POP_JUMP_IF_FALSE  1074  'to 1074'

 L.2597      1062  LOAD_FAST                'iprot'
             1064  LOAD_METHOD              readBool
             1066  CALL_METHOD_0         0  '0 positional arguments'
             1068  LOAD_FAST                'self'
             1070  STORE_ATTR               cacheIndexesOnWrite
             1072  JUMP_FORWARD       1084  'to 1084'
           1074_0  COME_FROM          1058  '1058'

 L.2599      1074  LOAD_FAST                'iprot'
             1076  LOAD_METHOD              skip
             1078  LOAD_FAST                'ftype'
             1080  CALL_METHOD_1         1  '1 positional argument'
             1082  POP_TOP          
           1084_0  COME_FROM          1072  '1072'
             1084  JUMP_FORWARD       1234  'to 1234'
           1086_0  COME_FROM          1046  '1046'

 L.2600      1086  LOAD_FAST                'fid'
             1088  LOAD_CONST               18
             1090  COMPARE_OP               ==
         1092_1094  POP_JUMP_IF_FALSE  1132  'to 1132'

 L.2601      1096  LOAD_FAST                'ftype'
             1098  LOAD_GLOBAL              TType
             1100  LOAD_ATTR                BOOL
             1102  COMPARE_OP               ==
         1104_1106  POP_JUMP_IF_FALSE  1120  'to 1120'

 L.2602      1108  LOAD_FAST                'iprot'
             1110  LOAD_METHOD              readBool
             1112  CALL_METHOD_0         0  '0 positional arguments'
             1114  LOAD_FAST                'self'
             1116  STORE_ATTR               compressTags
             1118  JUMP_FORWARD       1130  'to 1130'
           1120_0  COME_FROM          1104  '1104'

 L.2604      1120  LOAD_FAST                'iprot'
             1122  LOAD_METHOD              skip
             1124  LOAD_FAST                'ftype'
             1126  CALL_METHOD_1         1  '1 positional argument'
             1128  POP_TOP          
           1130_0  COME_FROM          1118  '1118'
             1130  JUMP_FORWARD       1234  'to 1234'
           1132_0  COME_FROM          1092  '1092'

 L.2605      1132  LOAD_FAST                'fid'
             1134  LOAD_CONST               19
             1136  COMPARE_OP               ==
         1138_1140  POP_JUMP_IF_FALSE  1178  'to 1178'

 L.2606      1142  LOAD_FAST                'ftype'
             1144  LOAD_GLOBAL              TType
             1146  LOAD_ATTR                BOOL
             1148  COMPARE_OP               ==
         1150_1152  POP_JUMP_IF_FALSE  1166  'to 1166'

 L.2607      1154  LOAD_FAST                'iprot'
             1156  LOAD_METHOD              readBool
             1158  CALL_METHOD_0         0  '0 positional arguments'
             1160  LOAD_FAST                'self'
             1162  STORE_ATTR               evictBlocksOnClose
             1164  JUMP_FORWARD       1176  'to 1176'
           1166_0  COME_FROM          1150  '1150'

 L.2609      1166  LOAD_FAST                'iprot'
             1168  LOAD_METHOD              skip
             1170  LOAD_FAST                'ftype'
             1172  CALL_METHOD_1         1  '1 positional argument'
             1174  POP_TOP          
           1176_0  COME_FROM          1164  '1164'
             1176  JUMP_FORWARD       1234  'to 1234'
           1178_0  COME_FROM          1138  '1138'

 L.2610      1178  LOAD_FAST                'fid'
             1180  LOAD_CONST               20
             1182  COMPARE_OP               ==
         1184_1186  POP_JUMP_IF_FALSE  1224  'to 1224'

 L.2611      1188  LOAD_FAST                'ftype'
             1190  LOAD_GLOBAL              TType
             1192  LOAD_ATTR                BOOL
             1194  COMPARE_OP               ==
         1196_1198  POP_JUMP_IF_FALSE  1212  'to 1212'

 L.2612      1200  LOAD_FAST                'iprot'
             1202  LOAD_METHOD              readBool
             1204  CALL_METHOD_0         0  '0 positional arguments'
             1206  LOAD_FAST                'self'
             1208  STORE_ATTR               inMemory
             1210  JUMP_FORWARD       1222  'to 1222'
           1212_0  COME_FROM          1196  '1196'

 L.2614      1212  LOAD_FAST                'iprot'
             1214  LOAD_METHOD              skip
             1216  LOAD_FAST                'ftype'
             1218  CALL_METHOD_1         1  '1 positional argument'
           1220_0  COME_FROM           932  '932'
           1220_1  COME_FROM           884  '884'
           1220_2  COME_FROM           836  '836'
           1220_3  COME_FROM           788  '788'
           1220_4  COME_FROM           740  '740'
           1220_5  COME_FROM           692  '692'
           1220_6  COME_FROM           644  '644'
           1220_7  COME_FROM           596  '596'
           1220_8  COME_FROM           548  '548'
           1220_9  COME_FROM           500  '500'
          1220_10  COME_FROM           452  '452'
          1220_11  COME_FROM           404  '404'
          1220_12  COME_FROM           232  '232'
          1220_13  COME_FROM           126  '126'
             1220  POP_TOP          
           1222_0  COME_FROM          1210  '1210'
             1222  JUMP_FORWARD       1234  'to 1234'
           1224_0  COME_FROM          1184  '1184'

 L.2616      1224  LOAD_FAST                'iprot'
             1226  LOAD_METHOD              skip
             1228  LOAD_FAST                'ftype'
             1230  CALL_METHOD_1         1  '1 positional argument'
             1232  POP_TOP          
           1234_0  COME_FROM          1222  '1222'
           1234_1  COME_FROM          1176  '1176'
           1234_2  COME_FROM          1130  '1130'
           1234_3  COME_FROM          1084  '1084'
           1234_4  COME_FROM          1038  '1038'
           1234_5  COME_FROM           992  '992'
           1234_6  COME_FROM           944  '944'
           1234_7  COME_FROM           896  '896'
           1234_8  COME_FROM           848  '848'
           1234_9  COME_FROM           800  '800'
          1234_10  COME_FROM           752  '752'
          1234_11  COME_FROM           704  '704'
          1234_12  COME_FROM           656  '656'
          1234_13  COME_FROM           608  '608'
          1234_14  COME_FROM           560  '560'
          1234_15  COME_FROM           512  '512'
          1234_16  COME_FROM           464  '464'
          1234_17  COME_FROM           416  '416'
          1234_18  COME_FROM           244  '244'
          1234_19  COME_FROM           138  '138'

 L.2617      1234  LOAD_FAST                'iprot'
             1236  LOAD_METHOD              readFieldEnd
             1238  CALL_METHOD_0         0  '0 positional arguments'
             1240  POP_TOP          
             1242  JUMP_BACK            72  'to 72'
             1244  POP_BLOCK        
           1246_0  COME_FROM_LOOP       68  '68'

 L.2618      1246  LOAD_FAST                'iprot'
             1248  LOAD_METHOD              readStructEnd
             1250  CALL_METHOD_0         0  '0 positional arguments'
             1252  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 1220_0

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TColumnFamilyDescriptor')
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 1)
            oprot.writeBinary(self.name)
            oprot.writeFieldEnd()
        if self.attributes is not None:
            oprot.writeFieldBegin('attributes', TType.MAP, 2)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.attributes))
            for kiter140, viter141 in self.attributes.items():
                oprot.writeBinary(kiter140)
                oprot.writeBinary(viter141)

            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        if self.configuration is not None:
            oprot.writeFieldBegin('configuration', TType.MAP, 3)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.configuration))
            for kiter142, viter143 in self.configuration.items():
                oprot.writeString(kiter142.encode('utf-8') if sys.version_info[0] == 2 else kiter142)
                oprot.writeString(viter143.encode('utf-8') if sys.version_info[0] == 2 else viter143)

            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        if self.blockSize is not None:
            oprot.writeFieldBegin('blockSize', TType.I32, 4)
            oprot.writeI32(self.blockSize)
            oprot.writeFieldEnd()
        if self.bloomnFilterType is not None:
            oprot.writeFieldBegin('bloomnFilterType', TType.I32, 5)
            oprot.writeI32(self.bloomnFilterType)
            oprot.writeFieldEnd()
        if self.compressionType is not None:
            oprot.writeFieldBegin('compressionType', TType.I32, 6)
            oprot.writeI32(self.compressionType)
            oprot.writeFieldEnd()
        if self.dfsReplication is not None:
            oprot.writeFieldBegin('dfsReplication', TType.I16, 7)
            oprot.writeI16(self.dfsReplication)
            oprot.writeFieldEnd()
        if self.dataBlockEncoding is not None:
            oprot.writeFieldBegin('dataBlockEncoding', TType.I32, 8)
            oprot.writeI32(self.dataBlockEncoding)
            oprot.writeFieldEnd()
        if self.keepDeletedCells is not None:
            oprot.writeFieldBegin('keepDeletedCells', TType.I32, 9)
            oprot.writeI32(self.keepDeletedCells)
            oprot.writeFieldEnd()
        if self.maxVersions is not None:
            oprot.writeFieldBegin('maxVersions', TType.I32, 10)
            oprot.writeI32(self.maxVersions)
            oprot.writeFieldEnd()
        if self.minVersions is not None:
            oprot.writeFieldBegin('minVersions', TType.I32, 11)
            oprot.writeI32(self.minVersions)
            oprot.writeFieldEnd()
        if self.scope is not None:
            oprot.writeFieldBegin('scope', TType.I32, 12)
            oprot.writeI32(self.scope)
            oprot.writeFieldEnd()
        if self.timeToLive is not None:
            oprot.writeFieldBegin('timeToLive', TType.I32, 13)
            oprot.writeI32(self.timeToLive)
            oprot.writeFieldEnd()
        if self.blockCacheEnabled is not None:
            oprot.writeFieldBegin('blockCacheEnabled', TType.BOOL, 14)
            oprot.writeBool(self.blockCacheEnabled)
            oprot.writeFieldEnd()
        if self.cacheBloomsOnWrite is not None:
            oprot.writeFieldBegin('cacheBloomsOnWrite', TType.BOOL, 15)
            oprot.writeBool(self.cacheBloomsOnWrite)
            oprot.writeFieldEnd()
        if self.cacheDataOnWrite is not None:
            oprot.writeFieldBegin('cacheDataOnWrite', TType.BOOL, 16)
            oprot.writeBool(self.cacheDataOnWrite)
            oprot.writeFieldEnd()
        if self.cacheIndexesOnWrite is not None:
            oprot.writeFieldBegin('cacheIndexesOnWrite', TType.BOOL, 17)
            oprot.writeBool(self.cacheIndexesOnWrite)
            oprot.writeFieldEnd()
        if self.compressTags is not None:
            oprot.writeFieldBegin('compressTags', TType.BOOL, 18)
            oprot.writeBool(self.compressTags)
            oprot.writeFieldEnd()
        if self.evictBlocksOnClose is not None:
            oprot.writeFieldBegin('evictBlocksOnClose', TType.BOOL, 19)
            oprot.writeBool(self.evictBlocksOnClose)
            oprot.writeFieldEnd()
        if self.inMemory is not None:
            oprot.writeFieldBegin('inMemory', TType.BOOL, 20)
            oprot.writeBool(self.inMemory)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.name is None:
            raise TProtocolException(message='Required field name is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TTableDescriptor(object):
    __doc__ = '\n    Thrift wrapper around\n    org.apache.hadoop.hbase.client.TableDescriptor\n\n    Attributes:\n     - tableName\n     - columns\n     - attributes\n     - durability\n    '

    def __init__(self, tableName=None, columns=None, attributes=None, durability=None):
        self.tableName = tableName
        self.columns = columns
        self.attributes = attributes
        self.durability = durability

    def read--- This code section failed: ---

 L.2753         0  LOAD_FAST                'iprot'
                2  LOAD_ATTR                _fast_decode
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    60  'to 60'
               10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'iprot'
               14  LOAD_ATTR                trans
               16  LOAD_GLOBAL              TTransport
               18  LOAD_ATTR                CReadableTransport
               20  CALL_FUNCTION_2       2  '2 positional arguments'
               22  POP_JUMP_IF_FALSE    60  'to 60'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                thrift_spec
               28  LOAD_CONST               None
               30  COMPARE_OP               is-not
               32  POP_JUMP_IF_FALSE    60  'to 60'

 L.2754        34  LOAD_FAST                'iprot'
               36  LOAD_METHOD              _fast_decode
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'iprot'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                __class__
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                thrift_spec
               50  BUILD_LIST_2          2 
               52  CALL_METHOD_3         3  '3 positional arguments'
               54  POP_TOP          

 L.2755        56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM            32  '32'
             60_1  COME_FROM            22  '22'
             60_2  COME_FROM             8  '8'

 L.2756        60  LOAD_FAST                'iprot'
               62  LOAD_METHOD              readStructBegin
               64  CALL_METHOD_0         0  '0 positional arguments'
               66  POP_TOP          

 L.2757     68_70  SETUP_LOOP          436  'to 436'

 L.2758        72  LOAD_FAST                'iprot'
               74  LOAD_METHOD              readFieldBegin
               76  CALL_METHOD_0         0  '0 positional arguments'
               78  UNPACK_SEQUENCE_3     3 
               80  STORE_FAST               'fname'
               82  STORE_FAST               'ftype'
               84  STORE_FAST               'fid'

 L.2759        86  LOAD_FAST                'ftype'
               88  LOAD_GLOBAL              TType
               90  LOAD_ATTR                STOP
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L.2760        96  BREAK_LOOP       
             98_0  COME_FROM            94  '94'

 L.2761        98  LOAD_FAST                'fid'
              100  LOAD_CONST               1
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   152  'to 152'

 L.2762       106  LOAD_FAST                'ftype'
              108  LOAD_GLOBAL              TType
              110  LOAD_ATTR                STRUCT
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   138  'to 138'

 L.2763       116  LOAD_GLOBAL              TTableName
              118  CALL_FUNCTION_0       0  '0 positional arguments'
              120  LOAD_FAST                'self'
              122  STORE_ATTR               tableName

 L.2764       124  LOAD_FAST                'self'
              126  LOAD_ATTR                tableName
              128  LOAD_METHOD              read
              130  LOAD_FAST                'iprot'
              132  CALL_METHOD_1         1  '1 positional argument'
              134  POP_TOP          
              136  JUMP_FORWARD        424  'to 424'
            138_0  COME_FROM           114  '114'

 L.2766       138  LOAD_FAST                'iprot'
              140  LOAD_METHOD              skip
              142  LOAD_FAST                'ftype'
              144  CALL_METHOD_1         1  '1 positional argument'
              146  POP_TOP          
          148_150  JUMP_FORWARD        424  'to 424'
            152_0  COME_FROM           104  '104'

 L.2767       152  LOAD_FAST                'fid'
              154  LOAD_CONST               2
              156  COMPARE_OP               ==
          158_160  POP_JUMP_IF_FALSE   258  'to 258'

 L.2768       162  LOAD_FAST                'ftype'
              164  LOAD_GLOBAL              TType
              166  LOAD_ATTR                LIST
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE   246  'to 246'

 L.2769       172  BUILD_LIST_0          0 
              174  LOAD_FAST                'self'
              176  STORE_ATTR               columns

 L.2770       178  LOAD_FAST                'iprot'
              180  LOAD_METHOD              readListBegin
              182  CALL_METHOD_0         0  '0 positional arguments'
              184  UNPACK_SEQUENCE_2     2 
              186  STORE_FAST               '_etype147'
              188  STORE_FAST               '_size144'

 L.2771       190  SETUP_LOOP          236  'to 236'
              192  LOAD_GLOBAL              range
              194  LOAD_FAST                '_size144'
              196  CALL_FUNCTION_1       1  '1 positional argument'
              198  GET_ITER         
              200  FOR_ITER            234  'to 234'
              202  STORE_FAST               '_i148'

 L.2772       204  LOAD_GLOBAL              TColumnFamilyDescriptor
              206  CALL_FUNCTION_0       0  '0 positional arguments'
              208  STORE_FAST               '_elem149'

 L.2773       210  LOAD_FAST                '_elem149'
              212  LOAD_METHOD              read
              214  LOAD_FAST                'iprot'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  POP_TOP          

 L.2774       220  LOAD_FAST                'self'
              222  LOAD_ATTR                columns
              224  LOAD_METHOD              append
              226  LOAD_FAST                '_elem149'
              228  CALL_METHOD_1         1  '1 positional argument'
              230  POP_TOP          
              232  JUMP_BACK           200  'to 200'
              234  POP_BLOCK        
            236_0  COME_FROM_LOOP      190  '190'

 L.2775       236  LOAD_FAST                'iprot'
              238  LOAD_METHOD              readListEnd
              240  CALL_METHOD_0         0  '0 positional arguments'
              242  POP_TOP          
              244  JUMP_FORWARD        256  'to 256'
            246_0  COME_FROM           170  '170'

 L.2777       246  LOAD_FAST                'iprot'
              248  LOAD_METHOD              skip
              250  LOAD_FAST                'ftype'
              252  CALL_METHOD_1         1  '1 positional argument'
              254  POP_TOP          
            256_0  COME_FROM           244  '244'
              256  JUMP_FORWARD        424  'to 424'
            258_0  COME_FROM           158  '158'

 L.2778       258  LOAD_FAST                'fid'
              260  LOAD_CONST               3
              262  COMPARE_OP               ==
          264_266  POP_JUMP_IF_FALSE   368  'to 368'

 L.2779       268  LOAD_FAST                'ftype'
              270  LOAD_GLOBAL              TType
              272  LOAD_ATTR                MAP
              274  COMPARE_OP               ==
          276_278  POP_JUMP_IF_FALSE   356  'to 356'

 L.2780       280  BUILD_MAP_0           0 
              282  LOAD_FAST                'self'
              284  STORE_ATTR               attributes

 L.2781       286  LOAD_FAST                'iprot'
              288  LOAD_METHOD              readMapBegin
              290  CALL_METHOD_0         0  '0 positional arguments'
              292  UNPACK_SEQUENCE_3     3 
              294  STORE_FAST               '_ktype151'
              296  STORE_FAST               '_vtype152'
              298  STORE_FAST               '_size150'

 L.2782       300  SETUP_LOOP          346  'to 346'
              302  LOAD_GLOBAL              range
              304  LOAD_FAST                '_size150'
              306  CALL_FUNCTION_1       1  '1 positional argument'
              308  GET_ITER         
              310  FOR_ITER            344  'to 344'
              312  STORE_FAST               '_i154'

 L.2783       314  LOAD_FAST                'iprot'
              316  LOAD_METHOD              readBinary
              318  CALL_METHOD_0         0  '0 positional arguments'
              320  STORE_FAST               '_key155'

 L.2784       322  LOAD_FAST                'iprot'
              324  LOAD_METHOD              readBinary
              326  CALL_METHOD_0         0  '0 positional arguments'
              328  STORE_FAST               '_val156'

 L.2785       330  LOAD_FAST                '_val156'
              332  LOAD_FAST                'self'
              334  LOAD_ATTR                attributes
              336  LOAD_FAST                '_key155'
              338  STORE_SUBSCR     
          340_342  JUMP_BACK           310  'to 310'
              344  POP_BLOCK        
            346_0  COME_FROM_LOOP      300  '300'

 L.2786       346  LOAD_FAST                'iprot'
              348  LOAD_METHOD              readMapEnd
              350  CALL_METHOD_0         0  '0 positional arguments'
              352  POP_TOP          
              354  JUMP_FORWARD        366  'to 366'
            356_0  COME_FROM           276  '276'

 L.2788       356  LOAD_FAST                'iprot'
              358  LOAD_METHOD              skip
              360  LOAD_FAST                'ftype'
              362  CALL_METHOD_1         1  '1 positional argument'
              364  POP_TOP          
            366_0  COME_FROM           354  '354'
              366  JUMP_FORWARD        424  'to 424'
            368_0  COME_FROM           264  '264'

 L.2789       368  LOAD_FAST                'fid'
              370  LOAD_CONST               4
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   414  'to 414'

 L.2790       378  LOAD_FAST                'ftype'
              380  LOAD_GLOBAL              TType
              382  LOAD_ATTR                I32
              384  COMPARE_OP               ==
          386_388  POP_JUMP_IF_FALSE   402  'to 402'

 L.2791       390  LOAD_FAST                'iprot'
              392  LOAD_METHOD              readI32
              394  CALL_METHOD_0         0  '0 positional arguments'
              396  LOAD_FAST                'self'
              398  STORE_ATTR               durability
              400  JUMP_FORWARD        412  'to 412'
            402_0  COME_FROM           386  '386'

 L.2793       402  LOAD_FAST                'iprot'
              404  LOAD_METHOD              skip
              406  LOAD_FAST                'ftype'
              408  CALL_METHOD_1         1  '1 positional argument'
            410_0  COME_FROM           136  '136'
              410  POP_TOP          
            412_0  COME_FROM           400  '400'
              412  JUMP_FORWARD        424  'to 424'
            414_0  COME_FROM           374  '374'

 L.2795       414  LOAD_FAST                'iprot'
              416  LOAD_METHOD              skip
              418  LOAD_FAST                'ftype'
              420  CALL_METHOD_1         1  '1 positional argument'
              422  POP_TOP          
            424_0  COME_FROM           412  '412'
            424_1  COME_FROM           366  '366'
            424_2  COME_FROM           256  '256'
            424_3  COME_FROM           148  '148'

 L.2796       424  LOAD_FAST                'iprot'
              426  LOAD_METHOD              readFieldEnd
              428  CALL_METHOD_0         0  '0 positional arguments'
              430  POP_TOP          
              432  JUMP_BACK            72  'to 72'
              434  POP_BLOCK        
            436_0  COME_FROM_LOOP       68  '68'

 L.2797       436  LOAD_FAST                'iprot'
              438  LOAD_METHOD              readStructEnd
              440  CALL_METHOD_0         0  '0 positional arguments'
              442  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 410_0

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TTableDescriptor')
        if self.tableName is not None:
            oprot.writeFieldBegin('tableName', TType.STRUCT, 1)
            self.tableName.write(oprot)
            oprot.writeFieldEnd()
        if self.columns is not None:
            oprot.writeFieldBegin('columns', TType.LIST, 2)
            oprot.writeListBegin(TType.STRUCT, len(self.columns))
            for iter157 in self.columns:
                iter157.write(oprot)

            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.attributes is not None:
            oprot.writeFieldBegin('attributes', TType.MAP, 3)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.attributes))
            for kiter158, viter159 in self.attributes.items():
                oprot.writeBinary(kiter158)
                oprot.writeBinary(viter159)

            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        if self.durability is not None:
            oprot.writeFieldBegin('durability', TType.I32, 4)
            oprot.writeI32(self.durability)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.tableName is None:
            raise TProtocolException(message='Required field tableName is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TNamespaceDescriptor(object):
    __doc__ = '\n    Thrift wrapper around\n    org.apache.hadoop.hbase.NamespaceDescriptor\n\n    Attributes:\n     - name\n     - configuration\n    '

    def __init__(self, name=None, configuration=None):
        self.name = name
        self.configuration = configuration

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                if fid == 2:
                    if ftype == TType.MAP:
                        self.configuration = {}
                        _ktype161, _vtype162, _size160 = iprot.readMapBegin()
                        for _i164 in range(_size160):
                            _key165 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                            _val166 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                            self.configuration[_key165] = _val166

                        iprot.readMapEnd()
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TNamespaceDescriptor')
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 1)
            oprot.writeString(self.name.encode('utf-8') if sys.version_info[0] == 2 else self.name)
            oprot.writeFieldEnd()
        if self.configuration is not None:
            oprot.writeFieldBegin('configuration', TType.MAP, 2)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.configuration))
            for kiter167, viter168 in self.configuration.items():
                oprot.writeString(kiter167.encode('utf-8') if sys.version_info[0] == 2 else kiter167)
                oprot.writeString(viter168.encode('utf-8') if sys.version_info[0] == 2 else viter168)

            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.name is None:
            raise TProtocolException(message='Required field name is unset!')

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TIOError(TException):
    __doc__ = '\n    A TIOError exception signals that an error occurred communicating\n    to the HBase master or a HBase region server. Also used to return\n    more general HBase error conditions.\n\n    Attributes:\n     - message\n    '

    def __init__(self, message=None):
        self.message = message

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.message = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TIOError')
        if self.message is not None:
            oprot.writeFieldBegin('message', TType.STRING, 1)
            oprot.writeString(self.message.encode('utf-8') if sys.version_info[0] == 2 else self.message)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class TIllegalArgument(TException):
    __doc__ = '\n    A TIllegalArgument exception indicates an illegal or invalid\n    argument was passed into a procedure.\n\n    Attributes:\n     - message\n    '

    def __init__(self, message=None):
        self.message = message

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            elif fid == 1:
                if ftype == TType.STRING:
                    self.message = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('TIllegalArgument')
        if self.message is not None:
            oprot.writeFieldBegin('message', TType.STRING, 1)
            oprot.writeString(self.message.encode('utf-8') if sys.version_info[0] == 2 else self.message)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(TTimeRange)
TTimeRange.thrift_spec = (
 None,
 (
  1, TType.I64, 'minStamp', None, None),
 (
  2, TType.I64, 'maxStamp', None, None))
all_structs.append(TColumn)
TColumn.thrift_spec = (
 None,
 (
  1, TType.STRING, 'family', 'BINARY', None),
 (
  2, TType.STRING, 'qualifier', 'BINARY', None),
 (
  3, TType.I64, 'timestamp', None, None))
all_structs.append(TColumnValue)
TColumnValue.thrift_spec = (
 None,
 (
  1, TType.STRING, 'family', 'BINARY', None),
 (
  2, TType.STRING, 'qualifier', 'BINARY', None),
 (
  3, TType.STRING, 'value', 'BINARY', None),
 (
  4, TType.I64, 'timestamp', None, None),
 (
  5, TType.STRING, 'tags', 'BINARY', None),
 (
  6, TType.BYTE, 'type', None, None))
all_structs.append(TColumnIncrement)
TColumnIncrement.thrift_spec = (
 None,
 (
  1, TType.STRING, 'family', 'BINARY', None),
 (
  2, TType.STRING, 'qualifier', 'BINARY', None),
 (
  3, TType.I64, 'amount', None, 1))
all_structs.append(TResult)
TResult.thrift_spec = (
 None,
 (
  1, TType.STRING, 'row', 'BINARY', None),
 (
  2, TType.LIST, 'columnValues', (TType.STRUCT, [TColumnValue, None], False), None),
 (
  3, TType.BOOL, 'stale', None, False),
 (
  4, TType.BOOL, 'partial', None, False))
all_structs.append(TAuthorization)
TAuthorization.thrift_spec = (
 None,
 (
  1, TType.LIST, 'labels', (TType.STRING, 'UTF8', False), None))
all_structs.append(TCellVisibility)
TCellVisibility.thrift_spec = (
 None,
 (
  1, TType.STRING, 'expression', 'UTF8', None))
all_structs.append(TGet)
TGet.thrift_spec = (
 None,
 (
  1, TType.STRING, 'row', 'BINARY', None),
 (
  2, TType.LIST, 'columns', (TType.STRUCT, [TColumn, None], False), None),
 (
  3, TType.I64, 'timestamp', None, None),
 (
  4, TType.STRUCT, 'timeRange', [TTimeRange, None], None),
 (
  5, TType.I32, 'maxVersions', None, None),
 (
  6, TType.STRING, 'filterString', 'BINARY', None),
 (
  7, TType.MAP, 'attributes', (TType.STRING, 'BINARY', TType.STRING, 'BINARY', False), None),
 (
  8, TType.STRUCT, 'authorizations', [TAuthorization, None], None),
 (
  9, TType.I32, 'consistency', None, None),
 (
  10, TType.I32, 'targetReplicaId', None, None),
 (
  11, TType.BOOL, 'cacheBlocks', None, None),
 (
  12, TType.I32, 'storeLimit', None, None),
 (
  13, TType.I32, 'storeOffset', None, None),
 (
  14, TType.BOOL, 'existence_only', None, None),
 (
  15, TType.STRING, 'filterBytes', 'BINARY', None))
all_structs.append(TPut)
TPut.thrift_spec = (
 None,
 (
  1, TType.STRING, 'row', 'BINARY', None),
 (
  2, TType.LIST, 'columnValues', (TType.STRUCT, [TColumnValue, None], False), None),
 (
  3, TType.I64, 'timestamp', None, None),
 None,
 (
  5, TType.MAP, 'attributes', (TType.STRING, 'BINARY', TType.STRING, 'BINARY', False), None),
 (
  6, TType.I32, 'durability', None, None),
 (
  7, TType.STRUCT, 'cellVisibility', [TCellVisibility, None], None))
all_structs.append(TDelete)
TDelete.thrift_spec = (
 None,
 (
  1, TType.STRING, 'row', 'BINARY', None),
 (
  2, TType.LIST, 'columns', (TType.STRUCT, [TColumn, None], False), None),
 (
  3, TType.I64, 'timestamp', None, None),
 (
  4, TType.I32, 'deleteType', None, 1),
 None,
 (
  6, TType.MAP, 'attributes', (TType.STRING, 'BINARY', TType.STRING, 'BINARY', False), None),
 (
  7, TType.I32, 'durability', None, None))
all_structs.append(TIncrement)
TIncrement.thrift_spec = (
 None,
 (
  1, TType.STRING, 'row', 'BINARY', None),
 (
  2, TType.LIST, 'columns', (TType.STRUCT, [TColumnIncrement, None], False), None),
 None,
 (
  4, TType.MAP, 'attributes', (TType.STRING, 'BINARY', TType.STRING, 'BINARY', False), None),
 (
  5, TType.I32, 'durability', None, None),
 (
  6, TType.STRUCT, 'cellVisibility', [TCellVisibility, None], None),
 (
  7, TType.BOOL, 'returnResults', None, None))
all_structs.append(TAppend)
TAppend.thrift_spec = (
 None,
 (
  1, TType.STRING, 'row', 'BINARY', None),
 (
  2, TType.LIST, 'columns', (TType.STRUCT, [TColumnValue, None], False), None),
 (
  3, TType.MAP, 'attributes', (TType.STRING, 'BINARY', TType.STRING, 'BINARY', False), None),
 (
  4, TType.I32, 'durability', None, None),
 (
  5, TType.STRUCT, 'cellVisibility', [TCellVisibility, None], None),
 (
  6, TType.BOOL, 'returnResults', None, None))
all_structs.append(TScan)
TScan.thrift_spec = (
 None,
 (
  1, TType.STRING, 'startRow', 'BINARY', None),
 (
  2, TType.STRING, 'stopRow', 'BINARY', None),
 (
  3, TType.LIST, 'columns', (TType.STRUCT, [TColumn, None], False), None),
 (
  4, TType.I32, 'caching', None, None),
 (
  5, TType.I32, 'maxVersions', None, 1),
 (
  6, TType.STRUCT, 'timeRange', [TTimeRange, None], None),
 (
  7, TType.STRING, 'filterString', 'BINARY', None),
 (
  8, TType.I32, 'batchSize', None, None),
 (
  9, TType.MAP, 'attributes', (TType.STRING, 'BINARY', TType.STRING, 'BINARY', False), None),
 (
  10, TType.STRUCT, 'authorizations', [TAuthorization, None], None),
 (
  11, TType.BOOL, 'reversed', None, None),
 (
  12, TType.BOOL, 'cacheBlocks', None, None),
 (
  13, TType.MAP, 'colFamTimeRangeMap', (TType.STRING, 'BINARY', TType.STRUCT, [TTimeRange, None], False), None),
 (
  14, TType.I32, 'readType', None, None),
 (
  15, TType.I32, 'limit', None, None),
 (
  16, TType.I32, 'consistency', None, None),
 (
  17, TType.I32, 'targetReplicaId', None, None),
 (
  18, TType.STRING, 'filterBytes', 'BINARY', None))
all_structs.append(TMutation)
TMutation.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'put', [TPut, None], None),
 (
  2, TType.STRUCT, 'deleteSingle', [TDelete, None], None))
all_structs.append(TRowMutations)
TRowMutations.thrift_spec = (
 None,
 (
  1, TType.STRING, 'row', 'BINARY', None),
 (
  2, TType.LIST, 'mutations', (TType.STRUCT, [TMutation, None], False), None))
all_structs.append(THRegionInfo)
THRegionInfo.thrift_spec = (
 None,
 (
  1, TType.I64, 'regionId', None, None),
 (
  2, TType.STRING, 'tableName', 'BINARY', None),
 (
  3, TType.STRING, 'startKey', 'BINARY', None),
 (
  4, TType.STRING, 'endKey', 'BINARY', None),
 (
  5, TType.BOOL, 'offline', None, None),
 (
  6, TType.BOOL, 'split', None, None),
 (
  7, TType.I32, 'replicaId', None, None))
all_structs.append(TServerName)
TServerName.thrift_spec = (
 None,
 (
  1, TType.STRING, 'hostName', 'UTF8', None),
 (
  2, TType.I32, 'port', None, None),
 (
  3, TType.I64, 'startCode', None, None))
all_structs.append(THRegionLocation)
THRegionLocation.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'serverName', [TServerName, None], None),
 (
  2, TType.STRUCT, 'regionInfo', [THRegionInfo, None], None))
all_structs.append(TTableName)
TTableName.thrift_spec = (
 None,
 (
  1, TType.STRING, 'ns', 'BINARY', None),
 (
  2, TType.STRING, 'qualifier', 'BINARY', None))
all_structs.append(TColumnFamilyDescriptor)
TColumnFamilyDescriptor.thrift_spec = (
 None,
 (
  1, TType.STRING, 'name', 'BINARY', None),
 (
  2, TType.MAP, 'attributes', (TType.STRING, 'BINARY', TType.STRING, 'BINARY', False), None),
 (
  3, TType.MAP, 'configuration', (TType.STRING, 'UTF8', TType.STRING, 'UTF8', False), None),
 (
  4, TType.I32, 'blockSize', None, None),
 (
  5, TType.I32, 'bloomnFilterType', None, None),
 (
  6, TType.I32, 'compressionType', None, None),
 (
  7, TType.I16, 'dfsReplication', None, None),
 (
  8, TType.I32, 'dataBlockEncoding', None, None),
 (
  9, TType.I32, 'keepDeletedCells', None, None),
 (
  10, TType.I32, 'maxVersions', None, None),
 (
  11, TType.I32, 'minVersions', None, None),
 (
  12, TType.I32, 'scope', None, None),
 (
  13, TType.I32, 'timeToLive', None, None),
 (
  14, TType.BOOL, 'blockCacheEnabled', None, None),
 (
  15, TType.BOOL, 'cacheBloomsOnWrite', None, None),
 (
  16, TType.BOOL, 'cacheDataOnWrite', None, None),
 (
  17, TType.BOOL, 'cacheIndexesOnWrite', None, None),
 (
  18, TType.BOOL, 'compressTags', None, None),
 (
  19, TType.BOOL, 'evictBlocksOnClose', None, None),
 (
  20, TType.BOOL, 'inMemory', None, None))
all_structs.append(TTableDescriptor)
TTableDescriptor.thrift_spec = (
 None,
 (
  1, TType.STRUCT, 'tableName', [TTableName, None], None),
 (
  2, TType.LIST, 'columns', (TType.STRUCT, [TColumnFamilyDescriptor, None], False), None),
 (
  3, TType.MAP, 'attributes', (TType.STRING, 'BINARY', TType.STRING, 'BINARY', False), None),
 (
  4, TType.I32, 'durability', None, None))
all_structs.append(TNamespaceDescriptor)
TNamespaceDescriptor.thrift_spec = (
 None,
 (
  1, TType.STRING, 'name', 'UTF8', None),
 (
  2, TType.MAP, 'configuration', (TType.STRING, 'UTF8', TType.STRING, 'UTF8', False), None))
all_structs.append(TIOError)
TIOError.thrift_spec = (
 None,
 (
  1, TType.STRING, 'message', 'UTF8', None))
all_structs.append(TIllegalArgument)
TIllegalArgument.thrift_spec = (
 None,
 (
  1, TType.STRING, 'message', 'UTF8', None))
fix_spec(all_structs)
del all_structs