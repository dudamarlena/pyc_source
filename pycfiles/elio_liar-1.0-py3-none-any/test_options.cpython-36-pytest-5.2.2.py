# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_options.py
# Compiled at: 2019-10-21 04:50:21
# Size of source mod 2**32: 3305 bytes
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
 'hunt.',
 'Ingrid',
 'just',
 'kissed',
 'like',
 'magic!',
 'Nearby,',
 'once',
 'privately',
 'quartered,',
 'romance',
 'secured',
 'the',
 'unfolding',
 'victory',
 'with',
 'xrated,',
 'youthful',
 'zest.']
complex_string = ' '.join(raw)
transform_tester = {'name':'transform_tester', 
 'class':'quicklist', 
 'data':[
  complex_string]}

class TestClassOptions:
    large_number_records = 10000
    transform_maker = IAmALiar(large_number_records)

    def test_options_splutter(self):
        percent = 50
        target = self.large_number_records * (percent / 100)
        leeway = self.large_number_records * 0.1
        d = self.transform_maker.get_data([
         rewrite_dict(transform_tester, {'splutter': percent})])
        d_not_blank = [item for item in d if item['transform_tester']]
        @py_assert1 = []
        @py_assert4 = len(d_not_blank)
        @py_assert9 = target - leeway
        @py_assert6 = @py_assert4 > @py_assert9
        @py_assert0 = @py_assert6
        if @py_assert6:
            @py_assert15 = len(d_not_blank)
            @py_assert20 = target + leeway
            @py_assert17 = @py_assert15 < @py_assert20
            @py_assert0 = @py_assert17
        if @py_assert0 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_options.py', lineno=66)
        if not @py_assert0:
            @py_format10 = @pytest_ar._call_reprcompare(('>', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n} > (%(py7)s - %(py8)s)', ), (@py_assert4, @py_assert9)) % {'py2':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py3':@pytest_ar._saferepr(d_not_blank) if 'd_not_blank' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d_not_blank) else 'd_not_blank',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py8':@pytest_ar._saferepr(leeway) if 'leeway' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(leeway) else 'leeway'}
            @py_format12 = '%(py11)s' % {'py11': @py_format10}
            @py_assert1.append(@py_format12)
            if @py_assert6:
                @py_format21 = @pytest_ar._call_reprcompare(('<', ), (@py_assert17,), ('%(py16)s\n{%(py16)s = %(py13)s(%(py14)s)\n} < (%(py18)s + %(py19)s)', ), (@py_assert15, @py_assert20)) % {'py13':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py14':@pytest_ar._saferepr(d_not_blank) if 'd_not_blank' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(d_not_blank) else 'd_not_blank',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target',  'py19':@pytest_ar._saferepr(leeway) if 'leeway' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(leeway) else 'leeway'}
                @py_format23 = '%(py22)s' % {'py22': @py_format21}
                @py_assert1.append(@py_format23)
            @py_format24 = @pytest_ar._format_boolop(@py_assert1, 0) % {}
            @py_format26 = 'assert %(py25)s' % {'py25': @py_format24}
            raise AssertionError(@pytest_ar._format_explanation(@py_format26))
        @py_assert0 = @py_assert1 = @py_assert4 = @py_assert6 = @py_assert9 = @py_assert15 = @py_assert17 = @py_assert20 = None

    def test_options_filter(self):
        d = self.transform_maker.get_data([academic_raw])
        @py_assert0 = {'Arts', 'Business', 'Science'}
        @py_assert4 = [item['academic_raw']['department'] for item in d]
        @py_assert6 = set(@py_assert4)
        @py_assert2 = @py_assert0 == @py_assert6
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_options.py', lineno=72)
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
        d = self.transform_maker.get_data([
         rewrite_dict(academic_raw, {'filters': {'department': ['Arts', 'Science']}})])
        @py_assert0 = {
         'Arts', 'Science'}
        @py_assert4 = [item['academic_raw']['department'] for item in d]
        @py_assert6 = set(@py_assert4)
        @py_assert2 = @py_assert0 == @py_assert6
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_options.py', lineno=84)
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None

    def test_options_multi_filter(self):
        d = self.transform_maker.get_data([
         {'name':'p1', 
          'class':'igetraw', 
          'data':'person', 
          'filters':{'sex':[
            'female'], 
           'title':['Mrs', 'Dr']}}])
        @py_assert0 = {
         'female'}
        @py_assert4 = [item['p1']['sex'] for item in d]
        @py_assert6 = set(@py_assert4)
        @py_assert2 = @py_assert0 == @py_assert6
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_options.py', lineno=99)
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = {'Dr', 'Mrs'}
        @py_assert4 = [item['p1']['title'] for item in d]
        @py_assert6 = set(@py_assert4)
        @py_assert2 = @py_assert0 == @py_assert6
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_options.py', lineno=100)
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None

    def test_options_remove(self):
        resp = 'NOSUCHCOLUMN!'
        d = self.transform_maker.get_data([
         ascii_lowercase_raw,
         rewrite_dict(ascii_uppercase_raw, {'remove': True})])
        @py_assert0 = d[0]
        @py_assert2 = @py_assert0.get
        @py_assert4 = 'ascii_uppercase_raw'
        @py_assert7 = @py_assert2(@py_assert4, resp)
        @py_assert9 = @py_assert7 == resp
        if @py_assert9 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_options.py', lineno=110)
        if not @py_assert9:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py3)s\n{%(py3)s = %(py1)s.get\n}(%(py5)s, %(py6)s)\n} == %(py10)s', ), (@py_assert7, resp)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(resp) if 'resp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(resp) else 'resp',  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(resp) if 'resp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(resp) else 'resp'}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = @py_assert9 = None


class TestClassFlatten:

    def test_flatten_column(self):
        number_records = 1
        maker = IAmALiar(number_records)
        data = maker.get_data([
         {'name':'academic', 
          'class':'igetraw', 
          'data':'academic', 
          'flatten':True}])
        @py_assert0 = 1
        @py_assert5 = len(data)
        @py_assert2 = @py_assert0 == @py_assert5
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_options.py', lineno=127)
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py4':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert5 = None
        @py_assert0 = 2
        @py_assert4 = data[0]
        @py_assert6 = @py_assert4.keys
        @py_assert8 = @py_assert6()
        @py_assert10 = len(@py_assert8)
        @py_assert2 = @py_assert0 == @py_assert10
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_options.py', lineno=128)
        if not @py_assert2:
            @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py11)s\n{%(py11)s = %(py3)s(%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.keys\n}()\n})\n}', ), (@py_assert0, @py_assert10)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10)}
            @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
        @py_assert0 = {'academic_department', 'academic_subject'}
        @py_assert4 = data[0]
        @py_assert6 = @py_assert4.keys
        @py_assert8 = @py_assert6()
        @py_assert10 = set(@py_assert8)
        @py_assert2 = @py_assert0 == @py_assert10
        if @py_assert2 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/tim/repo/dev/elioway/elioangels/liar/build/lib/liar/tests/test_options.py', lineno=129)
        if not @py_assert2:
            @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py11)s\n{%(py11)s = %(py3)s(%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.keys\n}()\n})\n}', ), (@py_assert0, @py_assert10)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10)}
            @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None