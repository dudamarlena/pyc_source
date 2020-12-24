# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aiogcd/connector/buffer.py
# Compiled at: 2019-09-11 07:21:09
# Size of source mod 2**32: 1418 bytes
__doc__ = 'buffer.py\n\nCreated on: May 19, 2017\n    Author: Jeroen van der Heijden <jeroen@transceptor.technology>\n'
import array

class BufferEncodeError(Exception):
    pass


class BufferDecodeError(Exception):
    pass


class Buffer(array.array):

    def __new__(cls, *args):
        return super().__new__(cls, 'B')

    def add_var_int32(self, val):
        if val & 127 == val:
            self.append(val)
            return
        if val >= 2147483648 or val < -2147483648:
            raise BufferEncodeError('int32 too big')
        if val < 0:
            val += 18446744073709551616
        while 1:
            bits = val & 127
            val >>= 7
            if val:
                bits |= 128
            self.append(bits)
            if not val:
                break

    def add_var_int64(self, val):
        if val >= 9223372036854775808 or val < -9223372036854775808:
            raise BufferEncodeError('int64 too big')
        if val < 0:
            val += 18446744073709551616
        while 1:
            bits = val & 127
            val >>= 7
            if val:
                bits |= 128
            self.append(bits)
            if not val:
                break

    def add_prefixed_string(self, val):
        assert isinstance(val, str), 'Expecting a str value but got {}'.format(type(val))
        self.add_var_int32(len(val))
        self.fromstring(val)