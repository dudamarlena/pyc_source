# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/common_tests/sampling_test.py
# Compiled at: 2019-10-16 12:05:38
# Size of source mod 2**32: 4714 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from unittest.mock import Mock
import pytest, paleomix.common.sampling as sampling
_SELECT_BY_VALUE = ((0.0, 'a'), (0.16666, 'a'), (0.16666666666666666, 'b'), (0.49999, 'b'),
                    (0.5, 'c'), (0.99999, 'c'))

@pytest.mark.parametrize('value, expectation', _SELECT_BY_VALUE)
def test_weighted_sampling__select_by_weight(value, expectation):
    choices = 'abc'
    weights = (1, 2, 3)
    rng = Mock(random=(lambda : value))
    iterator = sampling.weighted_sampling(choices, weights, rng)
    @py_assert2 = next(iterator)
    @py_assert4 = @py_assert2 == expectation
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sampling_test.py', lineno=50)
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, expectation)) % {'py0':@pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next',  'py1':@pytest_ar._saferepr(iterator) if 'iterator' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(iterator) else 'iterator',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(expectation) if 'expectation' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expectation) else 'expectation'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None


@pytest.mark.parametrize('choices, weights', (([], []), ([], [1, 2]), ([1, 2], [])))
def test_weighted_sampling__(choices, weights):
    iterator = sampling.weighted_sampling(choices, weights)
    with pytest.raises(ValueError):
        iterator.__next__()


_MISMATCHED_LENGTH_INPUTS = (
 (
  [
   0, 1], [1, 2, 3]),
 (
  [
   0, 1, 2], [1, 2]),
 (
  iter([0, 1]), [1, 2, 3]),
 (
  [
   0, 1], iter([1, 2, 3])),
 (
  iter([0, 1]), iter([1, 2, 3])))

@pytest.mark.parametrize('choices, weights', _MISMATCHED_LENGTH_INPUTS)
def test_weighted_sampling__different_length_input_raises_value_error(choices, weights):
    iterator = sampling.weighted_sampling(choices, weights)
    with pytest.raises(ValueError):
        iterator.__next__()


def test_weighted_sampling__negative_weight_value_error():
    choices = [
     0, 1, 2]
    weights = [1, -2, 3]
    iterator = sampling.weighted_sampling(choices, weights)
    with pytest.raises(ValueError):
        iterator.__next__()


def test_weighted_sampling__zero_weight_raises_value_error():
    choices = [
     0, 1, 2]
    weights = [1, 0, 3]
    iterator = sampling.weighted_sampling(choices, weights)
    with pytest.raises(ValueError):
        iterator.__next__()


def test_weighted_sampling__non_numerical_weight_raises_type_error():
    choices = [
     0, 1, 2]
    weights = [1, 'foo', 3]
    iterator = sampling.weighted_sampling(choices, weights)
    with pytest.raises(TypeError):
        iterator.__next__()


def test_reservoir_sampling__select_first_item():
    rng = Mock(randint=(lambda _min, _max: 1))
    values = [1, 2]
    result = sampling.reservoir_sampling(values, 1, rng)
    @py_assert2 = [1]
    @py_assert1 = result == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sampling_test.py', lineno=109)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_reservoir_sampling__select_second_item():
    rng = Mock(randint=(lambda _min, _max: 0))
    values = [1, 2]
    result = sampling.reservoir_sampling(values, 1, rng)
    @py_assert2 = [2]
    @py_assert1 = result == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sampling_test.py', lineno=116)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_reservoir_sampling__upsample_equals_input():
    result = sampling.reservoir_sampling(list(range(5)), 10)
    @py_assert4 = 5
    @py_assert6 = range(@py_assert4)
    @py_assert8 = list(@py_assert6)
    @py_assert1 = result == @py_assert8
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sampling_test.py', lineno=121)
    if not @py_assert1:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py9)s\n{%(py9)s = %(py2)s(%(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n})\n}', ), (result, @py_assert8)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py3':@pytest_ar._saferepr(range) if 'range' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(range) else 'range',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = None


def test_reservoir_sampling__downsample_to_zero():
    result = sampling.reservoir_sampling(list(range(5)), 0)
    @py_assert2 = []
    @py_assert1 = result == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/common_tests/sampling_test.py', lineno=126)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py0':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_reservoir_sampling__downsample_to_negative_raises_value_error():
    with pytest.raises(ValueError):
        sampling.reservoir_sampling(list(range(5)), -1)


def test_reservoir_sampling__downsample_to_float_raises_type_error():
    with pytest.raises(TypeError):
        sampling.reservoir_sampling(list(range(5)), 1.0)


def test_reservoir_sampling__downsample_to_non_number_raises_type_error():
    with pytest.raises(TypeError):
        sampling.reservoir_sampling(list(range(5)), 'Eh?')