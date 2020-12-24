# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/dpcluster/gpu_exp.py
# Compiled at: 2013-06-21 17:50:30
import pycuda, pycuda.autoinit
from pycuda.compiler import SourceModule
from pycuda import gpuarray
import scikits.cuda.cublas as cublas
from jinja2 import Template
import numpy as np, time
cublas_handle = cublas.cublasCreate()

def bptrs(a):
    """
    Pointer array when input represents a batch of matrices.
    """
    return gpuarray.arange(a.ptr, a.ptr + a.shape[0] * a.strides[0], a.strides[0], dtype=cublas.ctypes.c_void_p)


def prepare(m):
    permute_template = Template('\n    __global__ void permute_inds(int x[][{{ m }}]) {\n        unsigned int idx = blockIdx.x * blockDim.x + threadIdx.x;\n\n        int a[{{ m }}];\n\n        for (int i=0; i<{{ m }}; i++) a[i]=i;\n            \n        for (int i=0; i<{{ m }}; i++){\n            int i_=x[idx][i]-1; \n            int t = a[i]; \n            a[i] = a[i_]; \n            a[i_] = t; };\n\n        for (int i=0; i<{{ m }}; i++) x[idx][i]=a[i];\n    }\n    __global__ void batch_permute_rows(int s[][{{ m }}], \n                        float a[][{{ m }}][{{ m }}],\n                        float b[][{{ m }}][{{ m }}]) {\n        unsigned int idx = blockIdx.x * blockDim.x + threadIdx.x;\n        unsigned int idy = blockIdx.y * blockDim.y + threadIdx.y;\n        unsigned int idz = blockIdx.z * blockDim.z + threadIdx.z;\n        \n        b[idx][idy][idz] = a[idx][idy][s[idx][idz]];\n    }\n\n    ')
    perm_mod = SourceModule(permute_template.render(m=m))
    pi = perm_mod.get_function('permute_inds').prepare('P')
    pr = perm_mod.get_function('batch_permute_rows').prepare('PPP')
    return (
     pi.prepared_call, pr.prepared_call)


from scipy.linalg import lu_factor
l, m = 100 * 33, 32
perm, pmatrix = prepare(m)
A = np.random.rand(l, m, m).astype(np.float32)
A = np.array([ np.matrix(a) * np.matrix(a).T for a in A ])
a_gpu = gpuarray.to_gpu(A)
a_arr = bptrs(a_gpu)
s_gpu = gpuarray.empty((l, m), np.int32)
i_gpu = gpuarray.zeros(1, np.int32)
po_gpu = gpuarray.to_gpu(np.repeat(np.eye(m)[np.newaxis, :, :], l, axis=0).astype(np.float32))
p_gpu = gpuarray.empty_like(po_gpu)
for k in range(10):
    t = time.time()
    cublas.cublasSgetrfBatched(cublas_handle, m, a_arr.gpudata, m, s_gpu.gpudata, i_gpu.gpudata, l)
    print time.time() - t,
    perm((l, 1, 1), (1, 1, 1), s_gpu.gpudata)
    pmatrix((l, 1, 1), (1, m, m), s_gpu.gpudata, po_gpu.gpudata, p_gpu.gpudata)
    print time.time() - t

cublas.cublasDestroy(cublas_handle)