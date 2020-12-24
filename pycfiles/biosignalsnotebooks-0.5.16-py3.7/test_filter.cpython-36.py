# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\python362\Lib\site-packages\novainstrumentation\tests\test_filter.py
# Compiled at: 2017-03-06 22:19:14
# Size of source mod 2**32: 1005 bytes
import os, numpy, novainstrumentation, novainstrumentation as ni
from scipy import signal
from sklearn.utils.testing import assert_array_almost_equal, assert_true, assert_less
base_dir = os.path.dirname(novainstrumentation.__file__)

def test_emg_filter_params():
    fname = base_dir + '/code/data/emg.txt'
    t, emg = numpy.loadtxt(fname)
    env_ni = ni.lowpass((abs(emg)), order=2, f=10, fs=1000)
    b, a = signal.butter(2, Wn=0.02)
    env_ref = signal.lfilter(b, a, abs(emg))
    assert_array_almost_equal(env_ni, env_ref)


def test_emg_filter_values():
    f_name = base_dir + '/code/data/emg.txt'
    t, emg = numpy.loadtxt(f_name)
    env_ni = ni.lowpass((abs(emg)), order=2, f=10, fs=1000.0)
    b, a = signal.butter(2, Wn=0.02)
    env_ref = signal.lfilter(b, a, abs(emg))
    assert_array_almost_equal(env_ni, env_ref)