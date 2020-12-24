# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/gplearn/utils.py
# Compiled at: 2020-04-02 03:45:04
# Size of source mod 2**32: 3550 bytes
"""Utilities that are required by gplearn.

Most of these functions are slightly modified versions of some key utility
functions from scikit-learn that gplearn depends upon. They reside here in
order to maintain compatibility across different versions of scikit-learn.

"""
import numbers, numpy as np
from joblib import cpu_count

class NotFittedError(ValueError, AttributeError):
    __doc__ = "Exception class to raise if estimator is used before fitting.\n\n    This class inherits from both ValueError and AttributeError to help with\n    exception handling and backward compatibility.\n\n    Examples\n    --------\n    >>> from sklearn.svm import LinearSVC\n    >>> from sklearn.exceptions import NotFittedError\n    >>> try:\n    ...     LinearSVC().predict([[1, 2], [2, 3], [3, 4]])\n    ... except NotFittedError as e:\n    ...     print(repr(e))\n    ...                        # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS\n    NotFittedError('This LinearSVC instance is not fitted yet',)\n    .. versionchanged:: 0.18\n       Moved from sklearn.utils.validation.\n\n    "


def check_random_state(seed):
    """Turn seed into a np.random.RandomState instance

    Parameters
    ----------
    seed : None | int | instance of RandomState
        If seed is None, return the RandomState singleton used by np.random.
        If seed is an int, return a new RandomState instance seeded with seed.
        If seed is already a RandomState instance, return it.
        Otherwise raise ValueError.

    """
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, (numbers.Integral, np.integer)):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError('%r cannot be used to seed a numpy.random.RandomState instance' % seed)


def _get_n_jobs(n_jobs):
    """Get number of jobs for the computation.

    This function reimplements the logic of joblib to determine the actual
    number of jobs depending on the cpu count. If -1 all CPUs are used.
    If 1 is given, no parallel computing code is used at all, which is useful
    for debugging. For n_jobs below -1, (n_cpus + 1 + n_jobs) are used.
    Thus for n_jobs = -2, all CPUs but one are used.

    Parameters
    ----------
    n_jobs : int
        Number of jobs stated in joblib convention.

    Returns
    -------
    n_jobs : int
        The actual number of jobs as positive integer.

    Examples
    --------
    >>> from sklearn.utils import _get_n_jobs
    >>> _get_n_jobs(4)
    4
    >>> jobs = _get_n_jobs(-2)
    >>> assert jobs == max(cpu_count() - 1, 1)
    >>> _get_n_jobs(0)
    Traceback (most recent call last):
    ...
    ValueError: Parameter n_jobs == 0 has no meaning.

    """
    if n_jobs < 0:
        return max(cpu_count() + 1 + n_jobs, 1)
        if n_jobs == 0:
            raise ValueError('Parameter n_jobs == 0 has no meaning.')
    else:
        return n_jobs


def _partition_estimators(n_estimators, n_jobs):
    """Private function used to partition estimators between jobs."""
    n_jobs = min(_get_n_jobs(n_jobs), n_estimators)
    n_estimators_per_job = n_estimators // n_jobs * np.ones(n_jobs, dtype=(np.int))
    n_estimators_per_job[:n_estimators % n_jobs] += 1
    starts = np.cumsum(n_estimators_per_job)
    return (
     n_jobs, n_estimators_per_job.tolist(), [0] + starts.tolist())