# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/haoxun/Data/Project/pyenv-mirror-download/tests/test_main.py
# Compiled at: 2016-03-31 00:37:40
# Size of source mod 2**32: 267 bytes
from __future__ import division, absolute_import, print_function, unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pyenv_mirror_download.main import entry_point

def test_entry_point():
    @py_assert0 = 42
    @py_assert4 = entry_point()
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s()\n}', ), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(entry_point) if 'entry_point' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(entry_point) else 'entry_point', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None