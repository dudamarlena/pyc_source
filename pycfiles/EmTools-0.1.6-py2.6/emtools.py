# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/emtools.py
# Compiled at: 2011-09-19 11:19:21
import numpy

class ReadOnlyMemoryError(Exception):
    pass


class MemoryNotMappedError(Exception):
    pass


class Register(object):

    def __init__(self, width=8):
        self.value = 0
        self.width = width
        self.mask = (1 << width) - 1

    def set(self, value):
        """Sets the value of the register
    
    Args:
      `value` (int):
        The value to set.
    """
        self.value = value & self.mask

    def get(self):
        """Returns the value of the register
    
    Returns:
      The value of the register.
    """
        return self.value

    def inc(self):
        self.set(self.get() + 1)

    def dec(self):
        self.set(self.get() - 1)

    def setbit(self, bit, value):
        if value:
            self.set(self.get() | 1 << bit)
        else:
            self.set(self.get() & ~(1 << bit))

    def getbit(self, bit):
        """Gets a bit from the register.
    
    Args:
      `bit` (int):
        The bit to get. For a register of 8 bits, 0 is the least
        significant bit and 7 is the most significant bit.
    
    Returns:
      The bit specified by the argument, as an integer.
    """
        return self.get() >> bit & 1


class PairedRegister(Register):

    def __init__(self, high, low):
        self.high = high
        self.low = low

    def set(self, value):
        self.high.set(value >> self.low.width)
        self.low.set(value)

    def get(self):
        return (self.high.get() << self.low.width) + self.low.get()


class Stack(object):

    def __init__(self, size, width=8):
        self.size = size
        self.width = width
        self.data = []
        self.mask = (1 << width) - 1

    def __str__(self):
        return (', ').join(map(lambda n: '%d (0x%02X)' % (n, n), self.data))

    def push(self, value):
        if len(self.data) == self.size:
            raise CPUError(E_SOU)
        self.data.append(value & self.mask)

    def pop(self):
        if len(self.data) == 0:
            raise CPUError(E_SOU)
        return self.data.pop(-1)

    def get(self, n=0):
        return self.data[(-(n + 1))]


class ExtendedMemoryBase(object):
    """Defines memory utility methods"""

    def _init(self):
        self.hooks = {}

    def get_word_le16(self, addr):
        return self.get(addr) + (self.get(addr + 1) << 8)

    def set_word_le16(self, addr, value):
        self.set(addr, value)
        self.set(addr + 1, value >> 8)

    def get_word_be16(self, addr):
        return (self.get(addr) << 8) + self.get(addr + 1)

    def set_word_be16(self, addr, value):
        self.set(addr, value >> 8)
        self.set(addr + 1, value)

    def attach_hook(self, addr, reader, writer):
        self.hooks[addr] = (
         reader, writer)

    def remove_hooks(self, addr):
        del self.hooks[addr]

    def get(self, addr):
        if addr in self.hooks and self.hooks[addr][0] is not None:
            return self.hooks[addr][0]()
        else:
            return self._get(addr)
            return

    def set(self, addr, value):
        if addr in self.hooks and self.hooks[addr][1] is not None:
            self.hooks[addr][1](value)
        else:
            self._set(addr, value)
        return

    def __getitem__(self, addr):
        return self.get(addr)

    def __setitem__(self, addr, value):
        self.set(addr, value)


class ROMemory(ExtendedMemoryBase):

    def __init__(self, size):
        self._init()
        self.size = size
        self.clear()

    def clear(self):
        self.data = numpy.zeros(shape=(self.size,), dtype=numpy.uint8)

    def load(self, data, start=0):
        end = start + len(data)
        self.data[start:end] = map(ord, data)

    def dump(self):
        return self.data

    def _get(self, addr):
        return self.data[addr]

    def _set(self, addr, value):
        raise ReadOnlyMemoryError


class RWMemory(ROMemory):

    def _set(self, addr, value):
        self.data[addr] = value


class MemoryMap(ExtendedMemoryBase):

    def __init__(self):
        self._init()
        self.maps = {}

    def map(self, start, end, rw=True):
        cls = None
        if rw:
            cls = RWMemory
        else:
            cls = ROMemory
        size = end - start
        mem = cls(size)
        self.maps[start] = mem
        return mem

    def get_map(self, addr):
        offsets = self.maps.keys()
        minoffset = None
        for offset in sorted(offsets):
            if offset > addr:
                break
            minoffset = offset

        if minoffset is None:
            raise MemoryNotMappedError('Trying to access memory at 0x%08X' % addr)
        map = self.maps[minoffset]
        if minoffset + map.size < addr:
            raise MemoryNotMappedError('Trying to access memory at 0x%08X' % addr)
        return (map, addr - minoffset)

    def clear(self):
        for map in self.maps.values():
            map.clear()

    def _get(self, addr):
        (map, addr) = self.get_map(addr)
        return map.get(addr)

    def _set(self, addr, value):
        (map, addr) = self.get_map(addr)
        map.set(addr, value)