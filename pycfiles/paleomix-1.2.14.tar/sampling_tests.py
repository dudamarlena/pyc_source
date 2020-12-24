# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/common_tests/sampling_tests.py
# Compiled at: 2019-10-27 09:55:00
from nose.tools import assert_equal, assert_raises
from flexmock import flexmock
import paleomix.common.sampling as sampling

def test_weighted_sampling__select_by_weight():

    def _do_select_by_weight(value, expectation):
        choices = 'abc'
        weights = (1, 2, 3)
        rng = flexmock(random=lambda : value)
        iterator = sampling.weighted_sampling(choices, weights, rng)
        assert_equal(iterator.next(), expectation)

    yield (
     _do_select_by_weight, 0.0, 'a')
    yield (_do_select_by_weight, 0.16666, 'a')
    yield (_do_select_by_weight, 1 / 6.0, 'b')
    yield (_do_select_by_weight, 0.49999, 'b')
    yield (_do_select_by_weight, 3 / 6.0, 'c')
    yield (_do_select_by_weight, 0.99999, 'c')


def test_weighted_sampling__empty_input_raises_value_error_for_lists():

    def _do_empty_input_raises(choices, weights):
        iterator = sampling.weighted_sampling(choices, weights)
        assert_raises(ValueError, iterator.next)

    yield (
     _do_empty_input_raises, [], [])
    yield (_do_empty_input_raises, [], [1, 2])
    yield (_do_empty_input_raises, [1, 2], [])


def test_weighted_sampling__different_length_input_raises_value_error():

    def _do_different_length_input_raises(choices, weights):
        iterator = sampling.weighted_sampling(choices, weights)
        assert_raises(ValueError, iterator.next)

    yield (
     _do_different_length_input_raises, [0, 1], [1, 2, 3])
    yield (_do_different_length_input_raises, [0, 1, 2], [1, 2])
    yield (_do_different_length_input_raises, iter([0, 1]), [1, 2, 3])
    yield (_do_different_length_input_raises, [0, 1], iter([1, 2, 3]))
    yield (_do_different_length_input_raises, iter([0, 1]), iter([1, 2, 3]))


def test_weighted_sampling__negative_weight_value_error():
    choices = range(3)
    weights = [1, -2, 3]
    iterator = sampling.weighted_sampling(choices, weights)
    assert_raises(ValueError, iterator.next)


def test_weighted_sampling__zero_weight_raises_value_error():
    choices = range(3)
    weights = [1, 0, 3]
    iterator = sampling.weighted_sampling(choices, weights)
    assert_raises(ValueError, iterator.next)


def test_weighted_sampling__non_numerical_weight_raises_type_error():
    choices = range(3)
    weights = [1, 'foo', 3]
    iterator = sampling.weighted_sampling(choices, weights)
    assert_raises(TypeError, iterator.next)


def test_reservoir_sampling__select_first_item():
    rng = flexmock(randint=lambda _min, _max: 1)
    values = [1, 2]
    result = sampling.reservoir_sampling(values, 1, rng)
    assert_equal(result, [1])


def test_reservoir_sampling__select_second_item():
    rng = flexmock(randint=lambda _min, _max: 0)
    values = [1, 2]
    result = sampling.reservoir_sampling(values, 1, rng)
    assert_equal(result, [2])


def test_reservoir_sampling__upsample_equals_input():
    result = sampling.reservoir_sampling(range(5), 10)
    assert_equal(result, range(5))


def test_reservoir_sampling__downsample_to_zero():
    result = sampling.reservoir_sampling(range(5), 0)
    assert_equal(result, [])


def test_reservoir_sampling__downsample_to_negative_raises_value_error():
    assert_raises(ValueError, sampling.reservoir_sampling, range(5), -1)


def test_reservoir_sampling__downsample_to_float_raises_type_error():
    assert_raises(TypeError, sampling.reservoir_sampling, range(5), 1.0)


def test_reservoir_sampling__downsample_to_non_number_raises_type_error():
    assert_raises(TypeError, sampling.reservoir_sampling, range(5), 'Eh?')