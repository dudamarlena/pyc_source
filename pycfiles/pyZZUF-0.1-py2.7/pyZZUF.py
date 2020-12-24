# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyZZUF/pyZZUF.py
# Compiled at: 2014-11-03 20:09:47
__author__ = '@nezlooy'
__version__ = '0.1'
__version_info__ = (0, 1, 0, 0)
__status__ = 'Production'
from array import array
from random import randint
from ctypes import c_double
ZZUF_MAGIC0 = 305419896
ZZUF_MAGIC1 = 871007479
ZZUF_MAGIC2 = 2017182495
ZZUF_MAGIC3 = 2606605051
CHUNKBYTES = 1024
MAX_UINT32 = 4294967295
DEFAULT_OFFSET = 0
EOF = None
DEFAULT_SEED = 0
DEFAULT_CTX = 1
DEFAULT_RATIO = 0.004
DEFAULT_RATIO_STEP = 0.001
MIN_RATIO = 1e-09
MAX_RATIO = 5.0
C_DOUBLE_NDIGITS = 9
FUZZ_MODE_XOR = 0
FUZZ_MODE_SET = 1
FUZZ_MODE_UNSET = 2

def uint(v, ring=4294967295):
    return (v if isinstance(v, int) else int(v)) & ring


def uint8(v):
    return uint(v, 255)


def uint16(v):
    return uint(v, 65535)


def uint32(v):
    return uint(v, 4294967295)


def double(f, ndigits=C_DOUBLE_NDIGITS):
    return round(c_double(f).value, ndigits)


class pyZZUFArray(array):
    _seed, _ratio, _iter = (None, None, None)

    def __str__(self):
        return self.tostring()

    def __add__(self, other):
        return self.__str__() + other

    def get_state(self):
        return (
         self._seed, self._ratio, self._iter)

    def set_state(self, _seed, _ratio, _iter):
        self._seed, self._ratio, self._iter = _seed, _ratio, _iter
        return self


class pyZZUF(object):
    _seed = DEFAULT_SEED
    _ratio = DEFAULT_RATIO
    _offset = DEFAULT_OFFSET
    _fuzz_bytes = None
    _protected = None
    _refused = None
    _permitted = None
    _fuzz_mode = FUZZ_MODE_XOR
    _pos = DEFAULT_OFFSET
    _ctx = DEFAULT_CTX
    _iter = 0

    def __init__(self, buf, seed=None, ratio=None, offset=None):
        super(pyZZUF, self).__init__()
        self.set_buffer(buf)
        if seed is not None:
            self.set_seed(seed)
        if ratio is not None:
            self.set_ratio(ratio)
        if offset is not None:
            self.set_offset(offset)
        return

    def set_buffer(self, buf):
        self._buf = buf if isinstance(buf, array) else array('B', buf)
        self._buf_length = len(buf)

    def set_seed(self, seed):
        if not isinstance(seed, int):
            raise TypeError('<seed> must be int')
        self._seed = uint32(seed)

    def set_ratio(self, ratio):
        if not isinstance(ratio, float):
            raise TypeError('<ratio> must be float')
        ratio = double(ratio)
        if ratio > MAX_RATIO:
            ratio = MAX_RATIO
        elif ratio < MIN_RATIO:
            ratio = MIN_RATIO
        self._ratio = ratio

    def set_fuzz_mode(self, mode):
        if mode not in [FUZZ_MODE_XOR, FUZZ_MODE_SET, FUZZ_MODE_UNSET]:
            raise TypeError('bad <mode> (must be one of FUZZ_MODE_XOR, FUZZ_MODE_SET, FUZZ_MODE_UNSET)')
        self._fuzz_mode = mode

    def set_offset(self, offset):
        if not isinstance(offset, int):
            raise TypeError('<offset> must be int')
        self._offset = uint32(offset)

    def set_fuzz_bytes(self, fbytes):
        if not isinstance(fbytes, list):
            raise TypeError('<fbytes> must be list')
        self._fuzz_bytes = []
        for _zz_r in fbytes:
            if isinstance(_zz_r, list) and len(_zz_r) == 2:
                start, stop = _zz_r
                if isinstance(start, int):
                    self._fuzz_bytes.append((start, self._buf_length if stop is None else stop))
            elif isinstance(_zz_r, int):
                self._fuzz_bytes.append((_zz_r, _zz_r))
            else:
                raise TypeError('<fbytes> must be list')

        return

    def set_protected(self, protected_bytes, append=False):
        self._zz_arrbytes(protected_bytes, 'protected_bytes', '_protected', append)

    def set_refused(self, refused_bytes, append=False):
        self._zz_arrbytes(refused_bytes, 'refused_bytes', '_refused', append)

    def set_permitted(self, permitted_bytes, append=False):
        self._zz_arrbytes(permitted_bytes, 'permitted_bytes', '_permitted', append)

    def _zz_arrbytes(self, arr, attr_name, _attr, append):
        if type(arr) not in [list, str]:
            raise TypeError('<%s> must be list of int or str' % attr_name)
        if not append or getattr(self, _attr) is None:
            self.__dict__[_attr] = array('B')
        self.__dict__[_attr].fromlist(arr) if isinstance(arr, list) else self.__dict__[_attr].fromstring(arr)
        return

    def _zz_isinrange(self, index):
        for start, stop in self._fuzz_bytes:
            if index >= start and (start == stop or index < stop):
                return True

        return False

    def _zz_srand(self, seed):
        self._ctx = seed ^ ZZUF_MAGIC0

    def _zz_rand(self, maxv):
        hi, lo = self._ctx / 12773, self._ctx % 12773
        x = 16807 * lo - 2836 * hi
        if x <= 0:
            x += 2147483647
        self._ctx = x
        return uint32(self._ctx % maxv)

    def mutate(self):
        i = 0
        for _ in xrange(0, self._buf_length, CHUNKBYTES):
            chunkseed = i
            chunkseed ^= ZZUF_MAGIC2
            chunkseed += uint32(self._ratio * ZZUF_MAGIC1)
            chunkseed ^= self._seed
            chunkseed += uint32(i * ZZUF_MAGIC3)
            chunkseed = uint32(chunkseed)
            self._zz_srand(chunkseed)
            fuzz_data = bytearray(CHUNKBYTES)
            loop_bits = uint32((self._ratio * (8 * CHUNKBYTES) * 1000000.0 + self._zz_rand(1000000)) / 1000000.0)
            for x in xrange(loop_bits):
                idx = self._zz_rand(CHUNKBYTES)
                bit = 1 << self._zz_rand(8)
                fuzz_data[idx] ^= bit

            start = i * CHUNKBYTES if i * CHUNKBYTES > self._pos else self._pos
            stop = (i + 1) * CHUNKBYTES if (i + 1) * CHUNKBYTES < self._pos + self._buf_length else self._pos + self._buf_length
            for j in xrange(start, stop):
                if self._fuzz_bytes is not None and not self._zz_isinrange(j):
                    continue
                elif self._offset > 0 and j < self._offset:
                    continue
                byte = self._buf[j]
                if self._protected is not None and byte in self._protected:
                    continue
                fuzz_byte = fuzz_data[(j % CHUNKBYTES)]
                if not fuzz_byte:
                    continue
                if self._fuzz_mode == FUZZ_MODE_SET:
                    byte |= fuzz_byte
                elif self._fuzz_mode == FUZZ_MODE_UNSET:
                    byte &= ~fuzz_byte
                else:
                    byte ^= fuzz_byte
                if self._permitted is not None and byte not in self._permitted:
                    continue
                if self._refused is not None and byte in self._refused:
                    continue
                self._buf[j] = byte

            i += 1

        return pyZZUFArray('B', self._buf).set_state(self._seed, self._ratio, self._iter)

    def _zz_frange(self, start, stop, step):
        while start <= stop:
            next_state = yield start
            start = double(start + step)
            if next_state:
                start = double(next_state)

    def mutagen(self, start=DEFAULT_RATIO, stop=MAX_RATIO, step=DEFAULT_RATIO_STEP, inheritance=False, rand_seed=False):
        self._iter = 0
        start, stop, step = map(lambda f: double(f), [start, stop, step])
        buf = self._buf
        while start <= stop:
            if not inheritance:
                self.set_buffer(buf[:])
            self.set_seed(randint(0, MAX_UINT32) if rand_seed else self._iter)
            self.set_ratio(start)
            next_state = yield self.mutate()
            start = double(start + step)
            self._iter += 1
            if next_state:
                self._iter, start = next_state