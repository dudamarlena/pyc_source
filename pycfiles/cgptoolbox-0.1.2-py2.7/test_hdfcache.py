# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\test\test_hdfcache.py
# Compiled at: 2013-01-14 06:47:43
"""Tests for :mod:`cgp.utils.hdfcache`."""
import os, tempfile, numpy as np
from cgp.utils.hdfcache import Hdfcache
dtemp = None

def setup():
    global dtemp
    dtemp = tempfile.mkdtemp()


def teardown():
    import shutil
    try:
        shutil.rmtree(dtemp)
    except OSError:
        pass


def test_hdfcache():
    filename = os.path.join(dtemp, 'cachetest.h5')
    hdfcache = Hdfcache(filename)

    @hdfcache.cache
    def f(x, a, b=10):
        """This is the docstring for function f"""
        result = np.zeros(1, dtype=[('y', float)])
        result['y'] = x['i'] * 2 + x['f'] + a * b
        print 'Evaluating f:', x, a, b, '=>', result
        return result

    desired = '@hdfcache.cache\ndef f(x, a, b=10):'
    actual = ('\n').join(line.strip() for line in hdfcache.file.root.f._v_attrs.sourcecode.split('\n'))
    np.testing.assert_string_equal(actual[:len(desired)], desired)
    desired = __file__.replace('.pyc', '.py')
    actual = hdfcache.file.root.f._v_attrs.sourcefile
    np.testing.assert_string_equal(actual[-len(desired):], desired)