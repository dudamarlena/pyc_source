# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/transitionMatrix/estimators/cohort_estimator.py
# Compiled at: 2018-10-22 18:32:14
# Size of source mod 2**32: 6940 bytes
from __future__ import print_function
import numpy as np, statsmodels.stats.proportion as st
from transitionMatrix.estimators import BaseEstimator

class CohortEstimator(BaseEstimator):
    __doc__ = '\n    Class for implementing a Cohort estimator for the transition matrix\n    under the assumption of time homogeneity\n\n    '

    def __init__(self, cohort_intervals=None, states=None, ci=None):
        BaseEstimator.__init__(self)
        self.cohort_intervals = cohort_intervals
        if states is not None:
            self.states = states
        if ci is not None:
            assert ci['method'] in ('goodman', 'sison-glaz', 'binomial')
            assert 0 < ci['alpha'] <= 1.0
            self.ci_method = ci['method']
            self.ci_alpha = ci['alpha']

    def fit(self, data, labels=None):
        """
        Parameters
        ----------
        data : array-like
            The data to use for the estimation

        labels: a dictionary for relabeling column names

        Returns
        -------
        matrix : estimated transition matrix
        confint_lower: lower confidence interval
        confint_upper: upper confidence interval

        Notes
        ------
        """
        if labels is not None:
            state_label = labels['State']
            timestep_label = labels['Timestamp']
            id_label = labels['ID']
        else:
            state_label = 'State'
            id_label = 'ID'
            timestep_label = 'Timestep'
        state_dim = self.states.cardinality
        cohort_labels = data[timestep_label].unique()
        cohort_dim = len(cohort_labels) - 1
        event_count = data[id_label].count()
        event_exists = np.empty(event_count, int)
        event_id = np.empty(event_count, int)
        event_state = np.empty(event_count, int)
        event_time = np.empty(event_count, int)
        nan_count = 0
        i = 0
        for row in data.itertuples():
            try:
                event_state[i] = int(row[3])
                event_id[i] = row[1]
                event_time[i] = int(row[2])
                event_exists[i] = 1
            except ValueError:
                nan_count += 1

            i += 1

        self.nans = nan_count
        tm_count = np.ndarray((state_dim, cohort_dim), int)
        tmn_count = np.ndarray((state_dim, state_dim, cohort_dim), int)
        tm_count.fill(0)
        tmn_count.fill(0)
        tmn_values = np.ndarray((state_dim, state_dim, cohort_dim), float)
        tmn_values.fill(0.0)
        for i in range(1, event_count - 1):
            if event_exists[i] == 1:
                if event_id[(i + 1)] == event_id[i]:
                    tm_count[(event_state[i], event_time[i])] += 1
                    tmn_count[(event_state[i], event_state[(i + 1)], event_time[i])] += 1
                else:
                    continue

        i = 0
        if event_exists[i] == 1:
            if event_id[(i + 1)] == event_id[i]:
                tm_count[(event_state[i], event_time[i])] += 1
                tmn_count[(event_state[i], event_state[(i + 1)], event_time[i])] += 1
        self.counts = int(tm_count.sum())
        confint_lower = np.ndarray((state_dim, state_dim, cohort_dim))
        confint_upper = np.ndarray((state_dim, state_dim, cohort_dim))
        for k in range(cohort_dim):
            for s1 in range(state_dim):
                intervals = st.multinomial_proportions_confint(tmn_count[s1, :, k], alpha=self.ci_alpha, method=self.ci_method)
                for s2 in range(state_dim):
                    confint_lower[(s1, s2, k)] = intervals[s2][0]
                    confint_upper[(s1, s2, k)] = intervals[s2][1]

            self.confint_lower = confint_lower
            self.confint_upper = confint_upper

        for s1 in range(state_dim):
            for s2 in range(state_dim):
                for k in range(cohort_dim):
                    if tm_count[(s1, k)] > 0:
                        tmn_values[(s1, s2, k)] = tmn_count[(s1, s2, k)] / tm_count[(s1, k)]
                        continue

        for k in range(cohort_dim):
            self.matrix_set.append(tmn_values[:, :, k])
            self.count_set.append(tmn_count[:, :, k])
            self.count_normalization.append(tm_count[:, k])

        return self.matrix_set