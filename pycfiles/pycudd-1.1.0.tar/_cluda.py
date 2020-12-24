# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-armv7l/egg/pycuda/_cluda.py
# Compiled at: 2013-06-07 13:57:48
CLUDA_PREAMBLE = '\n#define local_barrier() __syncthreads();\n\n#define WITHIN_KERNEL __device__\n#define KERNEL extern "C" __global__\n#define GLOBAL_MEM /* empty */\n#define LOCAL_MEM __shared__\n#define LOCAL_MEM_ARG /* empty */\n#define REQD_WG_SIZE(X,Y,Z) __launch_bounds__(X*Y*Z, 1)\n\n#define LID_0 threadIdx.x\n#define LID_1 threadIdx.y\n#define LID_2 threadIdx.z\n\n#define GID_0 blockIdx.x\n#define GID_1 blockIdx.y\n#define GID_2 blockIdx.z\n\n#define LDIM_0 blockDim.x\n#define LDIM_1 blockDim.y\n#define LDIM_2 blockDim.z\n\n#define GDIM_0 gridDim.x\n#define GDIM_1 gridDim.y\n#define GDIM_2 gridDim.z\n'