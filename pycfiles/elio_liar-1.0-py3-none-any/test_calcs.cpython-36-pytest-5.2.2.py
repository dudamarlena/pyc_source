# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_calcs.py
# Compiled at: 2019-10-21 04:50:21
# Size of source mod 2**32: 2396 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from liar.iamaliar import IAmALiar

class TestClassCalcs:
    calc_maker = IAmALiar(1)

    def test_calc_add(self):
        d = self.calc_maker.get_data([
         {'name':'test_calc', 
          'class':'exact', 
          'data':3, 
          'calc':[
           {'add': 5}]}])
        @py_assert0 = d[0]['test_calc']
        @py_assert3 = 3
        @py_assert5 = 5
        @py_assert7 = @py_assert3 + @py_assert5
        @py_assert2 = @py_assert0 == @py_assert7
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_calcs.py', lineno=20)
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == (%(py4)s + %(py6)s)', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = @py_assert7 = None

    def test_calc_subtract(self):
        d = self.calc_maker.get_data([
         {'name':'test_calc', 
          'class':'exact', 
          'data':3, 
          'calc':[
           {'subtract': 5}]}])
        @py_assert0 = d[0]['test_calc']
        @py_assert3 = 3
        @py_assert5 = 5
        @py_assert7 = @py_assert3 - @py_assert5
        @py_assert2 = @py_assert0 == @py_assert7
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_calcs.py', lineno=33)
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == (%(py4)s - %(py6)s)', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = @py_assert7 = None

    def test_calc_multiply(self):
        d = self.calc_maker.get_data([
         {'name':'test_calc', 
          'class':'exact', 
          'data':3, 
          'calc':[
           {'multiply': 5}]}])
        @py_assert0 = d[0]['test_calc']
        @py_assert3 = 3
        @py_assert5 = 5
        @py_assert7 = @py_assert3 * @py_assert5
        @py_assert2 = @py_assert0 == @py_assert7
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_calcs.py', lineno=46)
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == (%(py4)s * %(py6)s)', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = @py_assert7 = None

    def test_calc_divide(self):
        d = self.calc_maker.get_data([
         {'name':'test_calc', 
          'class':'exact', 
          'data':3, 
          'calc':[
           {'divide': 5}]}])
        @py_assert0 = d[0]['test_calc']
        @py_assert3 = 3
        @py_assert5 = 5
        @py_assert7 = @py_assert3 / @py_assert5
        @py_assert2 = @py_assert0 == @py_assert7
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_calcs.py', lineno=59)
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == (%(py4)s / %(py6)s)', ), (@py_assert0, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = @py_assert7 = None

    def test_calc_format(self):
        d = self.calc_maker.get_data([
         {'name':'test_calc', 
          'class':'exact', 
          'data':5.012345678, 
          'calc':[
           {'format': '{:10.2f}'}]}])
        @py_assert0 = d[0]['test_calc']
        @py_assert3 = '      5.01'
        @py_assert2 = @py_assert0 == @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_calcs.py', lineno=72)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_calc_combine(self):
        d = self.calc_maker.get_data([
         {'name':'test_calc', 
          'class':'exact', 
          'data':3, 
          'calc':[
           {'multiply': 10},
           {'add': 2},
           {'subtract': 5},
           {'divide': 3}]}])
        @py_assert0 = d[0]['test_calc']
        @py_assert3 = 3
        @py_assert5 = 10
        @py_assert7 = @py_assert3 * @py_assert5
        @py_assert8 = 2
        @py_assert10 = @py_assert7 + @py_assert8
        @py_assert11 = 5
        @py_assert13 = @py_assert10 - @py_assert11
        @py_assert14 = 3
        @py_assert16 = @py_assert13 / @py_assert14
        @py_assert2 = @py_assert0 == @py_assert16
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_calcs.py', lineno=90)
        if not @py_assert2:
            @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == ((((%(py4)s * %(py6)s) + %(py9)s) - %(py12)s) / %(py15)s)', ), (@py_assert0, @py_assert16)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
            @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
            raise AssertionError(@pytest_ar._format_explanation(@py_format19))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = @py_assert10 = @py_assert11 = @py_assert13 = @py_assert14 = @py_assert16 = None