# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_cuda.py
# Compiled at: 2020-04-11 06:08:16
# Size of source mod 2**32: 3507 bytes
import unittest, jittor as jt
from .test_core import expect_error

def test_cuda(use_cuda=1):

    @unittest.skipIf(not jt.compiler.has_cuda, 'No CUDA found')
    class TestCudaBase(unittest.TestCase):

        def setUp(self):
            jt.flags.use_cuda = use_cuda

        def tearDown(self):
            jt.flags.use_cuda = 0

    return TestCudaBase


@unittest.skipIf(not jt.compiler.has_cuda, 'No CUDA found')
class TestCuda(unittest.TestCase):

    @jt.flag_scope(use_cuda=1)
    def test_cuda_flags(self):
        a = jt.random((10, 10))
        a.sync()

    @jt.flag_scope(use_cuda=2)
    def test_no_cuda_op(self):
        no_cuda_op = jt.compile_custom_op('\n        struct NoCudaOp : Op {\n            Var* output;\n            NoCudaOp(NanoVector shape, string dtype="float");\n            \n            const char* name() const override { return "my_cuda"; }\n            DECLARE_jit_run;\n        };\n        ', '\n        #ifndef JIT\n        NoCudaOp::NoCudaOp(NanoVector shape, string dtype) {\n            flags.set(NodeFlags::_cpu);\n            output = create_output(shape, dtype);\n        }\n\n        void NoCudaOp::jit_prepare() {\n            add_jit_define("T", output->dtype());\n        }\n\n        #else // JIT\n        void NoCudaOp::jit_run() {}\n        #endif // JIT\n        ', 'no_cuda')
        a = no_cuda_op([3, 4, 5], 'float')
        expect_error(lambda : a())

    @jt.flag_scope(use_cuda=1)
    def test_cuda_custom_op(self):
        my_op = jt.compile_custom_op('\n        struct MyCudaOp : Op {\n            Var* output;\n            MyCudaOp(NanoVector shape, string dtype="float");\n            \n            const char* name() const override { return "my_cuda"; }\n            DECLARE_jit_run;\n        };\n        ', '\n        #ifndef JIT\n        MyCudaOp::MyCudaOp(NanoVector shape, string dtype) {\n            flags.set(NodeFlags::_cuda);\n            output = create_output(shape, dtype);\n        }\n\n        void MyCudaOp::jit_prepare() {\n            add_jit_define("T", output->dtype());\n        }\n\n        #else // JIT\n        #ifdef JIT_cuda\n\n        __global__ void kernel(index_t n, T *x) {\n            int index = blockIdx.x * blockDim.x + threadIdx.x;\n            int stride = blockDim.x * gridDim.x;\n            for (int i = index; i < n; i += stride)\n                x[i] = (T)-i;\n        }\n\n        void MyCudaOp::jit_run() {\n            index_t num = output->num;\n            auto* __restrict__ x = output->ptr<T>();\n            int blockSize = 256;\n            int numBlocks = (num + blockSize - 1) / blockSize;\n            kernel<<<numBlocks, blockSize>>>(num, x);\n        }\n        #endif // JIT_cuda\n        #endif // JIT\n        ', 'my_cuda')
        a = my_op([3, 4, 5], 'float')
        na = a.data
        if not (a.shape == [3, 4, 5] and a.dtype == 'float'):
            raise AssertionError
        assert (-na.flatten() == range(60)).all(), na


@unittest.skipIf(jt.compiler.has_cuda, 'Only test without CUDA')
class TestNoCuda(unittest.TestCase):

    def test_cuda_flags(self):
        expect_error(lambda : setattr(jt.flags, 'use_cuda', 1))


if __name__ == '__main__':
    unittest.main()