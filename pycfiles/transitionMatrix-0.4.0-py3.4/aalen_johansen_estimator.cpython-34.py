# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/transitionMatrix/estimators/aalen_johansen_estimator.py
# Compiled at: 2018-10-22 18:32:14
# Size of source mod 2**32: 7728 bytes
from __future__ import print_function
import numpy as np, transitionMatrix as tm
from transitionMatrix.estimators import DurationEstimator

class AalenJohansenEstimator(DurationEstimator):
    __doc__ = '\n    Class for implementing the Aalen-Johansen estimator for the transition matrix\n\n\n    '

    def __init__(self, cohort_intervals=None, states=None):
        DurationEstimator.__init__(self)
        self.cohort_intervals = cohort_intervals
        if states is not None:
            self.states = states
        self.etm = None
        self.times = None

    def fit(self, data, labels=None):
        """
        Parameters
        ----------
        data : dataframe
            The data to use for the estimation provided in a pandas data frame in long format,
            with one row per observed transition. The data frame must contain the following columns:
            – ID: A unique entity identification number
            – FROM: State from where a transition occurs
            – TO: State to which a transition occurs
            – TIME Time when a transition occurs

        labels: a dictionary for relabeling column names

        TODO constraint possible transitions (absorbing states)
        TODO censored data
        TODO partial dates
        TODO covariance calculation
        TODO confidence intervals

        Returns
        -------
        etm.values : estimated empirical transition matrix throughout the observed interval.
        This is a three dimensional array object (From State, To State, Timepoint)
        observation_times: a list of observation times
        etm.observation_times

        TODO Store counts as well as frequencies
        TODO Optional Binning of close observation times

        Notes
        ------

        The input data MUST be sorted in ascending time order

        """
        state_dim = self.states.cardinality
        observation_times = tm.utils.unique_timestamps(data)
        event_count = data['ID'].count()
        event_id = np.empty(event_count, int)
        event_from_state = np.empty(event_count, int)
        event_to_state = np.empty(event_count, int)
        event_time = np.empty(event_count, float)
        event_timepoint = np.empty(event_count, int)
        event_exists = np.empty(event_count, bool)
        event_exists.fill(False)
        nan_count = 0
        i = 0
        t = 0
        for row in data.itertuples():
            try:
                event_id[i] = row[1]
                event_time[i] = row[2]
                event_from_state[i] = int(row[3])
                event_to_state[i] = int(row[4])
                if event_to_state[i] != event_from_state[i]:
                    event_exists[i] = True
                if i == 0:
                    event_timepoint[i] = 0
                else:
                    if i > 0 and event_time[i] > event_time[(i - 1)]:
                        t += 1
                        event_timepoint[i] = t
                    elif i > 0:
                        if event_time[i] == event_time[(i - 1)]:
                            event_timepoint[i] = t
            except ValueError:
                nan_count += 1

            i += 1

        self.nans = nan_count
        self.counts = event_count
        self.timepoint_count = t
        print('Events ', self.counts)
        print('NaNs ', self.nans)
        unique_ids = list(data['ID'].unique())
        y_initial_count = np.zeros((state_dim,), dtype=int)
        for i in range(0, event_count - 1):
            if event_id[i] in unique_ids:
                item = unique_ids.index(event_id[i])
                y_initial_count[int(event_from_state[i])] += 1
                unique_ids.pop(item)
                continue

        etm = np.zeros((state_dim, state_dim, self.timepoint_count), dtype=float)
        etm[:, :, 0] = np.eye(state_dim, state_dim)
        dN = np.zeros((state_dim, state_dim, self.timepoint_count), dtype=int)
        y = np.zeros((state_dim, self.timepoint_count), dtype=int)
        y[:, 0] = y_initial_count
        dA = np.zeros((state_dim, state_dim, self.timepoint_count), dtype=float)
        for i in range(0, event_count - 1):
            if event_exists[i]:
                if event_timepoint[i] > 0:
                    dN[(event_from_state[i], event_to_state[i], event_timepoint[i])] += 1
                else:
                    continue

        for k in range(1, self.timepoint_count - 1):
            for m in range(0, state_dim):
                migration_to_m = 0
                migration_from_m = 0
                for n in range(0, state_dim):
                    if n != m:
                        migration_to_m += dN[(n, m, k)]
                        migration_from_m += dN[(m, n, k)]
                        continue

                y[(m, k)] = y[(m, k - 1)] + migration_to_m - migration_from_m
                dN[(m, m, k)] = migration_from_m

        for k in range(1, self.timepoint_count - 1):
            for m in range(0, state_dim):
                for n in range(0, state_dim):
                    if y[(m, k)] != 0:
                        if m != n:
                            dA[(m, n, k)] = dN[(m, n, k)] / y[(m, k)]
                        else:
                            dA[(m, m, k)] = -dN[(m, m, k)] / y[(m, k)]
                    else:
                        dA[(m, n, k)] = 0

        identity = np.eye(state_dim, dtype=float)
        for k in range(1, self.timepoint_count):
            for m in range(0, state_dim):
                for n in range(0, state_dim):
                    for q in range(0, state_dim):
                        etm[(m, n, k)] += etm[(m, q, k - 1)] * (identity[(q, n)] + dA[(q, n, k)])

        self.etm = etm
        self.times = observation_times
        return (
         self.etm, self.times)