# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/scjurgen/Projects/hpd-20/hpd20/memoryops.py
# Compiled at: 2017-01-09 16:42:15


class MemoryOp:

    @staticmethod
    def get_int8(memory_block, index):
        value = memory_block[index]
        if value > 127:
            return -(256 - value)
        return value

    @staticmethod
    def set_int8(memory_block, index, value):
        memory_block[index] = value & 255

    @staticmethod
    def get_unsigned_int8(memory_block, index):
        value = memory_block[index]
        return value

    @staticmethod
    def get_int16(memory_block, index):
        value = memory_block[index] * 256 + memory_block[(index + 1)]
        if value > 32767:
            return -(65536 - value)
        return value

    @staticmethod
    def set_int16(memory_block, index, value):
        memory_block[index] = value >> 8 & 255
        memory_block[index + 1] = value & 255

    @staticmethod
    def get_unsigned_int16(memory_block, index):
        value = memory_block[index] * 256 + memory_block[(index + 1)]
        return value

    @staticmethod
    def set_unsigned_int16(memory_block, index, value):
        memory_block[index] = value >> 8 & 255
        memory_block[index + 1] = value & 255

    @staticmethod
    def get_string(memory_block, index, size):
        return str(memory_block[index:index + size])

    @staticmethod
    def set_string(memory_block, index, string):
        memory_block[index:(index + len(string))] = string