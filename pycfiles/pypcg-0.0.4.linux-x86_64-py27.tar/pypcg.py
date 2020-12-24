# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/pypcg.py
# Compiled at: 2015-11-21 14:17:50
from cffi import FFI
from random import SystemRandom, Random
from os.path import join, dirname, abspath
__all__ = [
 'PCG32']
ffi = FFI()
VERSION = '0_0_1'
PCG_VERSION = '0_94'

def makeModuleName():
    return 'pcg_c_' + VERSION + '_' + PCG_VERSION


header = '\nstruct pcg_state_setseq_64 {    // Internals are *Private*.\n    uint64_t state;             // RNG state.  All values are possible.\n    uint64_t inc;               // Controls which RNG sequence (stream) is\n                                // selected. Must *always* be odd.\n};\ntypedef struct pcg_state_setseq_64 pcg32_random_t;\n\n// pcg32_srandom(initstate, initseq)\n// pcg32_srandom_r(rng, initstate, initseq):\n//     Seed the rng.  Specified in two parts, state initializer and a\n//     sequence selection constant (a.k.a. stream id)\n\nvoid pcg32_srandom(uint64_t initstate, uint64_t initseq);\nvoid pcg32_srandom_r(pcg32_random_t* rng, uint64_t initstate,\n                     uint64_t initseq);\n\n// pcg32_random()\n// pcg32_random_r(rng)\n//     Generate a uniformly distributed 32-bit random number\n\nuint32_t pcg32_random(void);\nuint32_t pcg32_random_r(pcg32_random_t* rng);\n\n// pcg32_boundedrand(bound):\n// pcg32_boundedrand_r(rng, bound):\n//     Generate a uniformly distributed number, r, where 0 <= r < bound\n\nuint32_t pcg32_boundedrand(uint32_t bound);\nuint32_t pcg32_boundedrand_r(pcg32_random_t* rng, uint32_t bound);\n'
ffi.cdef(header)
with open(join(dirname(abspath(__file__)), 'pcg_basic', 'pcg_basic.c')) as (source):
    c_interface = ffi.verify(source.read(), include_dirs=[
     join(dirname(abspath(__file__)), 'pcg_basic')], modulename=makeModuleName())
DEFAULT_SEQUENCE = 184628983

class PCG32(Random):
    """
  An object that wraps a pcg32 engine from the c_pcg_basic library
  """

    def __init__(self, state=None, seq=DEFAULT_SEQUENCE):
        """
    Initialize a new PCGRandom engine. If no seed is specified use urandom and
    if no sequene is specified use an arbitrary sequece
    """
        self._rng_state = ffi.new('pcg32_random_t*')
        if state == None:
            system_random = SystemRandom()
            state = system_random.getrandbits(64)
        c_interface.pcg32_srandom_r(self._rng_state, state, seq)
        return

    def random(self):
        return float(c_interface.pcg32_random_r(self._rng_state)) / float(4294967295)

    def boundedrand_r(self, bound):
        return int(c_interface.pcg32_boundedrand_r(self._rng_state, bound))

    def seed(self, a=None, seq=DEFAULT_SEQUENCE, version=2):
        if type(a) != int:
            a = hash(a)
        c_interface.pcg32_srandom_r(self._rng_state, a, seq)

    def getstate(self):
        return self._rng_state

    def setstate(self):
        return self._rng_state

    def jumpahead(self, n):
        raise NotImplementedError

    def getrandbits(self, k):
        num_rand = k // 32
        num_extra = k % 32
        out = 0
        i = -1
        for i in range(num_rand):
            out |= c_interface.pcg32_random_r(self._rng_state) << 32 * i

        out |= (c_interface.pcg32_random_r(self._rng_state) & 2 ** num_extra - 1) << 32 * (i + 1)
        return out