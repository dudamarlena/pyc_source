# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vkuznetsov/prog/devops/python-abp/tests/test_stats/test_filtehits_loader.py
# Compiled at: 2019-05-13 06:18:18
# Size of source mod 2**32: 2001 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, py
from abp.stats.filterhits import load_filterhit_statistics
DATA_PATH = py.path.local(__file__).dirpath('data')

@pytest.fixture
def filterhits_file():
    return DATA_PATH.join('filterhits.csv')


@pytest.fixture
def filterhits_file_missing_columns():
    return DATA_PATH.join('filterhits_missing_columns.csv')


def test_filterhits_load_no_filtering(filterhits_file):
    entries = load_filterhit_statistics(str(filterhits_file))
    count = 0
    for entry in entries:
        count += 1
        @py_assert1 = entry['hits']
        @py_assert4 = isinstance(@py_assert1, int)
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_stats/test_filtehits_loader.py', lineno=41)
        if not @py_assert4:
            @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None
        @py_assert1 = entry['onehour_sessions']
        @py_assert4 = isinstance(@py_assert1, int)
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_stats/test_filtehits_loader.py', lineno=42)
        if not @py_assert4:
            @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None
        @py_assert1 = entry['domains']
        @py_assert4 = isinstance(@py_assert1, int)
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_stats/test_filtehits_loader.py', lineno=43)
        if not @py_assert4:
            @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None
        @py_assert1 = entry['rootdomains']
        @py_assert4 = isinstance(@py_assert1, int)
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_stats/test_filtehits_loader.py', lineno=44)
        if not @py_assert4:
            @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None

    @py_assert2 = 2
    @py_assert1 = count == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_stats/test_filtehits_loader.py', lineno=46)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (count, @py_assert2)) % {'py0':@pytest_ar._saferepr(count) if 'count' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(count) else 'count',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


@pytest.mark.parametrize('sources,exp_count', [
 (
  [
   'www.exceptionlist.com'], 1),
 (
  [
   'www.exceptionlist.com', 'www.blocklist.com'], 2),
 (
  [
   'inexistent_source', 'foo', 'bar'], 0)])
def test_filterhits_load_with_filtering(sources, exp_count, filterhits_file):
    entries = load_filterhit_statistics(str(filterhits_file), sources)
    @py_assert3 = list(entries)
    @py_assert5 = len(@py_assert3)
    @py_assert7 = @py_assert5 == exp_count
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_stats/test_filtehits_loader.py', lineno=57)
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py8)s', ), (@py_assert5, exp_count)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(entries) if 'entries' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(entries) else 'entries',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(exp_count) if 'exp_count' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exp_count) else 'exp_count'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert3 = @py_assert5 = @py_assert7 = None


def test_filterhits_load_missing_columns(filterhits_file_missing_columns):
    entries = load_filterhit_statistics(str(filterhits_file_missing_columns))
    @py_assert3 = list(entries)
    @py_assert5 = len(@py_assert3)
    @py_assert8 = 2
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_stats/test_filtehits_loader.py', lineno=63)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n})\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py2':@pytest_ar._saferepr(entries) if 'entries' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(entries) else 'entries',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None