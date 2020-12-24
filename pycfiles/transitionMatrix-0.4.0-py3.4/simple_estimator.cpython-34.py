# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/transitionMatrix/estimators/simple_estimator.py
# Compiled at: 2018-10-22 18:32:14
# Size of source mod 2**32: 4856 bytes
from __future__ import print_function
import numpy as np
from transitionMatrix.estimators import BaseEstimator
import statsmodels.stats.proportion as st

class SimpleEstimator(BaseEstimator):
    __doc__ = '\n    Class for implementing a simple estimator suitable for single period transitions\n\n    '

    def __init__(self, cohort_intervals=None, states=None, ci=None):
        BaseEstimator.__init__(self)
        if states is not None:
            self.states = states
        if ci is not None:
            assert ci['method'] in ('goodman', 'sison-glaz', 'binomial')
            self.ci_method = ci['method']
            self.ci_alpha = ci['alpha']

    def fit(self, data):
        """
        Parameters
        ----------
        data : array-like
            The data to use for the estimation

        Returns
        -------
        matrix : estimated transition matrix
        confint_lower: lower confidence interval
        confint_upper: upper confidence interval

        Notes
        ------
        """
        state_count = self.states.cardinality
        state_list = self.states.get_states()
        tm_count = np.ndarray(state_count)
        tmn_count = np.ndarray((state_count, state_count))
        tm_count.fill(0.0)
        tmn_count.fill(0.0)
        i = 0
        for row in data.itertuples():
            state_in = state_list.index(row[2])
            state_out = state_list.index(row[3])
            tm_count[state_in] += 1
            tmn_count[(state_in, state_out)] += 1
            i += 1

        self.counts = int(tm_count.sum())
        confint_lower = np.ndarray((state_count, state_count, 1))
        confint_upper = np.ndarray((state_count, state_count, 1))
        for s1 in range(state_count):
            intervals = st.multinomial_proportions_confint(tmn_count[s1, :], alpha=self.ci_alpha, method=self.ci_method)
            for s2 in range(state_count):
                confint_lower[(s1, s2, 0)] = intervals[s2][0]
                confint_upper[(s1, s2, 0)] = intervals[s2][1]

        self.confint_lower = confint_lower
        self.confint_upper = confint_upper
        for s1 in range(state_count):
            for s2 in range(state_count):
                if tm_count[s1] > 0:
                    tmn_count[(s1, s2)] = tmn_count[(s1, s2)] / tm_count[s1]
                    continue

        self.matrix_set.append(tmn_count)
        return self.matrix_set