# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_itransform.py
# Compiled at: 2019-10-21 04:50:21
# Size of source mod 2**32: 2258 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from slugify import slugify
from liar.ijusthelp import rewrite_dict
from liar.iamaliar import IAmALiar
from liar.model.raw import ascii_lowercase_raw, ascii_uppercase_raw, academic_raw
raw = [
 'A',
 'brave,',
 'chance',
 'dance',
 'ended',
 "Fred's",
 'girlfriend',
 'hunt',
 'Ingrid',
 'just',
 'kissed',
 'like',
 'magic!',
 'once',
 'privately',
 'quartered,',
 'Nearby,',
 'romance',
 'secured',
 'the',
 'unfolding',
 'victory',
 'with',
 'X-rated,',
 'youthful',
 'zest.']
complex_string = ' '.join(raw)
transform_tester = {'name':'transform_tester', 
 'class':'quicklist', 
 'data':[
  complex_string]}

class TestClassITransform:
    small_number_records = 1
    transform_maker = IAmALiar(small_number_records)

    def test_transform_upper(self):
        d = self.transform_maker.get_data([
         rewrite_dict(transform_tester, {'itransform': ['upper']})])
        @py_assert1 = complex_string.upper
        @py_assert3 = @py_assert1()
        @py_assert6 = d[0]['transform_tester']
        @py_assert5 = @py_assert3 == @py_assert6
        if @py_assert5 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_itransform.py', lineno=60)
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.upper\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(complex_string) if 'complex_string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(complex_string) else 'complex_string',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None

    def test_transform_lower(self):
        d = self.transform_maker.get_data([
         rewrite_dict(transform_tester, {'itransform': ['lower']})])
        @py_assert1 = complex_string.lower
        @py_assert3 = @py_assert1()
        @py_assert6 = d[0]['transform_tester']
        @py_assert5 = @py_assert3 == @py_assert6
        if @py_assert5 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_itransform.py', lineno=66)
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.lower\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(complex_string) if 'complex_string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(complex_string) else 'complex_string',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None

    def test_transform_title(self):
        d = self.transform_maker.get_data([
         rewrite_dict(transform_tester, {'itransform': ['title']})])
        @py_assert1 = complex_string.title
        @py_assert3 = @py_assert1()
        @py_assert6 = d[0]['transform_tester']
        @py_assert5 = @py_assert3 == @py_assert6
        if @py_assert5 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_itransform.py', lineno=72)
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.title\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(complex_string) if 'complex_string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(complex_string) else 'complex_string',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None

    def test_transform_chomp(self):
        d = self.transform_maker.get_data([
         rewrite_dict(transform_tester, {'itransform': ['chomp']})])
        @py_assert0 = complex_string[0]
        @py_assert3 = d[0]['transform_tester']
        @py_assert2 = @py_assert0 == @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_itransform.py', lineno=78)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_transform_capitalize(self):
        d = self.transform_maker.get_data([
         rewrite_dict(transform_tester, {'itransform': ['capitalize']})])
        @py_assert1 = complex_string.capitalize
        @py_assert3 = @py_assert1()
        @py_assert6 = d[0]['transform_tester']
        @py_assert5 = @py_assert3 == @py_assert6
        if @py_assert5 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_itransform.py', lineno=84)
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.capitalize\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(complex_string) if 'complex_string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(complex_string) else 'complex_string',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None

    def test_transform_slugify(self):
        d = self.transform_maker.get_data([
         rewrite_dict(transform_tester, {'itransform': ['slugify']})])
        @py_assert2 = slugify(complex_string)
        @py_assert5 = d[0]['transform_tester']
        @py_assert4 = @py_assert2 == @py_assert5
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_itransform.py', lineno=90)
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(slugify) if 'slugify' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(slugify) else 'slugify',  'py1':@pytest_ar._saferepr(complex_string) if 'complex_string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(complex_string) else 'complex_string',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None