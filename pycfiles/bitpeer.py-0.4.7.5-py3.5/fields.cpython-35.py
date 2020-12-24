# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitpeer/fields.py
# Compiled at: 2015-11-27 11:52:45
# Size of source mod 2**32: 10865 bytes
from .exceptions import NodeDisconnectException
from io import BytesIO
import struct, time, random, socket
PROTOCOL_VERSION = 70002
SERVICES = {'NODE_NETWORK': 1}
INVENTORY_TYPE = {'ERROR': 0, 
 'MSG_TX': 1, 
 'MSG_BLOCK': 2}

class Field(object):
    __doc__ = 'Base class for the Fields. This class only implements\n    the counter to keep the order of the fields on the\n    serializer classes.'
    counter = 0

    def __init__(self):
        self.count = Field.counter
        Field.counter += 1

    def parse(self, value):
        """This method should be implemented to parse the value
        parameter into the field internal representation.

        :param value: value to be parsed
        """
        raise NotImplemented

    def deserialize(self, stream):
        """This method must read the stream data and then
        deserialize and return the deserialized content.

        :returns: the deserialized content
        :param stream: stream of data to read
        """
        raise NotImplemented

    def serialize(self):
        """Serialize the internal representation and return
        the serialized data.

        :returns: the serialized data
        """
        raise NotImplemented

    def __repr__(self):
        return '<%s [%r]>' % (self.__class__.__name__,
         repr(self.value))

    def __str__(self):
        return str(self.value)


class PrimaryField(Field):
    __doc__ = 'This is a base class for all fields that has only\n    one value and their value can be represented by\n    a Python struct datatype.\n\n    Example of use::\n\n        class UInt32LEField(PrimaryField):\n            datatype = "<I"\n    '

    def parse(self, value):
        """This method will set the internal value to the
        specified value.

        :param value: the value to be set
        """
        self.value = value

    def deserialize(self, stream):
        """Deserialize the stream using the struct data type
        specified.

        :param stream: the data stream
        """
        data_size = struct.calcsize(self.datatype)
        data = stream.read(data_size)
        return struct.unpack(self.datatype, data)[0]

    def serialize(self):
        """Serialize the internal data and then return the
        serialized data."""
        data = struct.pack(self.datatype, self.value)
        return data


class Int32LEField(PrimaryField):
    __doc__ = '32-bit little-endian integer field.'
    datatype = '<i'


class UInt32LEField(PrimaryField):
    __doc__ = '32-bit little-endian unsigned integer field.'
    datatype = '<I'


class Int64LEField(PrimaryField):
    __doc__ = '64-bit little-endian integer field.'
    datatype = '<q'


class UInt64LEField(PrimaryField):
    __doc__ = '64-bit little-endian unsigned integer field.'
    datatype = '<Q'


class Int16LEField(PrimaryField):
    __doc__ = '16-bit little-endian integer field.'
    datatype = '<h'


class UInt16LEField(PrimaryField):
    __doc__ = '16-bit little-endian unsigned integer field.'
    datatype = '<H'


class UInt16BEField(PrimaryField):
    __doc__ = '16-bit big-endian unsigned integer field.'
    datatype = '>H'


class FixedStringField(Field):
    __doc__ = 'A fixed length string field.\n\n    Example of use::\n\n        class MessageHeaderSerializer(Serializer):\n            model_class = MessageHeader\n            magic = fields.UInt32LEField()\n            command = fields.FixedStringField(12)\n            length = fields.UInt32LEField()\n            checksum = fields.UInt32LEField()\n    '

    def __init__(self, length):
        super(FixedStringField, self).__init__()
        self.length = length

    def parse(self, value):
        self.value = value[:self.length]

    def deserialize(self, stream):
        data = stream.read(self.length)
        return data[:(data + b'\x00').index(b'\x00')].decode('utf-8')

    def serialize(self):
        bin_data = BytesIO()
        bin_data.write(struct.pack('12s', self.value.encode('utf-8')))
        return bin_data.getvalue()


class NestedField(Field):
    __doc__ = 'A field used to nest another serializer.\n\n    Example of use::\n\n       class TxInSerializer(Serializer):\n           model_class = TxIn\n           previous_output = fields.NestedField(OutPointSerializer)\n           signature_script = fields.VariableStringField()\n           sequence = fields.UInt32LEField()\n    '

    def __init__(self, serializer_class):
        super(NestedField, self).__init__()
        self.serializer_class = serializer_class
        self.serializer = self.serializer_class()

    def parse(self, value):
        self.value = value

    def deserialize(self, stream):
        return self.serializer.deserialize(stream)

    def serialize(self):
        return self.serializer.serialize(self.value)


class ListField(Field):
    __doc__ = 'A field used to serialize/deserialize a list of serializers.\n\n    Example of use::\n\n        class TxSerializer(Serializer):\n            model_class = Tx\n            version = fields.UInt32LEField()\n            tx_in = fields.ListField(TxInSerializer)\n            tx_out = fields.ListField(TxOutSerializer)\n            lock_time = fields.UInt32LEField()\n    '

    def __init__(self, serializer_class):
        super(ListField, self).__init__()
        self.serializer_class = serializer_class
        self.var_int = VariableIntegerField()

    def parse(self, value):
        self.value = value

    def serialize(self):
        bin_data = BytesIO()
        self.var_int.parse(len(self))
        bin_data.write(self.var_int.serialize())
        serializer = self.serializer_class()
        for item in self:
            bin_data.write(serializer.serialize(item))

        return bin_data.getvalue()

    def deserialize(self, stream):
        count = self.var_int.deserialize(stream)
        items = []
        serializer = self.serializer_class()
        for i in range(count):
            data = serializer.deserialize(stream)
            items.append(data)

        return items

    def __iter__(self):
        return iter(self.value)

    def __len__(self):
        return len(self.value)


class ListField(Field):
    __doc__ = 'A field used to serialize/deserialize a list of serializers.\n\n    Example of use::\n\n        class TxSerializer(Serializer):\n            model_class = Tx\n            version = fields.UInt32LEField()\n            tx_in = fields.ListField(TxInSerializer)\n            tx_out = fields.ListField(TxOutSerializer)\n            lock_time = fields.UInt32LEField()\n    '

    def __init__(self, serializer_class):
        super(ListField, self).__init__()
        self.serializer_class = serializer_class
        self.var_int = VariableIntegerField()

    def parse(self, value):
        self.value = value

    def serialize(self):
        bin_data = BytesIO()
        self.var_int.parse(len(self))
        bin_data.write(self.var_int.serialize())
        serializer = self.serializer_class()
        for item in self:
            bin_data.write(serializer.serialize(item))

        return bin_data.getvalue()

    def deserialize(self, stream):
        count = self.var_int.deserialize(stream)
        items = []
        serializer = self.serializer_class()
        for i in range(count):
            data = serializer.deserialize(stream)
            items.append(data)

        return items

    def __iter__(self):
        return iter(self.value)

    def __len__(self):
        return len(self.value)


class IPv4AddressField(Field):
    __doc__ = 'An IPv4 address field without timestamp and reserved IPv6 space.'
    reserved = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff'

    def parse(self, value):
        self.value = value

    def deserialize(self, stream):
        unused_reserved = stream.read(12)
        addr = stream.read(4)
        return socket.inet_ntoa(addr)

    def serialize(self):
        bin_data = BytesIO()
        bin_data.write(self.reserved)
        bin_data.write(socket.inet_aton(self.value))
        return bin_data.getvalue()


class VariableIntegerField(Field):
    __doc__ = 'A variable size integer field.'

    def parse(self, value):
        self.value = int(value)

    def deserialize(self, stream):
        int_id_raw = stream.read(struct.calcsize('<B'))
        int_id = struct.unpack('<B', int_id_raw)[0]
        if int_id == 253:
            data = stream.read(2)
            int_id = struct.unpack('<H', data)[0]
        else:
            if int_id == 254:
                data = stream.read(4)
                int_id = struct.unpack('<I', data)[0]
            elif int_id == 255:
                data = stream.read(8)
                int_id = struct.unpack('<Q', data)[0]
        return int_id

    def serialize(self):
        if self.value < 253:
            return struct.pack('B', self.value)
        if self.value <= 65535:
            return b'\xfd' + struct.pack('<H', self.value)
        if self.value <= 4294967295:
            return b'\xfe' + struct.pack('<I', self.value)
        return b'\xff' + struct.pack('<Q', self.value)


class VariableStringField(Field):
    __doc__ = 'A variable length string field.'

    def __init__(self):
        super(VariableStringField, self).__init__()
        self.var_int = VariableIntegerField()

    def parse(self, value):
        self.value = str(value)

    def deserialize(self, stream):
        string_length = self.var_int.deserialize(stream)
        string_data = stream.read(string_length)
        return string_data

    def serialize(self):
        self.var_int.parse(len(self))
        bin_data = BytesIO()
        bin_data.write(self.var_int.serialize())
        bin_data.write(bytes(self.value, 'utf-8'))
        return bin_data.getvalue()

    def __len__(self):
        return len(self.value)


class Hash(Field):
    __doc__ = 'A hash type field.'
    datatype = '<I'

    def parse(self, value):
        self.value = value

    def deserialize(self, stream):
        data_size = struct.calcsize(self.datatype)
        intvalue = 0
        for i in range(8):
            data = stream.read(data_size)
            val = struct.unpack(self.datatype, data)[0]
            intvalue += val << i * 32

        return intvalue

    def serialize(self):
        hash_ = self.value
        bin_data = BytesIO()
        for i in range(8):
            pack_data = struct.pack(self.datatype, hash_ & 4294967295)
            bin_data.write(pack_data)
            hash_ >>= 32

        return bin_data.getvalue()


class BlockLocator(Field):
    __doc__ = 'A block locator type used for getblocks and getheaders'
    datatype = '<I'

    def parse(self, values):
        self.values = values

    def serialize(self):
        bin_data = BytesIO()
        for hash_ in self.values:
            for i in range(8):
                pack_data = struct.pack(self.datatype, hash_ & 4294967295)
                bin_data.write(pack_data)
                hash_ >>= 32

        return bin_data.getvalue()