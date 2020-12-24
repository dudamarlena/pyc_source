# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lukas/work/development/gridcells/external/numpydoc/numpydoc/tests/test_plot_directive.py
# Compiled at: 2014-03-29 16:39:55
# Size of source mod 2**32: 322 bytes
from __future__ import division, absolute_import, print_function
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, sys
from nose import SkipTest

def test_import():
    if sys.version_info[0] >= 3:
        raise SkipTest('plot_directive not ported to Python 3 (use the one from Matplotlib instead)')
    import numpydoc.plot_directive