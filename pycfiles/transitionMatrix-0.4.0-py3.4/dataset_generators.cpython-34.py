# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/transitionMatrix/utils/dataset_generators.py
# Compiled at: 2018-10-22 18:32:14
# Size of source mod 2**32: 5458 bytes
import numpy as np, pandas as pd
from scipy import stats

def exponential_transitions(statespace, n, sample, rate, data_format='Compact'):
    """
    Generate continuous time events from exponential distribution and uniform sampling from state space. Suitable
    for testing cohorting algorithms and duration based estimators.

    The data are sorted by entity ID, then by time of occurence T. The first entry per entity indicates the state up
    to that timepoint. The format is a sequence of triples (ID, Time, State)

    :param statespace: The state space to use for the simulation
    :param int n: The number of distinct entities to simulate
    :param int sample: The number of events to simulate
    :param float rate: The event rate
    :return: transition events
    :rtype: pandas dataframe

    .. note:: May generate successive events in the same state

    """
    states = statespace.get_states()
    data = []
    for i in range(n):
        t = stats.expon.rvs(scale=rate, size=sample)
        t = t.cumsum()
        s = np.random.choice(states, sample)
        for e in range(sample):
            data.append((i, t[e], s[e]))

    return pd.DataFrame(data, columns=['ID', 'Time', 'State'])


def markov_chain(statespace, transitionmatrix, n, timesteps):
    """
    Generate discrete events from a markov chain matrix in Compact data format
    Suitable for testing cohort based estimators

    :type statespace: The state space to use for the simulation
    :type transitionmatrix: The transitionMatrix to use for the simulation
    :param int n: The number of distinct entities to simulate
    :param int timesteps: The number of timesteps to simulate (including initial state)
    :return: the message id
    :rtype: pandas dataframe

    """
    states = statespace.get_states()
    matrix = transitionmatrix
    data = []
    for i in range(n):
        initial_state = np.random.choice(len(states))
        k = 0
        data.append((i, k, states[initial_state]))
        p = matrix[initial_state]
        for k in range(1, timesteps):
            state = np.random.choice(len(states), p=p)
            p = matrix[state]
            data.append((i, k, states[state]))

    return pd.DataFrame(data, columns=['ID', 'Timestep', 'State'])


def long_format(statespace, transitionmatrix, n, timesteps):
    """
    Generate continuous events from a markov chain matrix in Long data format
    Suitable for testing duration based estimators

    :type statespace: The state space to use for the simulation
    :type transitionmatrix: The transitionMatrix to use for the simulation
    :param int n: The number of distinct entities to simulate
    :param int timesteps: The number of timesteps to simulate (including initial state)
    :return: the message id
    :rtype: pandas dataframe

    .. note: The observation time within timesteps is calculated using a uniform     distribution assumption

    """
    states = statespace.get_states()
    matrix = transitionmatrix
    data = []
    for i in range(n):
        from_state = np.random.choice(len(states))
        migrated = False
        p = matrix[from_state]
        for k in range(1, timesteps):
            to_state = np.random.choice(len(states), p=p)
            if to_state != from_state:
                migrated = True
                event_time = k - np.random.uniform(low=0.0, high=1.0, size=None)
                data.append((i, event_time, states[from_state], states[to_state]))
                p = matrix[to_state]
                from_state = to_state
                continue

        if not migrated:
            data.append((i, 0, states[from_state], states[from_state]))
            continue

    return pd.DataFrame(data, columns=['ID', 'Time', 'From', 'To'])