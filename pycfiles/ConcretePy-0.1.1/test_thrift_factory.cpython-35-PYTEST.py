# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/charman/src/concrete-python/tests/test_thrift_factory.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 155 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from concrete.util import is_accelerated

def test_is_accelerated():
    @py_assert1 = is_accelerated()
    @py_assert4 = (True, False)
    @py_assert3 = @py_assert1 in @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} in %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(is_accelerated) if 'is_accelerated' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(is_accelerated) else 'is_accelerated'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None