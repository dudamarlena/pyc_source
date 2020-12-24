# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/haoxun/Data/Project/magic_parameter/tests/test_utils.py
# Compiled at: 2016-04-17 00:01:15
# Size of source mod 2**32: 582 bytes
from __future__ import division, absolute_import, print_function, unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from builtins import *
from future.builtins.disabled import *
import pytest
from magic_parameter.utils import *
injected = 1

def test_injection():

    def func():
        @py_assert2 = 42
        @py_assert1 = injected == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (injected, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(injected) if 'injected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(injected) else 'injected'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    with pytest.raises(AssertionError):
        func()
    records = inject_globals(func, [('injected', 42)])
    func()
    restore_globals(func, records)
    with pytest.raises(AssertionError):
        func()