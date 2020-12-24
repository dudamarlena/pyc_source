# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\python362\Lib\site-packages\novainstrumentation\tests\test_tools.py
# Compiled at: 2017-03-06 22:19:14
# Size of source mod 2**32: 913 bytes
import os, numpy, novainstrumentation
from novainstrumentation import load_with_cache
from sklearn.utils.testing import assert_array_almost_equal, assert_true, assert_less
base_dir = os.path.dirname(novainstrumentation.__file__)

def test_load_with_cache():
    fname = base_dir + '/code/data/bvp.txt'
    fname_npy = fname + '.npy'
    direct_d = numpy.loadtxt(fname)
    cache_d = load_with_cache(fname, data_type='float')
    assert_array_almost_equal(direct_d, cache_d, decimal=5)
    assert_true(os.path.exists(fname_npy))
    assert_less(os.path.getsize(fname_npy), os.path.getsize(fname))
    os.remove(fname_npy)


def test_fail():
    assert False