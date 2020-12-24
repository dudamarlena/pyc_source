# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/james/Work/wide-product/build/lib.macosx-10.11-x86_64-2.7/wide_product/wide.py
# Compiled at: 2017-04-21 09:12:56
import numpy, scipy.sparse
from . import _wide

def wide_product(a, b):
    a = scipy.sparse.csr_matrix(a).astype('double')
    b = scipy.sparse.csr_matrix(b).astype('double')
    if a.shape[0] != b.shape[0]:
        raise ValueError('Matrices have different numbers of rows')
    height = a.shape[0]
    assert height + 1 == len(a.indptr)
    assert height + 1 == len(b.indptr)
    assert a.indices.dtype == 'int32'
    assert a.indptr.dtype == 'int32'
    assert b.indices.dtype == 'int32'
    assert b.indptr.dtype == 'int32'
    nnzsize = _wide.lib.wide_product_max_nnz(_wide.ffi.cast('wp_index*', a.indptr.ctypes.data), _wide.ffi.cast('wp_index*', b.indptr.ctypes.data), height)
    indptr = numpy.zeros(height + 1, dtype='int32')
    indices = numpy.zeros(nnzsize, dtype='int32')
    data = numpy.zeros(nnzsize, dtype='double')
    actual_nnz = _wide.lib.wide_product(height, _wide.ffi.cast('wp_number*', a.data.ctypes.data), _wide.ffi.cast('wp_index*', a.indices.ctypes.data), _wide.ffi.cast('wp_index*', a.indptr.ctypes.data), a.shape[1], len(a.data), _wide.ffi.cast('wp_number*', b.data.ctypes.data), _wide.ffi.cast('wp_index*', b.indices.ctypes.data), _wide.ffi.cast('wp_index*', b.indptr.ctypes.data), b.shape[1], len(b.data), _wide.ffi.cast('wp_number*', data.ctypes.data), _wide.ffi.cast('wp_index*', indices.ctypes.data), _wide.ffi.cast('wp_index*', indptr.ctypes.data))
    indices.resize(actual_nnz)
    data.resize(actual_nnz)
    return scipy.sparse.csr_matrix((
     data, indices, indptr), (
     height, a.shape[1] * b.shape[1]))