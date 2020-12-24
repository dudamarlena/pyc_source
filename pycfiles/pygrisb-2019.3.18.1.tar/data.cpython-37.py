# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ykent/GitLab/pygrisb/pygrisb/pygrisb/basic/data.py
# Compiled at: 2019-02-22 23:25:00
# Size of source mod 2**32: 259 bytes
import h5py, numpy

def compare_array(path, fname1='GLOG.h5', fname2='GLOG_REF.h5'):
    with h5py.File(fname1, 'r') as (f):
        data1 = f[path][()]
    with h5py.File(fname2, 'r') as (f):
        data2 = f[path][()]
    return numpy.allclose(data1, data2)