# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/medmad.py
# Compiled at: 2008-01-29 20:48:29
from medmadpyx import medmadpyx
import numpy as num

def medmad(filename, nframes, nr, nc, nframesskip, bytesperchunk, headersize):
    print 'headersize = %d' % headersize
    (medl, madl) = medmadpyx(filename, nframes, nr, nc, nframesskip, bytesperchunk, headersize)
    med = num.array(medl, copy=True)
    mad = num.array(madl, copy=True)
    print 'mad range = [%f,%f]' % (num.min(mad), num.max(mad))
    med.shape = (
     nr, nc)
    mad.shape = (nr, nc)
    return (
     med, mad)