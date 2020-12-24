# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_custom_op.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 2844 bytes
import unittest, os, jittor as jt
from .test_core import expect_error
header = '\n#pragma once\n#include "op.h"\n\nnamespace jittor {\n\nstruct CustomOp : Op {\n    Var* output;\n    CustomOp(NanoVector shape, NanoString dtype=ns_float);\n    \n    const char* name() const override { return "custom"; }\n    DECLARE_jit_run;\n};\n\n} // jittor\n'
src = '\n#include "var.h"\n#include "custom_op.h"\n\nnamespace jittor {\n#ifndef JIT\nCustomOp::CustomOp(NanoVector shape, NanoString dtype) {\n    output = create_output(shape, dtype);\n}\n\nvoid CustomOp::jit_prepare() {\n    add_jit_define("T", output->dtype());\n}\n\n#else // JIT\n#ifdef JIT_cpu\nvoid CustomOp::jit_run() {\n    index_t num = output->num;\n    auto* __restrict__ x = output->ptr<T>();\n    for (index_t i=0; i<num; i++)\n        x[i] = (T)i;\n}\n#else\nvoid CustomOp::jit_run() {\n}\n#endif // JIT_cpu\n#endif // JIT\n\n} // jittor\n'

class TestCustomOp(unittest.TestCase):

    def test_compile_custom_ops(self):
        tmp_path = jt.flags.cache_path
        hname = tmp_path + '/custom_op.h'
        ccname = tmp_path + '/custom_op.cc'
        with open(hname, 'w') as (f):
            f.write(header)
        with open(ccname, 'w') as (f):
            f.write(src)
        cops = jt.compile_custom_ops([hname, ccname])
        a = cops.custom([3, 4, 5], 'float')
        na = a.data
        if not (a.shape == [3, 4, 5] and a.dtype == 'float'):
            raise AssertionError
        assert (na.flatten() == range(60)).all(), na

    def test_compile_custom_op(self):
        my_op = jt.compile_custom_op('\n        struct MyOp : Op {\n            Var* output;\n            MyOp(NanoVector shape, NanoString dtype=ns_float);\n            \n            const char* name() const override { return "my"; }\n            DECLARE_jit_run;\n        };\n        ', '\n        #ifndef JIT\n        MyOp::MyOp(NanoVector shape, NanoString dtype) {\n            output = create_output(shape, dtype);\n        }\n\n        void MyOp::jit_prepare() {\n            add_jit_define("T", output->dtype());\n        }\n\n        #else // JIT\n        void MyOp::jit_run() {\n            index_t num = output->num;\n            auto* __restrict__ x = output->ptr<T>();\n            for (index_t i=0; i<num; i++)\n                x[i] = (T)-i;\n        }\n        #endif // JIT\n        ', 'my')
        a = my_op([3, 4, 5], 'float')
        na = a.data
        if not (a.shape == [3, 4, 5] and a.dtype == 'float'):
            raise AssertionError
        assert (-na.flatten() == range(60)).all(), na


if __name__ == '__main__':
    unittest.main()