# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/core/build/lib/impaf/tests/test_utils.py
# Compiled at: 2015-06-26 14:26:13
# Size of source mod 2**32: 378 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from ..utils import cached

class ExampleCached(object):

    def __init__(self):
        self._cache = {}
        self.runned = 0

    @cached
    def counting(self):
        self.runned += 1
        return self.runned


class TestCached(object):

    def test_simple(self):
        obj = ExampleCached()
        @py_assert1 = obj.counting
        @py_assert3 = @py_assert1()
        @py_assert6 = 1
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.counting\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj', 'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert1 = obj.counting
        @py_assert3 = @py_assert1()
        @py_assert6 = 1
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.counting\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(obj) if 'obj' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj) else 'obj', 'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None