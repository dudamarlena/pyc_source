# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/Miscellaneous/downsample.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 1881 bytes
"""
downsample2D.py

Created by MAD on 2011-04-14.
"""
from __future__ import print_function
import sys, os, numpy as np
from scipy.signal import decimate, lfilter, cheby1, medfilt, medfilt2d
from spike import NPKData

def downsample2D_med(data, n1=2, n2=2):
    """
    takes data (a 2D) and generate a smaller dataset downsampled by factor (n1,n2) on each axis
    the returned data-set is n1*n2 times smaller
    - simply takes the mean
    
    ** Not tested on non powers of 2 **
    
    """
    print('coucou1')
    cls = type(data)
    outp = cls(dim=2)
    if n1 > 1:
        yy = medfilt2d(data.buffer, (n1 + 1, n2 + 1))
        outp.buffer = yy[n1 / 2::n1, n2 / 2::n2]
    else:
        yy = medfilt2d(data.buffer, (1, n2 + 1))
        outp.buffer = yy[:, n2 / 2::n2]
    NPKData.copyaxes(data, outp)
    outp.adapt_size()
    return outp


def downsample2D(data, n1=2, n2=2):
    """
    takes data (a 2D) and generate a smaller dataset downsampled by factor (n1,n2) on each axis
    then returned data-set is n1*n2 times smaller
    - simply takes the mean
    
    ** Not tested on non powers of 2 **
    
    """
    print('coucou2')
    b1, a1 = cheby1(4, 0.05, 0.8 / n1)
    b2, a2 = cheby1(4, 0.05, 0.8 / n2)
    cls = type(data)
    outp = cls(buffer=(np.zeros((data.size1 / n1, data.size2 / n2))))
    for i in xrange(0, data.size1, n1):
        temp = np.zeros(data.size2 / n2)
        for j in xrange(n1):
            yy = lfilter(b2, a2, data.row(i + j).buffer)
            temp += yy[n2 / 2::n2]

        outp.buffer[i / n1, :] = 1.0 / n1 * temp

    NPKData.copyaxes(data, outp)
    outp.adapt_size()
    return outp


if __name__ == '__main__':
    main()