# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_classes.py
# Compiled at: 2019-10-21 04:50:21
# Size of source mod 2**32: 1335 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from liar.ijusthelp import rewrite_dict, get_single_from_list
from liar.iamaliar import IAmALiar

class TestClassClasses:

    def test_exact_list(self):
        number_records = 100
        maker = IAmALiar(number_records)
        data = maker.get_data([
         {'name':'fieldname', 
          'class':'exact',  'data':'pie'}])
        @py_assert0 = 100
        @py_assert5 = len(data)
        @py_assert2 = @py_assert0 == @py_assert5
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_classes.py', lineno=14)
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py4':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert5 = None
        @py_assert0 = {'pie'}
        @py_assert4 = [f['fieldname'] for f in data]
        @py_assert6 = set(@py_assert4)
        @py_assert2 = @py_assert0 == @py_assert6
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_classes.py', lineno=15)
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None

    def test_quick_list(self):
        number_records = 100
        maker = IAmALiar(number_records)
        data = maker.get_data([
         {'name':'fieldname', 
          'class':'quicklist', 
          'data':[
           'x', 'y', 'z']}])
        @py_assert0 = {
         'x', 'y', 'z'}
        @py_assert4 = [f['fieldname'] for f in data]
        @py_assert6 = set(@py_assert4)
        @py_assert2 = @py_assert0 == @py_assert6
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_classes.py', lineno=29)
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None

    def test_toothpaste_list(self):
        number_records = 10
        maker = IAmALiar(number_records)
        data = maker.get_data([
         {'name':'fieldname', 
          'class':'toothpaste', 
          'data':[
           'x', 'y', 'z']}])
        @py_assert0 = [
         'x', 'y', 'z', 'x', 'y', 'z', 'x', 'y', 'z', 'x']
        @py_assert3 = [f['fieldname'] for f in data]
        @py_assert2 = @py_assert0 == @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_classes.py', lineno=43)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None