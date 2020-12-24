# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/utils/constraints.py
# Compiled at: 2018-07-20 16:00:09
# Size of source mod 2**32: 6382 bytes
from numpy import array, absolute, zeros

def within_no_constraints(root_pattern, pattern, bound_no):
    return True


def apply_no_constraints(root_pattern, pattern, grad_update, grad_step, bound_no):
    return array(pattern - grad_step * grad_update)


def within_hypercube(root_pattern, pattern, bound_no, box_step):
    bound = bound_no * box_step
    for i in range(len(pattern)):
        if pattern[i] - root_pattern[i] > bound or pattern[i] - root_pattern[i] < -bound:
            return False

    return True


def apply_hypercube(root_pattern, pattern, grad_update, grad_step, bound_no, box_step):
    next_pattern = apply_no_constraints(root_pattern, pattern, grad_update, grad_step, bound_no)
    bound = bound_no * box_step
    for i in range(len(pattern)):
        if next_pattern[i] - root_pattern[i] > bound:
            next_pattern[i] = root_pattern[i] + bound

    return next_pattern


def within_only_increment(root_pattern, pattern, bound_no, only_increment_step, weights, inv_weights, feature_upper_bound):
    root_patt_discrete = array([int(round(item)) for item in root_pattern * weights])
    patt_discrete = array([int(round(item)) for item in pattern * weights])
    dist = sum(absolute(patt_discrete - root_patt_discrete))
    if dist <= only_increment_step * bound_no:
        return True
    return False


def apply_only_increment(root_pattern, pattern, grad_update, grad_step, bound_no, only_increment_step, weights, inv_weights, feature_upper_bound=None):
    grad_update_with_indexes = list(enumerate(grad_update * inv_weights))
    grad_update_with_indexes.sort(lambda x, y: -cmp(abs(x[1]), abs(y[1])))
    new_pattern = array(pattern)
    for feature_index, value in grad_update_with_indexes:
        if value > 0:
            new_value = pattern[feature_index] - inv_weights[feature_index]
            if root_pattern[feature_index] <= new_value:
                new_pattern[feature_index] = new_value
                return new_pattern
                continue
            elif value < 0:
                diff_pattern = [int(round(item)) for item in absolute(pattern - root_pattern) * weights]
                new_value = new_pattern[feature_index] + inv_weights[feature_index]
                if not sum(diff_pattern) < only_increment_step * bound_no or feature_upper_bound is None or new_value <= feature_upper_bound:
                    new_pattern[feature_index] = new_value
                    return new_pattern
                    continue
            else:
                return new_pattern

    return new_pattern


def within_hamming(root_pattern, pattern, bound_no):
    """For simplicity, we DO NOT check if features are TRULY binary..."""
    if sum(absolute(pattern - root_pattern)) <= bound_no:
        return True
    return False


def apply_hamming(root_pattern, pattern, grad_update, grad_step, bound_no):
    """For simplicity, we DO NOT check if features are TRULY binary..."""
    grad_update_with_indexes = list(enumerate(grad_update))
    grad_update_with_indexes.sort(lambda x, y: -cmp(abs(x[1]), abs(y[1])))
    new_pattern = array(pattern)
    for feature_index, value in grad_update_with_indexes:
        if value > 0:
            if pattern[feature_index] == 1:
                new_pattern[feature_index] = 0
                return new_pattern
                continue
            elif value < 0:
                if sum(absolute(pattern - root_pattern)) < bound_no and new_pattern[feature_index] == 0:
                    new_pattern[feature_index] = 1
                    return new_pattern
                    continue
            else:
                return new_pattern

    return new_pattern


def within_box_fixed(root_pattern, pattern, bound_no, lb, ub):
    for i in range(len(pattern)):
        if pattern[i] > ub or pattern[i] < lb:
            return False

    return True


def apply_box_fixed(root_pattern, pattern, grad_update, grad_step, bound_no, lb, ub):
    next_pattern = apply_no_constraints(root_pattern, pattern, grad_update, grad_step, bound_no)
    for i in range(len(pattern)):
        if next_pattern[i] > ub:
            next_pattern[i] = ub

    return next_pattern