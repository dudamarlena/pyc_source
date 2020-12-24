# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/extensions/test_bad_builtin.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 1268 bytes
"""Tests for the pylint checker in :mod:`pylint.extensions.bad_builtin
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os.path as osp, pytest
from pylint.extensions.bad_builtin import BadBuiltinChecker
from pylint.lint import fix_import_path
EXPECTED = [
 "Used builtin function 'map'. Using a list comprehension can be clearer.",
 "Used builtin function 'filter'. Using a list comprehension can be clearer."]

@pytest.fixture(scope='module')
def checker(checker):
    return BadBuiltinChecker


@pytest.fixture(scope='module')
def disable(disable):
    return ['I']


def test_types_redefined(linter):
    elif_test = osp.join(osp.dirname(osp.abspath(__file__)), 'data', 'bad_builtin.py')
    with fix_import_path([elif_test]):
        linter.check([elif_test])
    msgs = sorted((linter.reporter.messages), key=(lambda item: item.line))
    @py_assert2 = len(msgs)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/extensions/test_bad_builtin.py', lineno=39)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(msgs) if 'msgs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msgs) else 'msgs',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    for msg, expected in zip(msgs, EXPECTED):
        @py_assert1 = msg.symbol
        @py_assert4 = 'bad-builtin'
        @py_assert3 = @py_assert1 == @py_assert4
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/extensions/test_bad_builtin.py', lineno=41)
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.symbol\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(msg) if 'msg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg) else 'msg',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = msg.msg
        @py_assert3 = @py_assert1 == expected
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/extensions/test_bad_builtin.py', lineno=42)
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.msg\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(msg) if 'msg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(msg) else 'msg',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None