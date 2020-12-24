# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\biosignalsnotebooks\external_packages\novainstrumentation\tests\test_smooth.py
# Compiled at: 2020-03-23 15:40:39
# Size of source mod 2**32: 317 bytes
from numpy import arange
from novainstrumentation import smooth
from numpy.testing import assert_allclose, run_module_suite

def test_symmetric_window():
    x = arange(1.0, 11.0)
    sx = smooth(x, window_len=5, window='flat')
    assert_allclose(x, sx)


if __name__ == '__main__':
    run_module_suite()