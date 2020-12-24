# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-armv7l/egg/pycuda/sparse/coordinate.py
# Compiled at: 2015-06-16 13:16:13
from __future__ import division
from __future__ import absolute_import
from pytools import memoize_method
import pycuda.driver as drv, pycuda.gpuarray as gpuarray
from pycuda.compiler import SourceModule
import numpy as np
COO_FLAT_KERNEL_TEMPLATE = "\n#include <pycuda-helpers.hpp>\n\n#define BLOCK_SIZE %(block_size)d\n#define WARP_SIZE %(warp_size)d\n\ntypedef %(value_type)s value_type;\ntypedef %(index_type)s index_type;\n\ntexture<%(tex_value_type)s, 1, cudaReadModeElementType> tex_x;\n\nstatic __inline__ __device__ float atomicAdd(float *addr, float val)\n{\n    float old=*addr, assumed;\n\n    do {\n        assumed = old;\n        old = int_as_float( atomicCAS((int*)addr,\n                                        float_as_int(assumed),\n                                        float_as_int(val+assumed)));\n    } while( assumed!=old );\n\n    return old;\n}\n\n#ifndef CUDA_NO_SM_13_DOUBLE_INTRINSICS\nstatic __attribute__ ((unused)) __inline__ __device__ double atomicAdd(double *addr, double val)\n{\n    double old=*addr, assumed;\n\n    do {\n        assumed = old;\n        old = __longlong_as_double( atomicCAS((unsigned long long int*)addr,\n                                        __double_as_longlong(assumed),\n                                        __double_as_longlong(val+assumed)));\n    } while( assumed!=old );\n\n    return old;\n}\n#endif\n\n__global__ void\nspmv_coo_flat_kernel(const index_type num_nonzeros,\n                     const index_type interval_size,\n                     const index_type *I,\n                     const index_type *J,\n                     const value_type *V,\n                           value_type *y)\n{\n  __shared__ index_type idx[BLOCK_SIZE];\n  __shared__ value_type val[BLOCK_SIZE];\n  __shared__ index_type carry_idx[BLOCK_SIZE / 32];\n  __shared__ value_type carry_val[BLOCK_SIZE / 32];\n\n  const index_type thread_id   = BLOCK_SIZE * blockIdx.x + threadIdx.x;     // global thread index\n  const index_type thread_lane = threadIdx.x & (WARP_SIZE-1);               // thread index within the warp\n  const index_type warp_id     = thread_id   / WARP_SIZE;                   // global warp index\n  const index_type warp_lane   = threadIdx.x / WARP_SIZE;                   // warp index within the CTA\n\n  const index_type begin = warp_id * interval_size + thread_lane;           // thread's offset into I,J,V\n  const index_type end   = min(begin + interval_size, num_nonzeros);        // end of thread's work\n\n  if(begin >= end) return;                                                 // warp has no work to do\n\n  const index_type first_idx = I[warp_id * interval_size];                  // first row of this warp's interval\n\n  if (thread_lane == 0)\n  {\n    carry_idx[warp_lane] = first_idx;\n    carry_val[warp_lane] = 0;\n  }\n\n  for(index_type n = begin; n < end; n += WARP_SIZE)\n  {\n    idx[threadIdx.x] = I[n];                                             // row index\n    val[threadIdx.x] = V[n] * fp_tex1Dfetch(tex_x, J[n]);                // val = A[row,col] * x[col]\n\n    if (thread_lane == 0){\n      if(idx[threadIdx.x] == carry_idx[warp_lane])\n          val[threadIdx.x] += carry_val[warp_lane];                    // row continues into this warp's span\n      else if(carry_idx[warp_lane] != first_idx)\n          y[carry_idx[warp_lane]] += carry_val[warp_lane];             // row terminated, does not span boundary\n      else\n          atomicAdd(y + carry_idx[warp_lane], carry_val[warp_lane]);   // row terminated, but spans iter-warp boundary\n    }\n\n    // segmented reduction in shared memory\n    if( thread_lane >=  1 && idx[threadIdx.x] == idx[threadIdx.x - 1] ) { val[threadIdx.x] += val[threadIdx.x -  1]; }\n    if( thread_lane >=  2 && idx[threadIdx.x] == idx[threadIdx.x - 2] ) { val[threadIdx.x] += val[threadIdx.x -  2]; }\n    if( thread_lane >=  4 && idx[threadIdx.x] == idx[threadIdx.x - 4] ) { val[threadIdx.x] += val[threadIdx.x -  4]; }\n    if( thread_lane >=  8 && idx[threadIdx.x] == idx[threadIdx.x - 8] ) { val[threadIdx.x] += val[threadIdx.x -  8]; }\n    if( thread_lane >= 16 && idx[threadIdx.x] == idx[threadIdx.x -16] ) { val[threadIdx.x] += val[threadIdx.x - 16]; }\n\n    if( thread_lane == 31 ) {\n      carry_idx[warp_lane] = idx[threadIdx.x];                         // last thread in warp saves its results\n      carry_val[warp_lane] = val[threadIdx.x];\n    }\n    else if ( idx[threadIdx.x] != idx[threadIdx.x+1] ) {                 // row terminates here\n      if(idx[threadIdx.x] != first_idx)\n          y[idx[threadIdx.x]] += val[threadIdx.x];                     // row terminated, does not span inter-warp boundary\n      else\n          atomicAdd(y + idx[threadIdx.x], val[threadIdx.x]);           // row terminated, but spans iter-warp boundary\n    }\n  }\n\n  // final carry\n  if(thread_lane == 31){\n    atomicAdd(y + carry_idx[warp_lane], carry_val[warp_lane]);\n  }\n}\n"
COO_SERIAL_KERNEL_TEMPLATE = '\ntypedef %(value_type)s value_type;\ntypedef %(index_type)s index_type;\n\n__global__ void\nspmv_coo_serial_kernel(const index_type num_nonzeros,\n                       const index_type *I,\n                       const index_type *J,\n                       const value_type *V,\n                       const value_type *x,\n                             value_type *y)\n{\n  for (index_type n = 0; n < num_nonzeros; n++)\n    y[I[n]] += V[n] * x[J[n]];\n}\n'

class CoordinateSpMV:

    def __init__(self, mat, dtype):
        self.dtype = np.dtype(dtype)
        self.index_dtype = np.dtype(np.int32)
        self.shape = mat.shape
        self.block_size = 128
        from scipy.sparse import coo_matrix
        coo_mat = coo_matrix(mat, dtype=self.dtype)
        self.row_gpu = gpuarray.to_gpu(coo_mat.row.astype(self.index_dtype))
        self.col_gpu = gpuarray.to_gpu(coo_mat.col.astype(self.index_dtype))
        self.data_gpu = gpuarray.to_gpu(coo_mat.data)
        self.nnz = coo_mat.nnz
        from pycuda.tools import DeviceData
        dev = drv.Context.get_device()
        devdata = DeviceData()
        max_threads = devdata.warps_per_mp * devdata.warp_size * dev.multiprocessor_count
        max_blocks = 4 * max_threads // self.block_size
        warps_per_block = self.block_size // dev.warp_size
        if self.nnz:

            def divide_into(x, y):
                return (x + y - 1) // y

            num_units = self.nnz // dev.warp_size
            num_warps = min(num_units, warps_per_block * max_blocks)
            self.num_blocks = divide_into(num_warps, warps_per_block)
            num_iters = divide_into(num_units, num_warps)
            self.interval_size = dev.warp_size * num_iters
            self.tail = num_units * dev.warp_size

    @memoize_method
    def get_flat_kernel(self):
        from pycuda.tools import dtype_to_ctype
        mod = SourceModule(COO_FLAT_KERNEL_TEMPLATE % {'value_type': dtype_to_ctype(self.dtype), 
           'tex_value_type': dtype_to_ctype(self.dtype, with_fp_tex_hack=True), 
           'index_type': dtype_to_ctype(self.index_dtype), 
           'block_size': self.block_size, 
           'warp_size': drv.Context.get_device().warp_size})
        func = mod.get_function('spmv_coo_flat_kernel')
        x_texref = mod.get_texref('tex_x')
        func.prepare(self.index_dtype.char * 2 + 'PPPP', (
         self.block_size, 1, 1), texrefs=[x_texref])
        return (
         func, x_texref)

    @memoize_method
    def get_serial_kernel(self):
        from pycuda.tools import dtype_to_ctype
        mod = SourceModule(COO_SERIAL_KERNEL_TEMPLATE % {'value_type': dtype_to_ctype(self.dtype), 
           'index_type': dtype_to_ctype(self.index_dtype)})
        func = mod.get_function('spmv_coo_serial_kernel')
        func.prepare(self.index_dtype.char + 'PPPPP', (1, 1, 1))
        return func

    def __call__(self, x, y=None):
        if y is None:
            y = gpuarray.zeros(self.shape[0], dtype=self.dtype, allocator=x.allocator)
        if self.nnz == 0:
            return y
        else:
            flat_func, x_texref = self.get_flat_kernel()
            x.bind_to_texref_ext(x_texref, allow_double_hack=True)
            flat_func.prepared_call((self.num_blocks, 1), self.tail, self.interval_size, self.row_gpu.gpudata, self.col_gpu.gpudata, self.data_gpu.gpudata, y.gpudata)
            self.get_serial_kernel().prepared_call((1, 1), self.nnz - self.tail, self.row_gpu[self.tail:].gpudata, self.col_gpu[self.tail:].gpudata, self.data_gpu[self.tail:].gpudata, x.gpudata, y.gpudata)
            return y