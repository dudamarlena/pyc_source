# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cuda_functions/core.py
# Compiled at: 2017-09-08 03:03:55
# Size of source mod 2**32: 1780 bytes
from cuda_functions.bin import gpu_correlate_dp, gpu_correlate_sp, gpu_correlate_spc, gpu_correlate_dpc
from cuda_functions.bin import gpu_fft_dpc, gpu_fft_spc
import numpy as np, warnings

def cuda_acorrelate(array, mode='valid', safe_mode=True):
    if safe_mode:
        array = np.ascontiguousarray(array)
    if array.dtype == 'complex64':
        return gpu_correlate_spc.acorrelate(array, mode=mode)
    else:
        if array.dtype == 'complex128':
            return gpu_correlate_dpc.acorrelate(array, mode=mode)
        if array.dtype == 'float32':
            return gpu_correlate_sp.acorrelate(array, mode=mode)
        if array.dtype == 'float64':
            return gpu_correlate_dp.acorrelate(array, mode=mode)
        warnings.warn('{} type not supported, it will be converted to complex128'.format(array.dtype))
        return gpu_correlate_dpc.acorrelate(np.array(array, dtype='complex128'), mode=mode)


def cuda_fft(array, safe_mode=True):
    if safe_mode:
        array = np.ascontiguousarray(array)
    if array.dtype == 'complex64':
        return gpu_fft_spc.fft(array)
    else:
        if array.dtype == 'complex128':
            return gpu_fft_dpc.fft(array)
        warnings.warn('{} type not supported, it will be converted to complex128'.format(array.dtype))
        return gpu_fft_dpc.fft(np.array(array, dtype='complex128'))


def cuda_ifft(array, safe_mode=True):
    if safe_mode:
        array = np.ascontiguousarray(array)
    if array.dtype == 'complex64':
        return gpu_fft_spc.ifft(array)
    else:
        if array.dtype == 'complex128':
            return gpu_fft_dpc.ifft(array)
        warnings.warn('{} type not supported, it will be converted to complex128'.format(array.dtype))
        return gpu_fft_dpc.ifft(np.array(array, dtype='complex128'))