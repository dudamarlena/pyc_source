# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_code_op.py
# Compiled at: 2020-03-26 09:27:39
# Size of source mod 2**32: 5536 bytes
import unittest, jittor as jt, numpy as np

class TestCodeOp(unittest.TestCase):

    def test(self):
        a = jt.random([10])
        b = jt.code((a.shape), (a.dtype), [a], cpu_src='\n                for (int i=0; i<in0shape0; i++)\n                    @out(i) = @in0(i)*@in0(i)*2;\n            ',
          cpu_grad_src=[
         '\n                for (int i=0; i<in0shape0; i++) {\n                    @out(i) = @dout(i)*@in0(i)*4;\n                }\n            '])
        na, nb = jt.fetch_sync([a, b])
        assert np.allclose(na * na * 2, nb)
        c = jt.random([10])
        da = jt.grad(c * b, a)
        assert np.allclose(c.data * na * 4, da.data), (c.data * na * 4, da.data)

    def test_multi_input(self):
        a = jt.random([10])
        b = jt.random([10])
        c = jt.code((a.shape), (a.dtype), [a, b], cpu_src='\n                for (int i=0; i<in0shape0; i++)\n                    @out(i) = @in0(i)*@in1(i);\n            ',
          cpu_grad_src=[
         '\n                for (int i=0; i<in0shape0; i++) {\n                    @out(i) = @dout(i)*@in1(i);\n                }\n            ',
         '\n                for (int i=0; i<in0shape0; i++) {\n                    @out(i) = @dout(i)*@in0(i);\n                }\n            '])
        da, db = jt.grad(c, [a, b])
        assert np.allclose(c.data, a.data * b.data), (c.data, a.data * b.data)
        assert np.allclose(da.data, b.data)
        assert np.allclose(db.data, a.data)

    def test_header(self):
        a = jt.array([3, 2, 1])
        b = jt.code((a.shape), (a.dtype), [a], cpu_header='#include <algorithm>',
          cpu_src='\n                for (int i=0; i<in0shape0; i++)\n                    @out(i) = @in0(i);\n                std::sort(&@out(0), &@out(in0shape0));\n            ')
        assert (b.data == [1, 2, 3]).all()

    @unittest.skipIf(not jt.compiler.has_cuda, 'No CUDA found')
    @jt.flag_scope(use_cuda=1)
    def test_cuda(self):
        a = jt.random([100000])
        b = jt.random([100000])
        c = jt.code((a.shape), (a.dtype), [a, b], cuda_src='\n            __global__ static void kernel1(@ARGS_DEF) {\n                @PRECALC\n                int i = threadIdx.x + blockIdx.x * blockDim.x;\n                int stride = blockDim.x * gridDim.x;\n                for (; i<in0shape0; i+=stride)\n                    @out(i) = @in0(i)*@in1(i);\n            }\n                kernel1<<<(in0shape0-1)/1024+1, 1024>>>(@ARGS);\n            ',
          cuda_grad_src=[
         '\n            __global__ static void kernel2(@ARGS_DEF) {\n                @PRECALC\n                int i = threadIdx.x + blockIdx.x * blockDim.x;\n                int stride = blockDim.x * gridDim.x;\n                for (; i<in0shape0; i+=stride)\n                    @out(i) = @dout(i)*@in1(i);\n            }\n                kernel2<<<(in0shape0-1)/1024+1, 1024>>>(@ARGS);\n            ',
         '\n            __global__ static void kernel3(@ARGS_DEF) {\n                @PRECALC\n                int i = threadIdx.x + blockIdx.x * blockDim.x;\n                int stride = blockDim.x * gridDim.x;\n                for (; i<in0shape0; i+=stride)\n                    @out(i) = @dout(i)*@in0(i);\n            }\n                kernel3<<<(in0shape0-1)/1024+1, 1024>>>(@ARGS);\n            '])
        da, db = jt.grad(c, [a, b])
        assert np.allclose(c.data, a.data * b.data), (c.data, a.data * b.data)
        assert np.allclose(da.data, b.data)
        assert np.allclose(db.data, a.data)

    @unittest.skipIf(not jt.compiler.has_cuda, 'No CUDA found')
    @jt.flag_scope(use_cuda=1)
    def test_cuda2(self):
        a = jt.random((100, 100))
        b = jt.random((100, 100))
        c = jt.code((a.shape), (a.dtype), [a, b], cuda_src='\n                __global__ static void kernel1(@ARGS_DEF) {\n                    @PRECALC\n                    for (int i=blockIdx.x; i<in0shape0; i+=gridDim.x)\n                    for (int j=threadIdx.x; j<in0shape1; j+=blockDim.x)\n                        @out(i,j) = @in0(i,j)*@in1(i,j);\n                }\n                kernel1<<<32, 32>>>(@ARGS);\n            ',
          cuda_grad_src=[
         '\n                __global__ static void kernel(@ARGS_DEF) {\n                    @PRECALC\n                    for (int i=blockIdx.x; i<in0shape0; i+=gridDim.x)\n                    for (int j=threadIdx.x; j<in0shape1; j+=blockDim.x)\n                        @out(i,j) = @dout(i,j)*@in1(i,j);\n                }\n                kernel<<<32, 32>>>(@ARGS);\n            ',
         '\n                __global__ static void kernel(@ARGS_DEF) {\n                    @PRECALC\n                    @pout(0,0);\n                    for (int i=blockIdx.x; i<in0shape0; i+=gridDim.x)\n                    for (int j=threadIdx.x; j<in0shape1; j+=blockDim.x)\n                        @out(i,j) = @dout(i,j)*@in0(i,j);\n                }\n                kernel<<<32, 32>>>(@ARGS);\n            '])
        da, db = jt.grad(c, [a, b])
        assert np.allclose(c.data, a.data * b.data), (c.data, a.data * b.data)
        assert np.allclose(da.data, b.data)
        assert np.allclose(db.data, a.data)


if __name__ == '__main__':
    unittest.main()