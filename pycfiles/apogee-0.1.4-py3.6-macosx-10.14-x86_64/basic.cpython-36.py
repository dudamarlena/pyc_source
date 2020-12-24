# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/apogee/factors/discrete/optimise/basic.py
# Compiled at: 2019-06-30 08:41:01
# Size of source mod 2**32: 1605 bytes
import functools, itertools, numpy as np

def maximum_likelihood_update(x, states, n=0, alpha=0.0, parameters=None, dtype=np.float32):
    scope_states = np.unique(states, axis=0)
    parameters = np.asarray(parameters) if parameters is not None else np.zeros((scope_states.shape[0]), dtype=dtype)
    parameters *= n
    counts = _compute_rowwise_counts(x, np.arange(scope_states.shape[1]), scope_states).astype(dtype) + alpha
    for i in range(counts.shape[0]):
        idx = np.all((np.equal(scope_states[i][1:], scope_states[:, 1:])), axis=1)
        parameters[idx] += counts[idx]
        parameters[idx] /= parameters[idx].sum()

    return parameters


def _check_cardinality(data, scope, card):
    if card is None:
        card = count_unique((data[:, scope].T), axis=1)
    elif not np.all(count_unique((data[:, scope].T), axis=1) == card):
        raise AssertionError
    return card


def _compute_rowwise_counts(data, idx, states):
    count_matching_rows = functools.partial(count_matching, (data[:, idx]), axis=1)
    return np.asarray([count_matching_rows(states[i]) for i in range(states.shape[0])])


def _compute_states(card):
    variable_unique_states = np.asarray([np.arange(x) for x in card])
    state_combinations = list((itertools.product)(*variable_unique_states))
    return np.asarray(state_combinations)


def count_unique(a, axis=-1):
    b = np.sort(a, axis=axis)
    return (b[:, 1:] != b[:, :-1]).sum(axis) + 1


def count_matching(arr, target, axis=1):
    return np.all((np.equal(arr, target)), axis=axis).sum()