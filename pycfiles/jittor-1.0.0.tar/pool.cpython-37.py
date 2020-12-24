# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/pool.py
# Compiled at: 2020-04-10 01:50:22
# Size of source mod 2**32: 8120 bytes
import jittor as jt
from jittor import init, Module
import numpy as np, math

class Pool(Module):

    def __init__(self, kernel_size, stride=None, padding=0, dilation=None, return_indices=None, ceil_mode=False, op='maximum'):
        assert dilation == None
        assert return_indices == None
        self.kernel_size = kernel_size
        self.op = op
        self.stride = stride if stride else kernel_size
        self.padding = padding
        self.ceil_mode = ceil_mode

    def execute(self, x):
        N, C, H, W = x.shape
        if self.ceil_mode == False:
            h = (H + self.padding * 2 - self.kernel_size) // self.stride + 1
            w = (W + self.padding * 2 - self.kernel_size) // self.stride + 1
        else:
            h = (H + self.padding * 2 - self.kernel_size + self.stride - 1) // self.stride + 1
            w = (W + self.padding * 2 - self.kernel_size + self.stride - 1) // self.stride + 1
        if self.op == 'maximum' or self.op == 'minimum':
            if self.op == 'maximum':
                op = 'max'
            else:
                op = 'min'
            out = jt.code([N, C, h, w], (x.dtype), [x], cuda_src=f"\n                    __global__ static void kernel1(@ARGS_DEF) {{\n                        @PRECALC\n                        int p3 = threadIdx.x;\n                        int s3 = blockDim.x;\n                        int p2 = threadIdx.y + blockIdx.x * blockDim.y;\n                        int s2 = blockDim.y * gridDim.x;\n                        int i1 = blockIdx.y;\n                        int i0 = blockIdx.z;\n                        for (int i3 = p3; i3 < outshape3; i3 += s3)\n                            for (int i2 = p2; i2 < outshape2; i2 += s2) {{\n                                int k3 = i3*{self.stride}-{self.padding};\n                                int k2 = i2*{self.stride}-{self.padding};\n                                int k3_ = min(k3 + {self.kernel_size}, in0shape3);\n                                int k2_ = min(k2 + {self.kernel_size}, in0shape2);\n                                k3 = max(0, k3);\n                                k2 = max(0, k2);\n                                @out(i0, i1, i2, i3) = @in0(i0, i1, k2, k3);\n                                for (int p = k2; p < k2_; ++p)\n                                    for (int q = k3; q < k3_; ++q)\n                                        @out(i0, i1, i2, i3) = {op}(@out(i0, i1, i2, i3), @in0(i0, i1, p, q));\n                            }}\n                    }}\n                    int tx = min(1024, outshape3);\n                    int ty = min(1024 / tx, outshape2);\n                    int bx = (outshape2 - 1) / ty + 1;\n                    int by = outshape1;\n                    int bz = outshape0;\n                    dim3 s1(bx, by, bz);\n                    dim3 s2(tx, ty);\n                    kernel1<<<s1, s2>>>(@ARGS);\n                ",
              cuda_grad_src=[
             f"\n                    __global__ static void kernel3(@ARGS_DEF) {{\n                        @PRECALC\n                        int p3 = threadIdx.x;\n                        int s3 = blockDim.x;\n                        int p2 = threadIdx.y + blockIdx.x * blockDim.y;\n                        int s2 = blockDim.y * gridDim.x;\n                        int i1 = blockIdx.y;\n                        int i0 = blockIdx.z;\n                        for (int i3 = p3; i3 < poutshape3; i3 += s3)\n                            for (int i2 = p2; i2 < poutshape2; i2 += s2) {{\n                                int k3 = i3*{self.stride}-{self.padding};\n                                int k2 = i2*{self.stride}-{self.padding};\n                                int k3_ = min(k3 + {self.kernel_size}, in0shape3);\n                                int k2_ = min(k2 + {self.kernel_size}, in0shape2);\n                                k3 = max(0, k3);\n                                k2 = max(0, k2);\n                                int bo=1;\n                                for (int p = k2; p < k2_ && bo; ++p)\n                                    for (int q = k3; q < k3_ && bo; ++q) {{\n                                        if (@pout(i0,i1,i2,i3) == @in0(i0,i1,p,q)) {{\n                                            atomicAdd(&@out(i0,i1,p,q), @dout(i0,i1,i2,i3));\n                                            bo=0;\n                                        }}\n                                    }}\n                            }}\n                    }}\n                    cudaMemsetAsync(outp, 0, out->size);\n                    int tx = min(1024, poutshape3);\n                    int ty = min(1024 / tx, poutshape2);\n                    int bx = (poutshape2 - 1) / ty + 1;\n                    int by = poutshape1;\n                    int bz = poutshape0;\n                    dim3 s1_(bx, by, bz);\n                    dim3 s2_(tx, ty);\n                    kernel3<<<s1_, s2_>>>(@ARGS);\n                "],
              cpu_src=f"\n                    for (int i0=0; i0<outshape0; i0++)\n                    for (int i1=0; i1<outshape1; i1++)\n                    for (int i2=0; i2<outshape2; i2++)\n                    for (int i3=0; i3<outshape3; i3++) {{\n                        int k2 = i2*{self.stride}-{self.padding};\n                        int k3 = i3*{self.stride}-{self.padding};\n                        int k2_ = std::min(k2 + {self.kernel_size}, in0shape2);\n                        int k3_ = std::min(k3 + {self.kernel_size}, in0shape3);\n                        k2 = std::max(0, k2);\n                        k3 = std::max(0, k3);\n                        @out(i0, i1, i2, i3) = @in0(i0, i1, k2, k3);\n                        for (int p = k2; p < k2_; ++p)\n                            for (int q = k3; q < k3_; ++q)\n                                @out(i0, i1, i2, i3) = std::{op}(@out(i0, i1, i2, i3), @in0(i0, i1, p, q));\n                    }}\n                ",
              cpu_grad_src=[
             f"\n                    for (int i=0; i<outshape0; i++)\n                    for (int j=0; j<outshape1; j++)\n                    for (int k=0; k<outshape2; k++)\n                    for (int l=0; l<outshape3; l++) @out(i,j,k,l) = 0;\n\n                    for (int i0=0; i0<poutshape0; i0++)\n                    for (int i1=0; i1<poutshape1; i1++)\n                    for (int i2=0; i2<poutshape2; i2++) \n                    for (int i3=0; i3<poutshape3; i3++) {{\n                        int k3 = i3*{self.stride}-{self.padding};\n                        int k2 = i2*{self.stride}-{self.padding};\n                        int k3_ = std::min(k3 + {self.kernel_size}, in0shape3);\n                        int k2_ = std::min(k2 + {self.kernel_size}, in0shape2);\n                        k3 = std::max(0, k3);\n                        k2 = std::max(0, k2);\n                        int bo=1;\n                        for (int p = k2; p < k2_ && bo; ++p)\n                            for (int q = k3; q < k3_ && bo; ++q) {{\n                                if (@pout(i0,i1,i2,i3) == @in0(i0,i1,p,q)) {{\n                                    @out(i0,i1,p,q) += @dout(i0,i1,i2,i3);\n                                    bo=0;\n                                }}\n                            }}\n                    }}\n                "])
            return out
        xx = x.reindex([N, C, h, w, self.kernel_size, self.kernel_size], [
         'i0',
         'i1',
         f"i2*{self.stride}-{self.padding}+i4",
         f"i3*{self.stride}-{self.padding}+i5"])
        return xx.reduce(self.op, [4, 5])


def pool(x, size, op, padding, stride=1):
    return Pool(size, stride, padding, op=op)(x)