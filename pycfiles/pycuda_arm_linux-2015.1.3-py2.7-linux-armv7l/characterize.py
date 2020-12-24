# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/pycuda/characterize.py
# Compiled at: 2015-06-16 13:16:13
from __future__ import division
from __future__ import absolute_import
from pycuda.tools import context_dependent_memoize
import numpy as np

def platform_bits():
    return tuple.__itemsize__ * 8


def has_stack():
    from pycuda.driver import Context
    return Context.get_device().compute_capability() >= (2, 0)


def has_double_support():
    from pycuda.driver import Context
    return Context.get_device().compute_capability() >= (1, 3)


@context_dependent_memoize
def sizeof(type_name, preamble=''):
    from pycuda.compiler import SourceModule
    mod = SourceModule('\n    %s\n    extern "C"\n    __global__ void write_size(size_t *output)\n    {\n      *output = sizeof(%s);\n    }\n    ' % (preamble, type_name), no_extern_c=True)
    import pycuda.gpuarray as gpuarray
    output = gpuarray.empty((), dtype=np.uintp)
    mod.get_function('write_size')(output, block=(1, 1, 1), grid=(1, 1))
    return int(output.get())