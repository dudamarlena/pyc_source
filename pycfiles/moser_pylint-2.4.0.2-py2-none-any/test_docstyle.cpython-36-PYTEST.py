# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/extensions/test_docstyle.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 1751 bytes
"""Tests for the pylint checker in :mod:`pylint.extensions.check_docstring
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from os.path import abspath, dirname, join
import pytest
from pylint.extensions.docstyle import DocStringStyleChecker
EXPECTED_MSGS = [
 'First line empty in function docstring',
 'First line empty in class docstring',
 'First line empty in method docstring',
 'Bad docstring quotes in method, expected """, given \'\'\'',
 'Bad docstring quotes in method, expected """, given "',
 'Bad docstring quotes in method, expected """, given \'',
 'Bad docstring quotes in method, expected """, given \'']
EXPECTED_SYMBOLS = [
 'docstring-first-line-empty',
 'docstring-first-line-empty',
 'docstring-first-line-empty',
 'bad-docstring-quotes',
 'bad-docstring-quotes',
 'bad-docstring-quotes',
 'bad-docstring-quotes']

@pytest.fixture(scope='module')
def checker(checker):
    return DocStringStyleChecker


def test_docstring_message(linter):
    docstring_test = join(dirname(abspath(__file__)), 'data', 'docstring.py')
    linter.check([docstring_test])
    msgs = linter.reporter.messages
    @py_assert2 = len(msgs)
    @py_assert5 = 7
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/extensions/test_docstyle.py', lineno=47)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(msgs) if 'msgs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msgs) else 'msgs',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    for msg, expected_symbol, expected_msg in zip(msgs, EXPECTED_SYMBOLS, EXPECTED_MSGS):
        @py_assert1 = msg.symbol
        @py_assert3 = @py_assert1 == expected_symbol
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/extensions/test_docstyle.py', lineno=51)
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.symbol\n} == %(py4)s', ), (@py_assert1, expected_symbol)) % {'py0':@pytest_ar._saferepr(msg) if 'msg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg) else 'msg',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected_symbol) if 'expected_symbol' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_symbol) else 'expected_symbol'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        @py_assert1 = msg.msg
        @py_assert3 = @py_assert1 == expected_msg
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/extensions/test_docstyle.py', lineno=52)
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.msg\n} == %(py4)s', ), (@py_assert1, expected_msg)) % {'py0':@pytest_ar._saferepr(msg) if 'msg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg) else 'msg',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected_msg) if 'expected_msg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_msg) else 'expected_msg'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None