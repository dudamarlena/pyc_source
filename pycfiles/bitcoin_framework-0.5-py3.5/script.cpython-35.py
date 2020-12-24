# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitcoin/field/script.py
# Compiled at: 2017-07-08 11:42:23
# Size of source mod 2**32: 7897 bytes
"""
Defines fields that can appear in a script
"""
import math
from .model import Field
from .general import U2BLEInt, U4BLEInt
from .opcode import OP_PUSHDATA_MIN, OP_PUSHDATA_MAX, OP_PUSHDATA1, OP_PUSHDATA2, OP_PUSHDATA4, OP_PUSHDATA_MAX_BYTES
from .helper import bfh
from . import test

class ScriptData(Field):
    __doc__ = '\n    A script data field allows to include data in a script that has to be\n    pushed to the stack, that will automatically include the push data\n    operation code required so the data is correctly pushed into the stack.\n\n    Attributes:\n        _value (bytes|Field): saved value must be either a bytes object or a\n        Field object so that can be serialized\n    '

    @property
    def serialized_value(self):
        """ Returns the value serialized as a bytes object """
        if isinstance(self._value, bytes):
            return self._value
        return self._value.serialize()

    def _push_data_opcodes(self):
        """
        Calculates the pushdata opcodes needed to push the data to the stack
        and returns them as bytes

        Returns:
            bytes: serialized opcodes to push the data of the field into stack
        """
        serialized_data_length = len(self.serialized_value)
        bytes_length_size = math.ceil(serialized_data_length.bit_length() / 8)
        pushdata_opcodes = None
        if serialized_data_length >= OP_PUSHDATA_MIN and serialized_data_length <= OP_PUSHDATA_MAX:
            pushdata_opcodes = bytes([serialized_data_length])
        else:
            if bytes_length_size < OP_PUSHDATA_MAX_BYTES:
                pushdata_opcode = None
                pushdata_size = None
                if bytes_length_size == 1:
                    pushdata_opcode = OP_PUSHDATA1.serialize()
                    pushdata_size = bytes([serialized_data_length])
                else:
                    if bytes_length_size == 2:
                        pushdata_opcode = OP_PUSHDATA2.serialize()
                        pushdata_size = U2BLEInt(serialized_data_length).serialize()
                    else:
                        if bytes_length_size <= 4:
                            pushdata_opcode = OP_PUSHDATA4.serialize()
                            pushdata_size = U4BLEInt(serialized_data_length).serialize()
                        else:
                            raise ValueError('Length size does not have an opcode to\n                                    allow it to be pushed into the stack\n                                    and fit')
                pushdata_opcodes = pushdata_opcode + pushdata_size
            else:
                raise ValueError('Data is too big to be pushed into the stack. No\n            opcode exists to push that')
        return pushdata_opcodes

    def serialize(self):
        """
        Serializes the data saved, including the operation to push the
        serialized data into the stack depending on the serialized data length

        The opcode to push the data depends on the data length:
        If data length in bytes is
            >= OP_PUSHDATA_MIN (0x01) and <= OP_PUSHDATA_MAX (0x4b)
        then serialization is:
            <number of data bytes to push><data to push>
        else:
            Calculate how much bytes does the size of the data to be pushed
            occupies (if we want to push 65535 bytes of data, then we require
            two bytes to express 65535 bytes -> ceil(log_2(65535)/8) = 2)

            Knowing the bytes that the length of the data takes to be expressed
            we have to use OP_PUSHDATA1,2,4 depending if the bytes of data to
            be pushed can be represented in 1, 2 or 4 bytes.

            After the opcode OP_PUSHDATA we've chosen, we add the size in bytes
            of the data as a little-endian unsigned integer
            https://en.bitcoin.it/wiki/Script
            http://bitcoin.stackexchange.com/questions/2285/script-op-pushdatas

        Returns:
            bytes: array of bytes so the data stored can be pushed into the
            stack, adding the opcodes necessary for that to happen
        """
        return self._push_data_opcodes() + self.serialized_value

    @classmethod
    def deserialize(cls, data):
        """
        Given a bytes object that is known to contain as first byte a push data
        operation, decodes the operation and extracts the data from the bytes
        object, storing it as a bytes object in the value of the field of a new
        object

        The length of the bytes object can be different from the length of the
        actual data. The method will just save the data that the opcode and
        opcode data if it's the case says. The rest of data will be ignored

        Raise:
            ValueError: no data push opcode is found
        """
        data_size = 0
        opcode = data[0]
        offset = 1
        if opcode >= OP_PUSHDATA_MIN and opcode <= OP_PUSHDATA_MAX:
            data_size = opcode
        else:
            if opcode == OP_PUSHDATA1.value:
                data_size = data[offset]
                offset += 1
            else:
                if opcode == OP_PUSHDATA2.value:
                    data_size = U2BLEInt().deserialize(data[offset:offset + 2]).value
                    offset += 2
                else:
                    if opcode == OP_PUSHDATA4.value:
                        data_size = U4BLEInt().deserialize(data[offset:offset + 4]).value
                        offset += 4
                    else:
                        raise ValueError('Data to deserialize has not an opcode to\n                                 push data to the stack')
        return cls(data[offset:data_size + offset])

    def __str__(self):
        """ Returns the field as a printable string """
        pushdata = '[%s:%s(size=%d)] ' % (
         self._push_data_opcodes().hex(), 'OP_PUSHDATA',
         len(self.serialized_value))
        data = '[%s:DATA()]' % self.serialized_value.hex()
        return pushdata + data


class ScriptNum(Field):
    __doc__ = '\n    Defines a field containing an integetr number that can be used inside a\n    StackDataField to perform script operations\n\n    According to:\n    https://github.com/bitcoin/bitcoin/blob/master/src/script/script.h#L353-L371\n\n    Its serialization is a little-endian signed integer with the minimum bytes\n    possible. The signed / unsigned meaning is given by the first bit (sign,\n    magnitude coding)\n    '

    def serialize(self):
        bit_length = self._value.bit_length()
        byte_length = math.ceil(bit_length / 8)
        value_bytes = self._value.to_bytes(byte_length, 'little')
        if self._value < 0:
            if bit_length >= byte_length * 8:
                self._value = '\x00' + self._value
            self._value[0] = self._value[0] & 128
            raise NotImplementedError('pending to test')
        return value_bytes


if __name__ == '__main__':
    CASES = [
     (
      bfh('f0f1f2f3'), bfh('04f0f1f2f3'), ScriptData),
     (
      bfh('01' * 255), OP_PUSHDATA1.serialize() + bfh('ff' + '01' * 255),
      ScriptData),
     (
      bfh('02' * 65535), OP_PUSHDATA2.serialize() + bfh('ffff' + '02' * 65535),
      ScriptData),
     (
      bfh('04' * 16777215),
      OP_PUSHDATA4.serialize() + bfh('ffffff00' + '04' * 16777215),
      ScriptData)]
    print('Starting serialization test')
    for case in CASES:
        print('-> Testing', case[2].__name__, 'class.')
        print('      ', end='')
        test.serialization(*case)
        print('      ', end='')
        test.deserialization(*case)

    print('Tests passed')