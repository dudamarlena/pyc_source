# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/common_tests/text_test.py
# Compiled at: 2019-10-16 12:05:38
# Size of source mod 2**32: 8522 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, collections, pytest
from paleomix.common.text import TableError, padded_table, parse_lines, parse_lines_by_contig, parse_padded_table

def _padded_table(*args, **kwargs):
    return list(padded_table(*args, **kwargs))


def test_padded_table__empty():
    @py_assert1 = ()
    @py_assert3 = _padded_table(@py_assert1)
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=45)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(_padded_table) if '_padded_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_padded_table) else '_padded_table',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_padded_table__single_line():
    table = [
     (1, 20, 3000)]
    expected = ['1    20    3000']
    @py_assert4 = _padded_table(table)
    @py_assert1 = expected == @py_assert4
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=51)
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}', ), (expected, @py_assert4)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(_padded_table) if '_padded_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_padded_table) else '_padded_table',  'py3':@pytest_ar._saferepr(table) if 'table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(table) else 'table',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = None


def test_padded_table__two_lines():
    table = [
     (1, 20, 3000), (3000, 20, 1)]
    expected = ['1       20    3000', '3000    20    1']
    @py_assert4 = _padded_table(table)
    @py_assert1 = expected == @py_assert4
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=57)
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}', ), (expected, @py_assert4)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(_padded_table) if '_padded_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_padded_table) else '_padded_table',  'py3':@pytest_ar._saferepr(table) if 'table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(table) else 'table',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = None


def test_padded_table__three_lines():
    table = [
     (1, 20, 3000), (3000, 20, 1), (1, 2, 30)]
    expected = ['1       20    3000', '3000    20    1', '1       2     30']
    @py_assert4 = _padded_table(table)
    @py_assert1 = expected == @py_assert4
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=63)
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}', ), (expected, @py_assert4)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(_padded_table) if '_padded_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_padded_table) else '_padded_table',  'py3':@pytest_ar._saferepr(table) if 'table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(table) else 'table',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = None


_PT_COMMENT = '# An insightful comment goes here'
_PT_ROW_1 = (1, 20, 3000)
_PT_ROW_2 = (3000, 20, 1)
_PT_LINE_1 = '1       20    3000'
_PT_LINE_2 = '3000    20    1'
_PT_PERMUTATIONS = (
 (
  [
   _PT_COMMENT, _PT_ROW_1, _PT_ROW_2], [_PT_COMMENT, _PT_LINE_1, _PT_LINE_2]),
 (
  [
   _PT_ROW_1, _PT_COMMENT, _PT_ROW_2], [_PT_LINE_1, _PT_COMMENT, _PT_LINE_2]),
 (
  [
   _PT_ROW_1, _PT_ROW_2, _PT_COMMENT], [_PT_LINE_1, _PT_LINE_2, _PT_COMMENT]))

@pytest.mark.parametrize('table, expected', _PT_PERMUTATIONS)
def test_padded_table__with_text(table, expected):
    @py_assert4 = _padded_table(table)
    @py_assert1 = expected == @py_assert4
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=81)
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}', ), (expected, @py_assert4)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(_padded_table) if '_padded_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_padded_table) else '_padded_table',  'py3':@pytest_ar._saferepr(table) if 'table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(table) else 'table',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = None


def _parse_padded_table(*args, **kwargs):
    return list(parse_padded_table(*args, **kwargs))


def test_parse_padded_table__empty():
    @py_assert0 = []
    @py_assert4 = []
    @py_assert6 = _parse_padded_table(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=94)
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(_parse_padded_table) if '_parse_padded_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_parse_padded_table) else '_parse_padded_table',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_parse_padded_table__header_only():
    @py_assert0 = []
    @py_assert4 = [
     'A  B  C  D']
    @py_assert6 = _parse_padded_table(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=98)
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(_parse_padded_table) if '_parse_padded_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_parse_padded_table) else '_parse_padded_table',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_parse_padded_table__single_row():
    table = [
     'A    B    C    D', '4    3    2    1']
    expected = [{'A':'4',  'B':'3',  'C':'2',  'D':'1'}]
    @py_assert4 = _parse_padded_table(table)
    @py_assert1 = expected == @py_assert4
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=104)
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}', ), (expected, @py_assert4)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(_parse_padded_table) if '_parse_padded_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_parse_padded_table) else '_parse_padded_table',  'py3':@pytest_ar._saferepr(table) if 'table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(table) else 'table',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = None


def test_parse_padded_table__two_rows():
    table = [
     'A     B     C     D', '4     3     2     1', 'AB    CD    EF    GH']
    expected = [
     {'A':'4', 
      'B':'3',  'C':'2',  'D':'1'},
     {'A':'AB', 
      'B':'CD',  'C':'EF',  'D':'GH'}]
    @py_assert4 = _parse_padded_table(table)
    @py_assert1 = expected == @py_assert4
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=113)
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}', ), (expected, @py_assert4)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(_parse_padded_table) if '_parse_padded_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_parse_padded_table) else '_parse_padded_table',  'py3':@pytest_ar._saferepr(table) if 'table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(table) else 'table',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = None


def test_parse_padded_table__single_row__with_whitespace():
    table = [
     'A   B    C       E F', '1        0  1    2   3']
    expected = [{'A':'1',  'B':'0',  'C':'1',  'E':'2',  'F':'3'}]
    @py_assert4 = _parse_padded_table(table)
    @py_assert1 = expected == @py_assert4
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=120)
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}', ), (expected, @py_assert4)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(_parse_padded_table) if '_parse_padded_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_parse_padded_table) else '_parse_padded_table',  'py3':@pytest_ar._saferepr(table) if 'table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(table) else 'table',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = None


def test_parse_padded_table__single_row__with_tabs():
    table = [
     'A\t\t\t\tB', '1\t\t\t\t0']
    expected = [{'A':'1',  'B':'0'}]
    @py_assert4 = _parse_padded_table(table)
    @py_assert1 = expected == @py_assert4
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=127)
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}', ), (expected, @py_assert4)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(_parse_padded_table) if '_parse_padded_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_parse_padded_table) else '_parse_padded_table',  'py3':@pytest_ar._saferepr(table) if 'table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(table) else 'table',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = None


_PT_COMMENTS_LINE_AND_EMPTY_1 = 'A         B      C'
_PT_COMMENTS_LINE_AND_EMPTY_2 = '3000      20      1'
__PT_COMMENTS_LINE_AND_EMPTY = (
 [
  '# comment', _PT_COMMENTS_LINE_AND_EMPTY_1, _PT_COMMENTS_LINE_AND_EMPTY_2],
 [
  _PT_COMMENTS_LINE_AND_EMPTY_1, ' # comment', _PT_COMMENTS_LINE_AND_EMPTY_2],
 [
  _PT_COMMENTS_LINE_AND_EMPTY_1, _PT_COMMENTS_LINE_AND_EMPTY_2, '  # comment'],
 [
  '', _PT_COMMENTS_LINE_AND_EMPTY_1, _PT_COMMENTS_LINE_AND_EMPTY_2],
 [
  _PT_COMMENTS_LINE_AND_EMPTY_1, '  ', _PT_COMMENTS_LINE_AND_EMPTY_2],
 [
  _PT_COMMENTS_LINE_AND_EMPTY_1, _PT_COMMENTS_LINE_AND_EMPTY_2, '   '])

@pytest.mark.parametrize('lines', __PT_COMMENTS_LINE_AND_EMPTY)
def test_padded_table__comments_and_empty_lines(lines):
    expected = [{'A':'3000',  'B':'20',  'C':'1'}]
    @py_assert4 = _parse_padded_table(lines)
    @py_assert1 = expected == @py_assert4
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=146)
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}', ), (expected, @py_assert4)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(_parse_padded_table) if '_parse_padded_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_parse_padded_table) else '_parse_padded_table',  'py3':@pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = None


@pytest.mark.parametrize('postfix', ('\r', '\n', '\r\n'))
def test_padded_table__newlines(postfix):
    expected = [{'A':'3000',  'B':'20',  'C':'1'}]
    line_1 = 'A         B       C' + postfix
    line_2 = '3000      20      1' + postfix
    @py_assert3 = [line_1, line_2]
    @py_assert5 = _parse_padded_table(@py_assert3)
    @py_assert1 = expected == @py_assert5
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=155)
    if not @py_assert1:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py6)s\n{%(py6)s = %(py2)s(%(py4)s)\n}', ), (expected, @py_assert5)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(_parse_padded_table) if '_parse_padded_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_parse_padded_table) else '_parse_padded_table',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_padded_table__padding__comments__whitespace():
    expected = [
     {'A':'3000', 
      'B':'20',  'C':'1'}]
    lines = ['A         B       C', '3000      20      1', '  # useless comment']
    @py_assert4 = _parse_padded_table(lines)
    @py_assert1 = expected == @py_assert4
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=161)
    if not @py_assert1:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py5)s\n{%(py5)s = %(py2)s(%(py3)s)\n}', ), (expected, @py_assert4)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(_parse_padded_table) if '_parse_padded_table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_parse_padded_table) else '_parse_padded_table',  'py3':@pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = None


def test_parse_padded_table__malformed_table_0():
    table = [
     'A    B    C    D', '4    3    2']
    with pytest.raises(TableError):
        _parse_padded_table(table)


def test_parse_padded_table__malformed_table_1():
    table = [
     'A    B    C    D', '4    3    2    1    0']
    with pytest.raises(TableError):
        _parse_padded_table(table)


def _this(*args):
    return args


def _parse_lines(*args, **kwargs):
    return list(parse_lines(*args, **kwargs))


def test_parse_lines__empty_file():

    def _assert_false():
        @py_assert0 = False
        if @py_assert0 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=189)
        if not @py_assert0:
            @py_format2 = 'assert %(py1)s' % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None

    @py_assert1 = []
    @py_assert4 = _parse_lines(@py_assert1, _assert_false)
    @py_assert7 = []
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=191)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(_parse_lines) if '_parse_lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_parse_lines) else '_parse_lines',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(_assert_false) if '_assert_false' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_assert_false) else '_assert_false',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_parse_lines__single():
    @py_assert1 = [
     'abc line1 \n']
    @py_assert4 = _parse_lines(@py_assert1, _this)
    @py_assert7 = [
     ('abc line1', 9)]
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=195)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(_parse_lines) if '_parse_lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_parse_lines) else '_parse_lines',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(_this) if '_this' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_this) else '_this',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None


_PT_COMMENTS_AND_EMPTY_LINES = (
 [
  '# comment\n', 'abc line1 \n', 'def line2 \n'],
 [
  'abc line1 \n', ' # comment\n', 'def line2 \n'],
 [
  'abc line1 \n', 'def line2 \n', '   # comment\n'],
 [
  '\n', 'abc line1 \n', 'def line2 \n'],
 [
  'abc line1 \n', ' \n', 'def line2 \n'],
 [
  'abc line1 \n', 'def line2 \n', '   \n'])

@pytest.mark.parametrize('lines', _PT_COMMENTS_AND_EMPTY_LINES)
def test_parse_lines__comments_and_empty_lines(lines):
    expected = [('abc line1', 9), ('def line2', 9)]
    @py_assert3 = _parse_lines(lines, _this)
    @py_assert5 = @py_assert3 == expected
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=211)
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(_parse_lines) if '_parse_lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_parse_lines) else '_parse_lines',  'py1':@pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines',  'py2':@pytest_ar._saferepr(_this) if '_this' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_this) else '_this',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert3 = @py_assert5 = None


@pytest.mark.parametrize('postfix', ('\r', '\n', '\r\n'))
def test_parse_lines__padding__newlines(postfix):
    expected = [('abc line1', 9), ('def line2', 9)]
    line_1 = 'abc line1 ' + postfix
    line_2 = 'def line2 ' + postfix
    @py_assert3 = [line_1, line_2]
    @py_assert6 = _parse_lines(@py_assert3, _this)
    @py_assert1 = expected == @py_assert6
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=220)
    if not @py_assert1:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py7)s\n{%(py7)s = %(py2)s(%(py4)s, %(py5)s)\n}', ), (expected, @py_assert6)) % {'py0':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py2':@pytest_ar._saferepr(_parse_lines) if '_parse_lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_parse_lines) else '_parse_lines',  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(_this) if '_this' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_this) else '_this',  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert6 = None


def test_parse_lines__uncallable():
    with pytest.raises(TypeError):
        _parse_lines([], 1)


_RecordMock = collections.namedtuple('_RecordMock', 'contig value')

def test_parse_lines_by_contig__single_contig():
    lines = [
     'abc line1 \n', 'abc line2 \n']

    def _parse(line, length):
        @py_assert2 = len(line)
        @py_assert4 = @py_assert2 == length
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=238)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, length)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(line) if 'line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(line) else 'line',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(length) if 'length' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(length) else 'length'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None
        return _RecordMock(*line.split())

    expected = {'abc': [_RecordMock('abc', 'line1'), _RecordMock('abc', 'line2')]}
    @py_assert3 = parse_lines_by_contig(lines, _parse)
    @py_assert5 = @py_assert3 == expected
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=242)
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(parse_lines_by_contig) if 'parse_lines_by_contig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parse_lines_by_contig) else 'parse_lines_by_contig',  'py1':@pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines',  'py2':@pytest_ar._saferepr(_parse) if '_parse' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_parse) else '_parse',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert3 = @py_assert5 = None


def test_parse_lines__two_contigs():
    lines = [
     'abc line1 \n', 'def line2 \n']

    def _parse(line, length):
        @py_assert2 = len(line)
        @py_assert4 = @py_assert2 == length
        if @py_assert4 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=249)
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, length)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(line) if 'line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(line) else 'line',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(length) if 'length' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(length) else 'length'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None
        return _RecordMock(*line.split())

    expected = {'abc':[
      _RecordMock('abc', 'line1')], 
     'def':[
      _RecordMock('def', 'line2')]}
    @py_assert3 = parse_lines_by_contig(lines, _parse)
    @py_assert5 = @py_assert3 == expected
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/text_test.py', lineno=256)
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(parse_lines_by_contig) if 'parse_lines_by_contig' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parse_lines_by_contig) else 'parse_lines_by_contig',  'py1':@pytest_ar._saferepr(lines) if 'lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines) else 'lines',  'py2':@pytest_ar._saferepr(_parse) if '_parse' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_parse) else '_parse',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert3 = @py_assert5 = None