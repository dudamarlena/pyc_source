# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/implicit/utils.py
# Compiled at: 2019-10-24 03:58:04
# Size of source mod 2**32: 1210 bytes
import logging, os, numpy as np

def nonzeros(m, row):
    """ returns the non zeroes of a row in csr_matrix """
    for index in range(m.indptr[row], m.indptr[(row + 1)]):
        yield (
         m.indices[index], m.data[index])


_checked_blas_config = False

def check_blas_config():
    """ checks to see if using OpenBlas/Intel MKL. If so, warn if the number of threads isn't set
    to 1 (causes severe perf issues when training - can be 10x slower) """
    global _checked_blas_config
    if _checked_blas_config:
        return
    else:
        _checked_blas_config = True
        if np.__config__.get_info('openblas_info'):
            if os.environ.get('OPENBLAS_NUM_THREADS') != '1':
                logging.warning("OpenBLAS detected. Its highly recommend to set the environment variable 'export OPENBLAS_NUM_THREADS=1' to disable its internal multithreading")
        if np.__config__.get_info('blas_mkl_info') and os.environ.get('MKL_NUM_THREADS') != '1':
            logging.warning("Intel MKL BLAS detected. Its highly recommend to set the environment variable 'export MKL_NUM_THREADS=1' to disable its internal multithreading")