# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-armv7l/egg/pycuda/curandom.py
# Compiled at: 2015-06-16 13:16:13
from __future__ import division
from __future__ import absolute_import
import numpy as np, pycuda.compiler, pycuda.driver as drv, pycuda.gpuarray as array
from pytools import memoize_method
import six
md5_code = '\n/*\n **********************************************************************\n ** Copyright (C) 1990, RSA Data Security, Inc. All rights reserved. **\n **                                                                  **\n ** License to copy and use this software is granted provided that   **\n ** it is identified as the "RSA Data Security, Inc. MD5 Message     **\n ** Digest Algorithm" in all material mentioning or referencing this **\n ** software or this function.                                       **\n **                                                                  **\n ** License is also granted to make and use derivative works         **\n ** provided that such works are identified as "derived from the RSA **\n ** Data Security, Inc. MD5 Message Digest Algorithm" in all         **\n ** material mentioning or referencing the derived work.             **\n **                                                                  **\n ** RSA Data Security, Inc. makes no representations concerning      **\n ** either the merchantability of this software or the suitability   **\n ** of this software for any particular purpose.  It is provided "as **\n ** is" without express or implied warranty of any kind.             **\n **                                                                  **\n ** These notices must be retained in any copies of any part of this **\n ** documentation and/or software.                                   **\n **********************************************************************\n */\n\n/* F, G and H are basic MD5 functions: selection, majority, parity */\n#define F(x, y, z) (((x) & (y)) | ((~x) & (z)))\n#define G(x, y, z) (((x) & (z)) | ((y) & (~z)))\n#define H(x, y, z) ((x) ^ (y) ^ (z))\n#define I(x, y, z) ((y) ^ ((x) | (~z)))\n\n/* ROTATE_LEFT rotates x left n bits */\n#define ROTATE_LEFT(x, n) (((x) << (n)) | ((x) >> (32-(n))))\n\n/* FF, GG, HH, and II transformations for rounds 1, 2, 3, and 4 */\n/* Rotation is separate from addition to prevent recomputation */\n#define FF(a, b, c, d, x, s, ac)   {(a) += F ((b), (c), (d)) + (x) + (ac);    (a) = ROTATE_LEFT ((a), (s));    (a) += (b);   }\n#define GG(a, b, c, d, x, s, ac)   {(a) += G ((b), (c), (d)) + (x) + (ac);    (a) = ROTATE_LEFT ((a), (s));    (a) += (b);   }\n#define HH(a, b, c, d, x, s, ac)   {(a) += H ((b), (c), (d)) + (x) + (ac);    (a) = ROTATE_LEFT ((a), (s));    (a) += (b);   }\n#define II(a, b, c, d, x, s, ac)   {(a) += I ((b), (c), (d)) + (x) + (ac);    (a) = ROTATE_LEFT ((a), (s));    (a) += (b);   }\n\n#define X0 threadIdx.x\n#define X1 threadIdx.y\n#define X2 threadIdx.z\n#define X3 blockIdx.x\n#define X4 blockIdx.y\n#define X5 blockIdx.z\n#define X6 seed\n#define X7 i\n#define X8 n\n#define X9  blockDim.x\n#define X10 blockDim.y\n#define X11 blockDim.z\n#define X12 gridDim.x\n#define X13 gridDim.y\n#define X14 gridDim.z\n#define X15 0\n\n  unsigned int a = 0x67452301;\n  unsigned int b = 0xefcdab89;\n  unsigned int c = 0x98badcfe;\n  unsigned int d = 0x10325476;\n\n  /* Round 1 */\n#define S11 7\n#define S12 12\n#define S13 17\n#define S14 22\n  FF ( a, b, c, d, X0 , S11, 3614090360); /* 1 */\n  FF ( d, a, b, c, X1 , S12, 3905402710); /* 2 */\n  FF ( c, d, a, b, X2 , S13,  606105819); /* 3 */\n  FF ( b, c, d, a, X3 , S14, 3250441966); /* 4 */\n  FF ( a, b, c, d, X4 , S11, 4118548399); /* 5 */\n  FF ( d, a, b, c, X5 , S12, 1200080426); /* 6 */\n  FF ( c, d, a, b, X6 , S13, 2821735955); /* 7 */\n  FF ( b, c, d, a, X7 , S14, 4249261313); /* 8 */\n  FF ( a, b, c, d, X8 , S11, 1770035416); /* 9 */\n  FF ( d, a, b, c, X9 , S12, 2336552879); /* 10 */\n  FF ( c, d, a, b, X10, S13, 4294925233); /* 11 */\n  FF ( b, c, d, a, X11, S14, 2304563134); /* 12 */\n  FF ( a, b, c, d, X12, S11, 1804603682); /* 13 */\n  FF ( d, a, b, c, X13, S12, 4254626195); /* 14 */\n  FF ( c, d, a, b, X14, S13, 2792965006); /* 15 */\n  FF ( b, c, d, a, X15, S14, 1236535329); /* 16 */\n\n  /* Round 2 */\n#define S21 5\n#define S22 9\n#define S23 14\n#define S24 20\n  GG ( a, b, c, d, X1 , S21, 4129170786); /* 17 */\n  GG ( d, a, b, c, X6 , S22, 3225465664); /* 18 */\n  GG ( c, d, a, b, X11, S23,  643717713); /* 19 */\n  GG ( b, c, d, a, X0 , S24, 3921069994); /* 20 */\n  GG ( a, b, c, d, X5 , S21, 3593408605); /* 21 */\n  GG ( d, a, b, c, X10, S22,   38016083); /* 22 */\n  GG ( c, d, a, b, X15, S23, 3634488961); /* 23 */\n  GG ( b, c, d, a, X4 , S24, 3889429448); /* 24 */\n  GG ( a, b, c, d, X9 , S21,  568446438); /* 25 */\n  GG ( d, a, b, c, X14, S22, 3275163606); /* 26 */\n  GG ( c, d, a, b, X3 , S23, 4107603335); /* 27 */\n  GG ( b, c, d, a, X8 , S24, 1163531501); /* 28 */\n  GG ( a, b, c, d, X13, S21, 2850285829); /* 29 */\n  GG ( d, a, b, c, X2 , S22, 4243563512); /* 30 */\n  GG ( c, d, a, b, X7 , S23, 1735328473); /* 31 */\n  GG ( b, c, d, a, X12, S24, 2368359562); /* 32 */\n\n  /* Round 3 */\n#define S31 4\n#define S32 11\n#define S33 16\n#define S34 23\n  HH ( a, b, c, d, X5 , S31, 4294588738); /* 33 */\n  HH ( d, a, b, c, X8 , S32, 2272392833); /* 34 */\n  HH ( c, d, a, b, X11, S33, 1839030562); /* 35 */\n  HH ( b, c, d, a, X14, S34, 4259657740); /* 36 */\n  HH ( a, b, c, d, X1 , S31, 2763975236); /* 37 */\n  HH ( d, a, b, c, X4 , S32, 1272893353); /* 38 */\n  HH ( c, d, a, b, X7 , S33, 4139469664); /* 39 */\n  HH ( b, c, d, a, X10, S34, 3200236656); /* 40 */\n  HH ( a, b, c, d, X13, S31,  681279174); /* 41 */\n  HH ( d, a, b, c, X0 , S32, 3936430074); /* 42 */\n  HH ( c, d, a, b, X3 , S33, 3572445317); /* 43 */\n  HH ( b, c, d, a, X6 , S34,   76029189); /* 44 */\n  HH ( a, b, c, d, X9 , S31, 3654602809); /* 45 */\n  HH ( d, a, b, c, X12, S32, 3873151461); /* 46 */\n  HH ( c, d, a, b, X15, S33,  530742520); /* 47 */\n  HH ( b, c, d, a, X2 , S34, 3299628645); /* 48 */\n\n  /* Round 4 */\n#define S41 6\n#define S42 10\n#define S43 15\n#define S44 21\n  II ( a, b, c, d, X0 , S41, 4096336452); /* 49 */\n  II ( d, a, b, c, X7 , S42, 1126891415); /* 50 */\n  II ( c, d, a, b, X14, S43, 2878612391); /* 51 */\n  II ( b, c, d, a, X5 , S44, 4237533241); /* 52 */\n  II ( a, b, c, d, X12, S41, 1700485571); /* 53 */\n  II ( d, a, b, c, X3 , S42, 2399980690); /* 54 */\n  II ( c, d, a, b, X10, S43, 4293915773); /* 55 */\n  II ( b, c, d, a, X1 , S44, 2240044497); /* 56 */\n  II ( a, b, c, d, X8 , S41, 1873313359); /* 57 */\n  II ( d, a, b, c, X15, S42, 4264355552); /* 58 */\n  II ( c, d, a, b, X6 , S43, 2734768916); /* 59 */\n  II ( b, c, d, a, X13, S44, 1309151649); /* 60 */\n  II ( a, b, c, d, X4 , S41, 4149444226); /* 61 */\n  II ( d, a, b, c, X11, S42, 3174756917); /* 62 */\n  II ( c, d, a, b, X2 , S43,  718787259); /* 63 */\n  II ( b, c, d, a, X9 , S44, 3951481745); /* 64 */\n\n  a += 0x67452301;\n  b += 0xefcdab89;\n  c += 0x98badcfe;\n  d += 0x10325476;\n'

def rand(shape, dtype=np.float32, stream=None):
    from pycuda.gpuarray import GPUArray
    from pycuda.elementwise import get_elwise_kernel
    result = GPUArray(shape, dtype)
    if dtype == np.float32:
        func = get_elwise_kernel('float *dest, unsigned int seed', md5_code + '\n            #define POW_2_M32 (1/4294967296.0f)\n            dest[i] = a*POW_2_M32;\n            if ((i += total_threads) < n)\n                dest[i] = b*POW_2_M32;\n            if ((i += total_threads) < n)\n                dest[i] = c*POW_2_M32;\n            if ((i += total_threads) < n)\n                dest[i] = d*POW_2_M32;\n            ', 'md5_rng_float')
    elif dtype == np.float64:
        func = get_elwise_kernel('double *dest, unsigned int seed', md5_code + '\n            #define POW_2_M32 (1/4294967296.0)\n            #define POW_2_M64 (1/18446744073709551616.)\n\n            dest[i] = a*POW_2_M32 + b*POW_2_M64;\n\n            if ((i += total_threads) < n)\n            {\n              dest[i] = c*POW_2_M32 + d*POW_2_M64;\n            }\n            ', 'md5_rng_float')
    elif dtype in [np.int32, np.uint32]:
        func = get_elwise_kernel('unsigned int *dest, unsigned int seed', md5_code + '\n            dest[i] = a;\n            if ((i += total_threads) < n)\n                dest[i] = b;\n            if ((i += total_threads) < n)\n                dest[i] = c;\n            if ((i += total_threads) < n)\n                dest[i] = d;\n            ', 'md5_rng_int')
    else:
        raise NotImplementedError
    func.prepared_async_call(result._grid, result._block, stream, result.gpudata, np.random.randint(2147483647), result.size)
    return result


try:
    import pycuda._driver as _curand
except ImportError:

    def get_curand_version():
        return


else:
    get_curand_version = _curand.get_curand_version

if get_curand_version() >= (3, 2, 0):
    direction_vector_set = _curand.direction_vector_set
    _get_direction_vectors = _curand._get_direction_vectors
if get_curand_version() >= (4, 0, 0):
    _get_scramble_constants32 = _curand._get_scramble_constants32
    _get_scramble_constants64 = _curand._get_scramble_constants64
gen_template = '\n__global__ void %(name)s(%(state_type)s *s, %(out_type)s *d, const int n)\n{\n  const int tidx = blockIdx.x*blockDim.x+threadIdx.x;\n  const int delta = blockDim.x*gridDim.x;\n  for (int idx = tidx; idx < n; idx += delta)\n    d[idx] = curand%(suffix)s(&s[tidx]);\n}\n'
gen_log_template = '\n__global__ void %(name)s(%(state_type)s *s, %(out_type)s *d, %(in_type)s mean, %(in_type)s stddev, const int n)\n{\n  const int tidx = blockIdx.x*blockDim.x+threadIdx.x;\n  const int delta = blockDim.x*gridDim.x;\n  for (int idx = tidx; idx < n; idx += delta)\n    d[idx] = curand_log%(suffix)s(&s[tidx], mean, stddev);\n}\n'
gen_poisson_template = '\n__global__ void %(name)s(%(state_type)s *s, %(out_type)s *d, double lambda, const int n)\n{\n  const int tidx = blockIdx.x*blockDim.x+threadIdx.x;\n  const int delta = blockDim.x*gridDim.x;\n  for (int idx = tidx; idx < n; idx += delta)\n    d[idx] = curand_poisson%(suffix)s(&s[tidx], lambda);\n}\n'
random_source = '\n// Uses C++ features (templates); do not surround with extern C\n#include <curand_kernel.h>\n\nextern "C"\n{\n\n%(generators)s\n\n}\n'
random_skip_ahead32_source = '\nextern "C" {\n__global__ void skip_ahead(%(state_type)s *s, const int n, const unsigned int skip)\n{\n  const int idx = blockIdx.x*blockDim.x+threadIdx.x;\n  if (idx < n)\n    skipahead(skip, &s[idx]);\n}\n\n__global__ void skip_ahead_array(%(state_type)s *s, const int n, const unsigned int *skip)\n{\n  const int idx = blockIdx.x*blockDim.x+threadIdx.x;\n  if (idx < n)\n      skipahead(skip[idx], &s[idx]);\n}\n}\n'
random_skip_ahead64_source = '\nextern "C" {\n__global__ void skip_ahead(%(state_type)s *s, const int n, const unsigned long long skip)\n{\n  const int idx = blockIdx.x*blockDim.x+threadIdx.x;\n  if (idx < n)\n    skipahead(skip, &s[idx]);\n}\n\n__global__ void skip_ahead_array(%(state_type)s *s, const int n, const unsigned long long *skip)\n{\n  const int idx = blockIdx.x*blockDim.x+threadIdx.x;\n  if (idx < n)\n      skipahead(skip[idx], &s[idx]);\n}\n}\n'

class _RandomNumberGeneratorBase(object):
    """
    Class surrounding CURAND kernels from CUDA 3.2.
    It allows for generating random numbers with uniform
    and normal probability function of various types.
    """
    gen_info = [
     ('uniform_int', 'unsigned int', ''),
     ('uniform_long', 'unsigned long long', ''),
     ('uniform_float', 'float', '_uniform'),
     ('uniform_double', 'double', '_uniform_double'),
     ('normal_float', 'float', '_normal'),
     ('normal_double', 'double', '_normal_double'),
     ('normal_float2', 'float2', '_normal2'),
     ('normal_double2', 'double2', '_normal2_double')]
    gen_log_info = [
     ('normal_log_float', 'float', 'float', '_normal'),
     ('normal_log_double', 'double', 'double', '_normal_double'),
     ('normal_log_float2', 'float', 'float2', '_normal2'),
     ('normal_log_double2', 'double', 'double2', '_normal2_double')]
    gen_poisson_info = [
     ('poisson_int', 'unsigned int', '')]

    def __init__(self, state_type, vector_type, generator_bits, additional_source, scramble_type=None):
        if get_curand_version() < (3, 2, 0):
            raise EnvironmentError('Need at least CUDA 3.2')
        dev = drv.Context.get_device()
        self.block_count = dev.get_attribute(pycuda.driver.device_attribute.MULTIPROCESSOR_COUNT)
        from pycuda.characterize import has_double_support

        def do_generate(out_type):
            result = True
            if 'double' in out_type:
                result = result and has_double_support()
            if '2' in out_type:
                result = result and self.has_box_muller
            return result

        my_generators = [ (name, out_type, suffix) for name, out_type, suffix in self.gen_info if do_generate(out_type)
                        ]
        if get_curand_version() >= (4, 0, 0):
            my_log_generators = [ (name, in_type, out_type, suffix) for name, in_type, out_type, suffix in self.gen_log_info if do_generate(out_type)
                                ]
        if get_curand_version() >= (5, 0, 0):
            my_poisson_generators = [ (name, out_type, suffix) for name, out_type, suffix in self.gen_poisson_info if do_generate(out_type)
                                    ]
        generator_sources = [ gen_template % {'name': name, 'out_type': out_type, 'suffix': suffix, 'state_type': state_type} for name, out_type, suffix in my_generators
                            ]
        if get_curand_version() >= (4, 0, 0):
            generator_sources.extend([ gen_log_template % {'name': name, 'in_type': in_type, 'out_type': out_type, 'suffix': suffix, 'state_type': state_type} for name, in_type, out_type, suffix in my_log_generators
                                     ])
        if get_curand_version() >= (5, 0, 0):
            generator_sources.extend([ gen_poisson_template % {'name': name, 'out_type': out_type, 'suffix': suffix, 'state_type': state_type} for name, out_type, suffix in my_poisson_generators
                                     ])
        source = (random_source + additional_source) % {'state_type': state_type, 
           'vector_type': vector_type, 
           'scramble_type': scramble_type, 
           'generators': ('\n').join(generator_sources)}
        self.module = module = pycuda.compiler.SourceModule(source, no_extern_c=True)
        self.generators = {}
        for name, out_type, suffix in my_generators:
            gen_func = module.get_function(name)
            gen_func.prepare('PPi')
            self.generators[name] = gen_func

        if get_curand_version() >= (4, 0, 0):
            for name, in_type, out_type, suffix in my_log_generators:
                gen_func = module.get_function(name)
                if in_type == 'float':
                    gen_func.prepare('PPffi')
                if in_type == 'double':
                    gen_func.prepare('PPddi')
                self.generators[name] = gen_func

        if get_curand_version() >= (5, 0, 0):
            for name, out_type, suffix in my_poisson_generators:
                gen_func = module.get_function(name)
                gen_func.prepare('PPdi')
                self.generators[name] = gen_func

        self.generator_bits = generator_bits
        self._prepare_skipahead()
        self.state_type = state_type
        self._state = None
        return

    def _prepare_skipahead(self):
        self.skip_ahead = self.module.get_function('skip_ahead')
        if self.generator_bits == 32:
            self.skip_ahead.prepare('PiI')
        if self.generator_bits == 64:
            self.skip_ahead.prepare('PiQ')
        self.skip_ahead_array = self.module.get_function('skip_ahead_array')
        self.skip_ahead_array.prepare('PiP')

    def _kernels(self):
        return list(six.itervalues(self.generators)) + [
         self.skip_ahead, self.skip_ahead_array]

    @property
    @memoize_method
    def generators_per_block(self):
        return min(kernel.max_threads_per_block for kernel in self._kernels())

    @property
    def state(self):
        if self._state is None:
            from pycuda.characterize import sizeof
            data_type_size = sizeof(self.state_type, '#include <curand_kernel.h>')
            self._state = drv.mem_alloc(self.block_count * self.generators_per_block * data_type_size)
        return self._state

    def fill_uniform(self, data, stream=None):
        if data.dtype == np.float32:
            func = self.generators['uniform_float']
        elif data.dtype == np.float64:
            func = self.generators['uniform_double']
        elif data.dtype in [np.int, np.int32, np.uint32]:
            func = self.generators['uniform_int']
        elif data.dtype in [np.int64, np.uint64] and self.generator_bits >= 64:
            func = self.generators['uniform_long']
        else:
            raise NotImplementedError
        func.prepared_async_call((
         self.block_count, 1), (self.generators_per_block, 1, 1), stream, self.state, data.gpudata, data.size)

    def fill_normal(self, data, stream=None):
        if data.dtype == np.float32:
            func_name = 'normal_float'
        elif data.dtype == np.float64:
            func_name = 'normal_double'
        else:
            raise NotImplementedError
        data_size = data.size
        if self.has_box_muller and data_size % 2 == 0:
            func_name += '2'
            data_size //= 2
        func = self.generators[func_name]
        func.prepared_async_call((
         self.block_count, 1), (self.generators_per_block, 1, 1), stream, self.state, data.gpudata, int(data_size))

    def gen_uniform(self, shape, dtype, stream=None):
        result = array.empty(shape, dtype)
        self.fill_uniform(result, stream)
        return result

    def gen_normal(self, shape, dtype, stream=None):
        result = array.empty(shape, dtype)
        self.fill_normal(result, stream)
        return result

    if get_curand_version() >= (4, 0, 0):

        def fill_log_normal(self, data, mean, stddev, stream=None):
            if data.dtype == np.float32:
                func_name = 'normal_log_float'
            elif data.dtype == np.float64:
                func_name = 'normal_log_double'
            else:
                raise NotImplementedError
            data_size = data.size
            if self.has_box_muller and data_size % 2 == 0:
                func_name += '2'
                data_size //= 2
            func = self.generators[func_name]
            func.prepared_async_call((
             self.block_count, 1), (self.generators_per_block, 1, 1), stream, self.state, data.gpudata, mean, stddev, int(data_size))

        def gen_log_normal(self, shape, dtype, mean, stddev, stream=None):
            result = array.empty(shape, dtype)
            self.fill_log_normal(result, mean, stddev, stream)
            return result

    if get_curand_version() >= (5, 0, 0):

        def fill_poisson(self, data, lambda_value, stream=None):
            if data.dtype == np.uint32:
                func_name = 'poisson_int'
            else:
                raise NotImplementedError
            func = self.generators[func_name]
            func.prepared_async_call((
             self.block_count, 1), (self.generators_per_block, 1, 1), stream, self.state, data.gpudata, lambda_value, data.size)

        def gen_poisson(self, shape, dtype, lambda_value, stream=None):
            result = array.empty(shape, dtype)
            self.fill_poisson(result, lambda_value, stream)
            return result

    def call_skip_ahead(self, i, stream=None):
        self.skip_ahead.prepared_async_call((
         self.block_count, 1), (self.generators_per_block, 1, 1), stream, self.state, self.generators_per_block, i)

    def call_skip_ahead_array(self, i, stream=None):
        self.skip_ahead_array.prepared_async_call((
         self.block_count, 1), (self.generators_per_block, 1, 1), stream, self.state, self.generators_per_block, i.gpudata)


class _PseudoRandomNumberGeneratorBase(_RandomNumberGeneratorBase):

    def __init__(self, seed_getter, offset, state_type, vector_type, generator_bits, additional_source, scramble_type=None):
        super(_PseudoRandomNumberGeneratorBase, self).__init__(state_type, vector_type, generator_bits, additional_source)
        generator_count = self.generators_per_block * self.block_count
        if seed_getter is None:
            seed = array.to_gpu(np.asarray(np.random.random_integers(0, 2147483646, generator_count), dtype=np.int32))
        else:
            seed = seed_getter(generator_count)
        if not (isinstance(seed, pycuda.gpuarray.GPUArray) and seed.dtype == np.int32 and seed.size == generator_count):
            raise TypeError('seed must be GPUArray of integers of right length')
        p = self.module.get_function('prepare')
        p.prepare('PiPi')
        from pycuda.characterize import has_stack
        has_stack = has_stack()
        if has_stack:
            prev_stack_size = drv.Context.get_limit(drv.limit.STACK_SIZE)
        try:
            if has_stack:
                drv.Context.set_limit(drv.limit.STACK_SIZE, 16384)
            try:
                p.prepared_call((
                 self.block_count, 1), (self.generators_per_block, 1, 1), self.state, generator_count, seed.gpudata, offset)
            except drv.LaunchError:
                raise ValueError('Initialisation failed. Decrease number of threads.')

        finally:
            if has_stack:
                drv.Context.set_limit(drv.limit.STACK_SIZE, prev_stack_size)

        return

    def _prepare_skipahead(self):
        self.skip_ahead = self.module.get_function('skip_ahead')
        self.skip_ahead.prepare('PiQ')
        self.skip_ahead_array = self.module.get_function('skip_ahead_array')
        self.skip_ahead_array.prepare('PiP')
        self.skip_ahead_sequence = self.module.get_function('skip_ahead_sequence')
        self.skip_ahead_sequence.prepare('PiQ')
        self.skip_ahead_sequence_array = self.module.get_function('skip_ahead_sequence_array')
        self.skip_ahead_sequence_array.prepare('PiP')

    def call_skip_ahead_sequence(self, i, stream=None):
        self.skip_ahead_sequence.prepared_async_call((
         self.block_count, 1), (self.generators_per_block, 1, 1), stream, self.state, self.generators_per_block * self.block_count, i)

    def call_skip_ahead_sequence_array(self, i, stream=None):
        self.skip_ahead_sequence_array.prepared_async_call((
         self.block_count, 1), (self.generators_per_block, 1, 1), stream, self.state, self.generators_per_block * self.block_count, i.gpudata)

    def _kernels(self):
        return _RandomNumberGeneratorBase._kernels(self) + [self.module.get_function('prepare')] + [self.module.get_function('skip_ahead_sequence'),
         self.module.get_function('skip_ahead_sequence_array')]


def seed_getter_uniform(N):
    result = pycuda.gpuarray.empty([N], np.int32)
    import random
    value = random.randint(0, 2147483647)
    return result.fill(value)


def seed_getter_unique(N):
    result = np.random.randint(0, 2147483647, N).astype(np.int32)
    return pycuda.gpuarray.to_gpu(result)


xorwow_random_source = '\nextern "C" {\n__global__ void prepare(%(state_type)s *s, const int n,\n    %(vector_type)s *v, const unsigned int o)\n{\n  const int id = blockIdx.x*blockDim.x+threadIdx.x;\n  if (id < n)\n    curand_init(v[id], id, o, &s[id]);\n}\n}\n'
xorwow_skip_ahead_sequence_source = '\nextern "C" {\n__global__ void skip_ahead_sequence(%(state_type)s *s, const int n, const unsigned long long skip)\n{\n  const int idx = blockIdx.x*blockDim.x+threadIdx.x;\n  if (idx < n)\n    skipahead_sequence(skip, &s[idx]);\n}\n\n__global__ void skip_ahead_sequence_array(%(state_type)s *s, const int n, const unsigned long long *skip)\n{\n  const int idx = blockIdx.x*blockDim.x+threadIdx.x;\n  if (idx < n)\n      skipahead_sequence(skip[idx], &s[idx]);\n}\n}\n'
if get_curand_version() >= (3, 2, 0):

    class XORWOWRandomNumberGenerator(_PseudoRandomNumberGeneratorBase):
        has_box_muller = True

        def __init__(self, seed_getter=None, offset=0):
            """
            :arg seed_getter: a function that, given an integer count, will yield an `int32`
              :class:`GPUArray` of seeds.
            """
            super(XORWOWRandomNumberGenerator, self).__init__(seed_getter, offset, 'curandStateXORWOW', 'unsigned int', 32, xorwow_random_source + xorwow_skip_ahead_sequence_source + random_skip_ahead64_source)


mrg32k3a_random_source = '\nextern "C" {\n__global__ void prepare(%(state_type)s *s, const int n,\n    %(vector_type)s *v, const unsigned int o)\n{\n  const int id = blockIdx.x*blockDim.x+threadIdx.x;\n  if (id < n)\n    curand_init(v[id], id, o, &s[id]);\n}\n}\n'
mrg32k3a_skip_ahead_sequence_source = '\nextern "C" {\n__global__ void skip_ahead_sequence(%(state_type)s *s, const int n, const unsigned long long skip)\n{\n  const int idx = blockIdx.x*blockDim.x+threadIdx.x;\n  if (idx < n)\n    skipahead_sequence(skip, &s[idx]);\n}\n\n__global__ void skip_ahead_sequence_array(%(state_type)s *s, const int n, const unsigned long long *skip)\n{\n  const int idx = blockIdx.x*blockDim.x+threadIdx.x;\n  if (idx < n)\n      skipahead_sequence(skip[idx], &s[idx]);\n}\n\n__global__ void skip_ahead_subsequence(%(state_type)s *s, const int n, const unsigned long long skip)\n{\n  const int idx = blockIdx.x*blockDim.x+threadIdx.x;\n  if (idx < n)\n    skipahead_subsequence(skip, &s[idx]);\n}\n\n__global__ void skip_ahead_subsequence_array(%(state_type)s *s, const int n, const unsigned long long *skip)\n{\n  const int idx = blockIdx.x*blockDim.x+threadIdx.x;\n  if (idx < n)\n      skipahead_subsequence(skip[idx], &s[idx]);\n}\n}\n'
if get_curand_version() >= (4, 1, 0):

    class MRG32k3aRandomNumberGenerator(_PseudoRandomNumberGeneratorBase):
        has_box_muller = True

        def __init__(self, seed_getter=None, offset=0):
            """
            :arg seed_getter: a function that, given an integer count, will yield an `int32`
              :class:`GPUArray` of seeds.
            """
            super(MRG32k3aRandomNumberGenerator, self).__init__(seed_getter, offset, 'curandStateMRG32k3a', 'unsigned int', 32, mrg32k3a_random_source + mrg32k3a_skip_ahead_sequence_source + random_skip_ahead64_source)

        def _prepare_skipahead(self):
            super(MRG32k3aRandomNumberGenerator, self)._prepare_skipahead()
            self.skip_ahead_subsequence = self.module.get_function('skip_ahead_subsequence')
            self.skip_ahead_subsequence.prepare('PiQ')
            self.skip_ahead_subsequence_array = self.module.get_function('skip_ahead_subsequence_array')
            self.skip_ahead_subsequence_array.prepare('PiP')

        def call_skip_ahead_subsequence(self, i, stream=None):
            self.skip_ahead_subsequence.prepared_async_call((
             self.block_count, 1), (self.generators_per_block, 1, 1), stream, self.state, self.generators_per_block * self.block_count, i)

        def call_skip_ahead_subsequence_array(self, i, stream=None):
            self.skip_ahead_subsequence_array.prepared_async_call((
             self.block_count, 1), (self.generators_per_block, 1, 1), stream, self.state, self.generators_per_block * self.block_count, i.gpudata)

        def _kernels(self):
            return _PseudoRandomNumberGeneratorBase._kernels(self) + [
             self.module.get_function('skip_ahead_subsequence'),
             self.module.get_function('skip_ahead_subsequence_array')]


def generate_direction_vectors(count, direction=None):
    if get_curand_version() >= (4, 0, 0):
        if direction == direction_vector_set.VECTOR_64 or direction == direction_vector_set.SCRAMBLED_VECTOR_64:
            result = np.empty((count, 64), dtype=np.uint64)
        else:
            result = np.empty((count, 32), dtype=np.uint32)
    else:
        result = np.empty((count, 32), dtype=np.uint32)
    _get_direction_vectors(direction, result, count)
    return pycuda.gpuarray.to_gpu(result)


if get_curand_version() >= (4, 0, 0):

    def generate_scramble_constants32(count):
        result = np.empty((count,), dtype=np.uint32)
        _get_scramble_constants32(result, count)
        return pycuda.gpuarray.to_gpu(result)


    def generate_scramble_constants64(count):
        result = np.empty((count,), dtype=np.uint64)
        _get_scramble_constants64(result, count)
        return pycuda.gpuarray.to_gpu(result)


sobol_random_source = '\nextern "C" {\n__global__ void prepare(%(state_type)s *s, const int n,\n    %(vector_type)s *v, const unsigned int o)\n{\n  const int id = blockIdx.x*blockDim.x+threadIdx.x;\n  if (id < n)\n    curand_init(v[id], o, &s[id]);\n}\n}\n'

class _SobolRandomNumberGeneratorBase(_RandomNumberGeneratorBase):
    """
    Class surrounding CURAND kernels from CUDA 3.2.
    It allows for generating quasi-random numbers with uniform
    and normal probability function of type int, float, and double.
    """
    has_box_muller = False

    def __init__(self, dir_vector, dir_vector_dtype, dir_vector_size, dir_vector_set, offset, state_type, vector_type, generator_bits, sobol_random_source):
        super(_SobolRandomNumberGeneratorBase, self).__init__(state_type, vector_type, generator_bits, sobol_random_source)
        if dir_vector is None:
            dir_vector = generate_direction_vectors(self.block_count * self.generators_per_block, dir_vector_set)
        if not (isinstance(dir_vector, pycuda.gpuarray.GPUArray) and dir_vector.dtype == dir_vector_dtype and dir_vector.shape == (self.block_count * self.generators_per_block, dir_vector_size)):
            raise TypeError('seed must be GPUArray of integers of right length')
        p = self.module.get_function('prepare')
        p.prepare('PiPi')
        from pycuda.characterize import has_stack
        has_stack = has_stack()
        if has_stack:
            prev_stack_size = drv.Context.get_limit(drv.limit.STACK_SIZE)
        try:
            if has_stack:
                drv.Context.set_limit(drv.limit.STACK_SIZE, 16384)
            try:
                p.prepared_call((self.block_count, 1), (self.generators_per_block, 1, 1), self.state, self.block_count * self.generators_per_block, dir_vector.gpudata, offset)
            except drv.LaunchError:
                raise ValueError('Initialisation failed. Decrease number of threads.')

        finally:
            if has_stack:
                drv.Context.set_limit(drv.limit.STACK_SIZE, prev_stack_size)

        return

    def _kernels(self):
        return _RandomNumberGeneratorBase._kernels(self) + [
         self.module.get_function('prepare')]


scrambledsobol_random_source = '\nextern "C" {\n__global__ void prepare( %(state_type)s *s, const int n,\n    %(vector_type)s *v, %(scramble_type)s *scramble, const unsigned int o)\n{\n  const int id = blockIdx.x*blockDim.x+threadIdx.x;\n  if (id < n)\n    curand_init(v[id], scramble[id], o, &s[id]);\n}\n}\n'

class _ScrambledSobolRandomNumberGeneratorBase(_RandomNumberGeneratorBase):
    """
    Class surrounding CURAND kernels from CUDA 4.0.
    It allows for generating quasi-random numbers with uniform
    and normal probability function of type int, float, and double.
    """
    has_box_muller = False

    def __init__(self, dir_vector, dir_vector_dtype, dir_vector_size, dir_vector_set, scramble_vector, scramble_vector_function, offset, state_type, vector_type, generator_bits, scramble_type, sobol_random_source):
        super(_ScrambledSobolRandomNumberGeneratorBase, self).__init__(state_type, vector_type, generator_bits, sobol_random_source, scramble_type)
        if dir_vector is None:
            dir_vector = generate_direction_vectors(self.block_count * self.generators_per_block, dir_vector_set)
        if scramble_vector is None:
            scramble_vector = scramble_vector_function(self.block_count * self.generators_per_block)
        if not (isinstance(dir_vector, pycuda.gpuarray.GPUArray) and dir_vector.dtype == dir_vector_dtype and dir_vector.shape == (self.block_count * self.generators_per_block, dir_vector_size)):
            raise TypeError('seed must be GPUArray of integers of right length')
        if not (isinstance(scramble_vector, pycuda.gpuarray.GPUArray) and scramble_vector.dtype == dir_vector_dtype and scramble_vector.shape == (self.block_count * self.generators_per_block,)):
            raise TypeError('scramble must be GPUArray of integers of right length')
        p = self.module.get_function('prepare')
        p.prepare('PiPPi')
        from pycuda.characterize import has_stack
        has_stack = has_stack()
        if has_stack:
            prev_stack_size = drv.Context.get_limit(drv.limit.STACK_SIZE)
        try:
            if has_stack:
                drv.Context.set_limit(drv.limit.STACK_SIZE, 16384)
            try:
                p.prepared_call((self.block_count, 1), (self.generators_per_block, 1, 1), self.state, self.block_count * self.generators_per_block, dir_vector.gpudata, scramble_vector.gpudata, offset)
            except drv.LaunchError:
                raise ValueError('Initialisation failed. Decrease number of threads.')

        finally:
            if has_stack:
                drv.Context.set_limit(drv.limit.STACK_SIZE, prev_stack_size)

        return

    def _kernels(self):
        return _RandomNumberGeneratorBase._kernels(self) + [
         self.module.get_function('prepare')]


if get_curand_version() >= (3, 2, 0):

    class Sobol32RandomNumberGenerator(_SobolRandomNumberGeneratorBase):
        """
        Class surrounding CURAND kernels from CUDA 3.2.
        It allows for generating quasi-random numbers with uniform
        and normal probability function of type int, float, and double.
        """

        def __init__(self, dir_vector=None, offset=0):
            super(Sobol32RandomNumberGenerator, self).__init__(dir_vector, np.uint32, 32, direction_vector_set.VECTOR_32, offset, 'curandStateSobol32', 'curandDirectionVectors32_t', 32, sobol_random_source + random_skip_ahead32_source)


if get_curand_version() >= (4, 0, 0):

    class ScrambledSobol32RandomNumberGenerator(_ScrambledSobolRandomNumberGeneratorBase):
        """
        Class surrounding CURAND kernels from CUDA 4.0.
        It allows for generating quasi-random numbers with uniform
        and normal probability function of type int, float, and double.
        """

        def __init__(self, dir_vector=None, scramble_vector=None, offset=0):
            super(ScrambledSobol32RandomNumberGenerator, self).__init__(dir_vector, np.uint32, 32, direction_vector_set.SCRAMBLED_VECTOR_32, scramble_vector, generate_scramble_constants32, offset, 'curandStateScrambledSobol32', 'curandDirectionVectors32_t', 32, 'unsigned int', scrambledsobol_random_source + random_skip_ahead32_source)


if get_curand_version() >= (4, 0, 0):

    class Sobol64RandomNumberGenerator(_SobolRandomNumberGeneratorBase):
        """
        Class surrounding CURAND kernels from CUDA 4.0.
        It allows for generating quasi-random numbers with uniform
        and normal probability function of type int, float, and double.
        """

        def __init__(self, dir_vector=None, offset=0):
            super(Sobol64RandomNumberGenerator, self).__init__(dir_vector, np.uint64, 64, direction_vector_set.VECTOR_64, offset, 'curandStateSobol64', 'curandDirectionVectors64_t', 64, sobol_random_source + random_skip_ahead64_source)


if get_curand_version() >= (4, 0, 0):

    class ScrambledSobol64RandomNumberGenerator(_ScrambledSobolRandomNumberGeneratorBase):
        """
        Class surrounding CURAND kernels from CUDA 4.0.
        It allows for generating quasi-random numbers with uniform
        and normal probability function of type int, float, and double.
        """

        def __init__(self, dir_vector=None, scramble_vector=None, offset=0):
            super(ScrambledSobol64RandomNumberGenerator, self).__init__(dir_vector, np.uint64, 64, direction_vector_set.SCRAMBLED_VECTOR_64, scramble_vector, generate_scramble_constants64, offset, 'curandStateScrambledSobol64', 'curandDirectionVectors64_t', 64, 'unsigned long long', scrambledsobol_random_source + random_skip_ahead64_source)