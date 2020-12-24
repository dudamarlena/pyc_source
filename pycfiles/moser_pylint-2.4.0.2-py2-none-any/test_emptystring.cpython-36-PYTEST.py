# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/extensions/test_emptystring.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 1275 bytes
"""Tests for the pylint checker in :mod:`pylint.extensions.emptystring
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os.path as osp, pytest
from pylint.extensions.emptystring import CompareToEmptyStringChecker

@pytest.fixture(scope='module')
def checker(checker):
    return CompareToEmptyStringChecker


@pytest.fixture(scope='module')
def disable(disable):
    return ['I']


def test_emptystring_message(linter):
    elif_test = osp.join(osp.dirname(osp.abspath(__file__)), 'data', 'empty_string_comparison.py')
    linter.check([elif_test])
    msgs = linter.reporter.messages
    expected_lineno = [6, 9, 12, 15]
    @py_assert2 = len(msgs)
    @py_assert7 = len(expected_lineno)
    @py_assert4 = @py_assert2 == @py_assert7
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/extensions/test_emptystring.py', lineno=36)
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}', ), (@py_assert2, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(msgs) if 'msgs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msgs) else 'msgs',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py6':@pytest_ar._saferepr(expected_lineno) if 'expected_lineno' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_lineno) else 'expected_lineno',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    for msg, lineno in zip(msgs, expected_lineno):
        @py_assert1 = msg.symbol
        @py_assert4 = 'compare-to-empty-string'
        @py_assert3 = @py_assert1 == @py_assert4
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/extensions/test_emptystring.py', lineno=38)
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.symbol\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(msg) if 'msg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg) else 'msg',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = msg.msg
        @py_assert4 = 'Avoid comparisons to empty string'
        @py_assert3 = @py_assert1 == @py_assert4
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/extensions/test_emptystring.py', lineno=39)
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.msg\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(msg) if 'msg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg) else 'msg',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = msg.line
        @py_assert3 = @py_assert1 == lineno
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/extensions/test_emptystring.py', lineno=40)
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.line\n} == %(py4)s', ), (@py_assert1, lineno)) % {'py0':@pytest_ar._saferepr(msg) if 'msg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg) else 'msg',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(lineno) if 'lineno' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lineno) else 'lineno'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None