# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/plugins/bcorr.py
# Compiled at: 2020-01-11 10:17:51
# Size of source mod 2**32: 6911 bytes
"""set of function for the baseline correction

First version - Not finished !

improved July 2016
"""
from __future__ import print_function, division
import numpy as np
from scipy import interpolate
from scipy.optimize import leastsq
from spike import NPKError
from spike.NPKData import NPKData_plugin
import sys
if sys.version_info[0] < 3:
    pass
else:
    xrange = range

def get_ypoints(buff, xpoints, nsmooth=0):
    """
    from  buff and xpoints, returns ypoints = buff[xpoints]
    eventually smoothed by moving average over 2*nsmooth+1 positions
    """
    nsmooth = abs(nsmooth)
    xp = np.array(xpoints).astype(int)
    y = np.zeros(len(xpoints))
    for i in range(2 * nsmooth + 1):
        xi = np.minimum(np.maximum(xp - i, 0), len(buff) - 1)
        y += buff[xi]

    y /= 2 * nsmooth + 1
    return y


def _spline_interpolate(buff, xpoints, kind=3, nsmooth=0):
    """compute and returns a spline function 
        we are using splrep and splev instead of interp1d because interp1d needs to have 0 and last point
        it doesn't extend.
    """
    if len(xpoints) == 2:
        return _linear_interpolate(buff, xpoints)
    if len(xpoints) > 2:
        xpoints.sort()
        y = get_ypoints(buff, xpoints, nsmooth=nsmooth)
        tck = interpolate.splrep(xpoints, y, k=kind)

        def f(x):
            return interpolate.splev(x, tck, der=0, ext=0)

        return f
    raise NPKError('too little points in spline interpolation')


def _linear_interpolate(buff, xpoints, nsmooth=0):
    """computes and returns a linear interpolation"""
    xdata = np.array(xpoints)
    ydata = get_ypoints(buff, xpoints, nsmooth=nsmooth)
    coeffs = np.polyfit(xdata, ydata, 1)
    return np.poly1d(coeffs)


def _interpolate--- This code section failed: ---

 L.  68         0  LOAD_FAST                'npkd'
                2  LOAD_ATTR                dim
                4  LOAD_CONST               1
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    58  'to 58'

 L.  69        10  LOAD_FAST                'func'
               12  LOAD_FAST                'npkd'
               14  LOAD_ATTR                buffer
               16  LOAD_FAST                'xpoints'
               18  LOAD_FAST                'nsmooth'
               20  LOAD_CONST               ('nsmooth',)
               22  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               24  STORE_FAST               'f'

 L.  70        26  LOAD_GLOBAL              np
               28  LOAD_METHOD              arange
               30  LOAD_FAST                'npkd'
               32  LOAD_ATTR                size1
               34  CALL_METHOD_1         1  '1 positional argument'
               36  STORE_FAST               'x'

 L.  71        38  LOAD_FAST                'npkd'
               40  DUP_TOP          
               42  LOAD_ATTR                buffer
               44  LOAD_FAST                'f'
               46  LOAD_FAST                'x'
               48  CALL_FUNCTION_1       1  '1 positional argument'
               50  INPLACE_SUBTRACT 
               52  ROT_TWO          
               54  STORE_ATTR               buffer
               56  JUMP_FORWARD        292  'to 292'
             58_0  COME_FROM             8  '8'

 L.  72        58  LOAD_FAST                'npkd'
               60  LOAD_ATTR                dim
               62  LOAD_CONST               2
               64  COMPARE_OP               ==
            66_68  POP_JUMP_IF_FALSE   284  'to 284'

 L.  73        70  LOAD_FAST                'npkd'
               72  LOAD_METHOD              test_axis
               74  LOAD_FAST                'axis'
               76  CALL_METHOD_1         1  '1 positional argument'
               78  LOAD_CONST               2
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE   176  'to 176'

 L.  74        84  LOAD_GLOBAL              np
               86  LOAD_METHOD              arange
               88  LOAD_FAST                'npkd'
               90  LOAD_ATTR                size2
               92  CALL_METHOD_1         1  '1 positional argument'
               94  STORE_FAST               'x'

 L.  75        96  SETUP_LOOP          282  'to 282'
               98  LOAD_GLOBAL              xrange
              100  LOAD_FAST                'npkd'
              102  LOAD_ATTR                size1
              104  CALL_FUNCTION_1       1  '1 positional argument'
              106  GET_ITER         
              108  FOR_ITER            172  'to 172'
              110  STORE_FAST               'i'

 L.  76       112  LOAD_FAST                'func'
              114  LOAD_FAST                'npkd'
              116  LOAD_ATTR                buffer
              118  LOAD_FAST                'i'
              120  LOAD_CONST               None
              122  LOAD_CONST               None
              124  BUILD_SLICE_2         2 
              126  BUILD_TUPLE_2         2 
              128  BINARY_SUBSCR    
              130  LOAD_FAST                'xpoints'
              132  LOAD_FAST                'nsmooth'
              134  LOAD_CONST               ('nsmooth',)
              136  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              138  STORE_FAST               'f'

 L.  77       140  LOAD_FAST                'npkd'
              142  LOAD_ATTR                buffer
              144  LOAD_FAST                'i'
              146  LOAD_CONST               None
              148  LOAD_CONST               None
              150  BUILD_SLICE_2         2 
              152  BUILD_TUPLE_2         2 
              154  DUP_TOP_TWO      
              156  BINARY_SUBSCR    
              158  LOAD_FAST                'f'
              160  LOAD_FAST                'x'
              162  CALL_FUNCTION_1       1  '1 positional argument'
              164  INPLACE_SUBTRACT 
              166  ROT_THREE        
              168  STORE_SUBSCR     
              170  JUMP_BACK           108  'to 108'
              172  POP_BLOCK        
              174  JUMP_FORWARD        282  'to 282'
            176_0  COME_FROM            82  '82'

 L.  78       176  LOAD_FAST                'npkd'
              178  LOAD_METHOD              test_axis
              180  LOAD_FAST                'axis'
              182  CALL_METHOD_1         1  '1 positional argument'
              184  LOAD_CONST               1
              186  COMPARE_OP               ==
          188_190  POP_JUMP_IF_FALSE   292  'to 292'

 L.  79       192  LOAD_GLOBAL              np
              194  LOAD_METHOD              arange
              196  LOAD_FAST                'npkd'
              198  LOAD_ATTR                size1
              200  CALL_METHOD_1         1  '1 positional argument'
              202  STORE_FAST               'x'

 L.  80       204  SETUP_LOOP          292  'to 292'
              206  LOAD_GLOBAL              xrange
              208  LOAD_FAST                'npkd'
              210  LOAD_ATTR                size2
              212  CALL_FUNCTION_1       1  '1 positional argument'
              214  GET_ITER         
              216  FOR_ITER            280  'to 280'
              218  STORE_FAST               'i'

 L.  81       220  LOAD_FAST                'func'
              222  LOAD_FAST                'npkd'
              224  LOAD_ATTR                buffer
              226  LOAD_CONST               None
              228  LOAD_CONST               None
              230  BUILD_SLICE_2         2 
              232  LOAD_FAST                'i'
              234  BUILD_TUPLE_2         2 
              236  BINARY_SUBSCR    
              238  LOAD_FAST                'xpoints'
              240  LOAD_FAST                'nsmooth'
              242  LOAD_CONST               ('nsmooth',)
              244  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              246  STORE_FAST               'f'

 L.  82       248  LOAD_FAST                'npkd'
              250  LOAD_ATTR                buffer
              252  LOAD_CONST               None
              254  LOAD_CONST               None
              256  BUILD_SLICE_2         2 
              258  LOAD_FAST                'i'
              260  BUILD_TUPLE_2         2 
              262  DUP_TOP_TWO      
              264  BINARY_SUBSCR    
              266  LOAD_FAST                'f'
              268  LOAD_FAST                'x'
              270  CALL_FUNCTION_1       1  '1 positional argument'
              272  INPLACE_SUBTRACT 
              274  ROT_THREE        
              276  STORE_SUBSCR     
              278  JUMP_BACK           216  'to 216'
              280  POP_BLOCK        
            282_0  COME_FROM_LOOP      204  '204'
            282_1  COME_FROM           174  '174'
            282_2  COME_FROM_LOOP       96  '96'
              282  JUMP_FORWARD        292  'to 292'
            284_0  COME_FROM            66  '66'

 L.  84       284  LOAD_GLOBAL              NPKError
              286  LOAD_STR                 'not implemented'
              288  CALL_FUNCTION_1       1  '1 positional argument'
              290  RAISE_VARARGS_1       1  'exception instance'
            292_0  COME_FROM           282  '282'
            292_1  COME_FROM           188  '188'
            292_2  COME_FROM            56  '56'

 L.  85       292  LOAD_FAST                'npkd'
              294  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 282_2


def linear_interpolate(npkd, xpoints, axis='F2', nsmooth=0):
    """"
    compute and applies a linear function as a baseline correction
    xpoints are the location of pivot points
    """
    return _interpolate(_linear_interpolate, npkd, xpoints, axis=axis, nsmooth=nsmooth)


def spline_interpolate(npkd, xpoints, axis='F2', nsmooth=0):
    """"
    compute and applies a spline function as a baseline correction
    xpoints are the location of pivot points
    """
    return _interpolate(_spline_interpolate, npkd, xpoints, axis=axis, nsmooth=nsmooth)


import spike.Algo.savitzky_golay as sgm
import spike.Algo.BC as BC

def bcorr_auto(npkd, iterations=10, nbchunks=40, degree=1, nbcores=2, smooth=True):
    """applies an automatic baseline correction
    
    Find baseline by using low norm value and then high norm value to attract the baseline on the small values.
    Parameters : 
    iterations : number of iterations for convergence toward the small values. 
    nbchunks : number of chunks on which is done the minimization. Typically, each chunk must be larger than the peaks. 
    degree : degree of the polynome used for approaching each signal chunk. 
    nbcores : number of cores used for minimizing in parallel on many chunks (if not None)
    
    smooth i True, applies a final Savitsky-Golay smoothing
    """
    npkd.check1D()
    bl = BC.correctbaseline((npkd.get_buffer()), iterations=iterations, nbchunks=nbchunks, degree=degree, nbcores=nbcores)
    if smooth:
        bl = sgm.savitzky_golay(bl, 205, 7)
    npkd.set_buffer(npkd.get_buffer() - bl)
    return npkd


def autopoints(npkd, Npoints=8):
    """
    computes Npoints (defaut 8) positions for a spline baseline correction
    """
    if Npoints is None:
        N = 8
    else:
        N = Npoints
    bf = npkd.get_buffer().copy()
    bf -= np.percentile(bf, 20)
    bf = abs(bf)
    L = len(bf)
    chunksize = L // N
    xpoints = np.array([i + bf[i:i + chunksize - 8].argmin() for i in range(4, L, chunksize)])
    if npkd.itype == 1:
        xpoints *= 2
    return xpoints


def bcorr(npkd, method='spline', xpoints=None, nsmooth=0):
    """
    recapitulate all baseline correction methods, only 1D so far
    
    method is either
        auto: 
            use bcorr_auto, uses an automatic determination of the baseline
            does not work with negative peaks.
        linear:
            simple 1D correction
        spline:
            a cubic spline correction
    both linear and spline use an additional list of pivot points 'xpoints' used to calculate the baseline
    if xpoints absent,  pivots are estimated automaticaly
    if xpoints is integer, it determines the number of computed pivots (defaut is 8 if xpoints is None)
    if xpoints is a list of integers, there will used as pivots

    if nsmooth >0, buffer is smoothed by moving average over 2*nsmooth+1 positions around pivots.
    default is spline with automatic detection of 8 baseline points
    """
    if method == 'auto':
        return bcorr_auto(npkd)
    if xpoints is None or isinstance(xpoints, int):
        xpoints = autopoints(npkd, xpoints)
    if method == 'linear':
        return linear_interpolate(npkd, xpoints, nsmooth=nsmooth)
    if method == 'spline':
        return spline_interpolate(npkd, xpoints, nsmooth=nsmooth)
    raise Exception('Wrong method in bcorr plugin')


NPKData_plugin('bcorr_lin', linear_interpolate)
NPKData_plugin('bcorr_spline', spline_interpolate)
NPKData_plugin('bcorr_auto', bcorr_auto)
NPKData_plugin('bcorr', bcorr)