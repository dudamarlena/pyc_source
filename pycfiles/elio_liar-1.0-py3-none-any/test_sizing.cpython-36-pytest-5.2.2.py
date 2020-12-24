# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_sizing.py
# Compiled at: 2019-10-21 04:50:21
# Size of source mod 2**32: 805 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from liar.ijusthelp import rewrite_dict, get_single_from_list
from liar.iamaliar import IAmALiar
from liar.model.raw import ainu_raw

class TestClassSizing:

    def test_sizing_record(self):
        number_records = 1
        maker = IAmALiar(number_records)
        d = maker.get_data([ainu_raw])
        @py_assert2 = len(d)
        @py_assert4 = @py_assert2 == number_records
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_sizing.py', lineno=14)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, number_records)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(number_records) if 'number_records' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(number_records) else 'number_records'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None

    def test_sizing_records(self):
        number_records = 10000
        maker = IAmALiar(number_records)
        d = maker.get_data([ainu_raw])
        @py_assert2 = len(d)
        @py_assert4 = @py_assert2 == number_records
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_sizing.py', lineno=20)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, number_records)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(d) if 'd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d) else 'd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(number_records) if 'number_records' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(number_records) else 'number_records'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None

    def test_sizing_get_single(self):
        number_records = 10000
        maker = IAmALiar(number_records)
        d = maker.get_data([ainu_raw])
        item = get_single_from_list(d)
        @py_assert1 = item['ainu_raw']
        @py_assert4 = isinstance(@py_assert1, str)
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_sizing.py', lineno=27)
        if not @py_assert4:
            @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None