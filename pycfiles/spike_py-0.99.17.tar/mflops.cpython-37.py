# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/v2/mflops.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 2180 bytes
"""
This script computes the speed of the processing in MFlops.
It is adapted from the FFTW page (see http://www.fftw.org/speed/ )

The FT used inside NPK is not based on FFTW, but rather inspired from Numerical Recipes :
The Art of Scientific Computing, first edition.

It is a mixed of single precision and double precision code, and has not been optimized for speed, nor for smal data-sets.
As NPK does not directly implement regular complex FT, a fake hypercomplex FT is used to time the processing.
"""
from __future__ import print_function
import time, math
from v1 import *

def l2(x):
    return math.log(x) / math.log(2)


def doit():
    stat = 32
    stat_time = 4.0
    liste = ((32, 32), (64, 64), (16, 512), (128, 128), (512, 64), (64, 1024), (256, 256),
             (512, 512), (1024, 1024), (2048, 2048))
    for N, M in liste:
        K.dim(2)
        K.chsize(2 * N, 2 * M)
        K.itype(3)
        print(K.get_itype_2d())
        K.addnoise(123, 234)
        K.ft('F2')
        K.ft('F1')
        K.put('data')
        t = time.time()
        for i in range(stat):
            K.get('data')
            K.ft('F2')
            K.ft('F1')

        tt = time.time() - t
        try:
            mflop = 10.0 * N * M * l2(2 * N * M) * stat / (tt * 1000000.0)
        except:
            mflop = 0

        try:
            mean += mflop
        except:
            mean = mflop

        print('2D FT : %d x %d :\t%d Mflops' % (N, M, mflop))
        if tt > stat_time and stat > 2:
            stat = stat / 2

    print('Mean MFlops value : %d' % (mean / len(liste)))


prof_file = 'profile2.dump'
import pstats
st = pstats.Stats(prof_file)
st.strip_dirs()
st.sort_stats('time')
st.print_stats()