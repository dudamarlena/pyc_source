# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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