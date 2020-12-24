# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/extensions/test_check_mccabe.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 2014 bytes
"""Tests for the pylint checker in :mod:`pylint.extensions.check_mccabe
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os.path as osp, pytest
from pylint.extensions import mccabe
EXPECTED_MSGS = [
 "'f1' is too complex. The McCabe rating is 1",
 "'f2' is too complex. The McCabe rating is 1",
 "'f3' is too complex. The McCabe rating is 3",
 "'f4' is too complex. The McCabe rating is 2",
 "'f5' is too complex. The McCabe rating is 2",
 "'f6' is too complex. The McCabe rating is 2",
 "'f7' is too complex. The McCabe rating is 3",
 "'f8' is too complex. The McCabe rating is 4",
 "'f9' is too complex. The McCabe rating is 9",
 "'method1' is too complex. The McCabe rating is 1",
 "This 'for' is too complex. The McCabe rating is 4",
 "'method3' is too complex. The McCabe rating is 2",
 "'f10' is too complex. The McCabe rating is 11",
 "'method2' is too complex. The McCabe rating is 18"]

@pytest.fixture(scope='module')
def enable(enable):
    return ['too-complex']


@pytest.fixture(scope='module')
def disable(disable):
    return ['all']


@pytest.fixture(scope='module')
def register(register):
    return mccabe.register


@pytest.fixture
def fname_mccabe_example():
    return osp.join(osp.dirname(osp.abspath(__file__)), 'data', 'mccabe.py')


@pytest.mark.parametrize('complexity, expected', [
 (
  0, EXPECTED_MSGS),
 (
  9, EXPECTED_MSGS[-2:])])
def test_max_mccabe_rate(linter, fname_mccabe_example, complexity, expected):
    linter.global_set_option('max-complexity', complexity)
    linter.check([fname_mccabe_example])
    real_msgs = [message.msg for message in linter.reporter.messages]
    @py_assert2 = sorted(expected)
    @py_assert7 = sorted(real_msgs)
    @py_assert4 = @py_assert2 == @py_assert7
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/extensions/test_check_mccabe.py', lineno=63)
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}', ), (@py_assert2, @py_assert7)) % {'py0':@pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted',  'py1':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted',  'py6':@pytest_ar._saferepr(real_msgs) if 'real_msgs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(real_msgs) else 'real_msgs',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None