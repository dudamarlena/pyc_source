# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/transitionMatrix/utils/preprocessing.py
# Compiled at: 2018-10-22 18:32:14
# Size of source mod 2**32: 5350 bytes
"""
module transitionMatrix.utils - helper classes and functions

"""
from __future__ import print_function, division
import numpy as np, pandas as pd

def unique_timestamps(data):
    """
    Identify unique timestamps in a dataframe

    :param data: dataframe. The 'Time' column is used by default

    :returns: returns a numpy array

    """
    unique_timestamps = data['Time'].unique()
    return unique_timestamps


def bin_timestamps(data, cohorts):
    """
    Bin timestamped data in a dataframe so as to have ingoing and outgoing states per cohort interval

    The 'Time' column is used by default

    .. note:: This is a lossy operation: Timestamps are discretised and intermediate state     transitions are lost

    """
    t_min = data['Time'].min()
    t_max = data['Time'].max()
    dt = (t_max - t_min) / cohorts
    cohort_intervals = [t_min + dt * i for i in range(0, cohorts + 1)]
    sorted_data = data.sort_values(['Time', 'ID'], ascending=[True, True])
    unique_ids = sorted_data['ID'].unique()
    cohort_assigned_state = np.empty((len(unique_ids), len(cohort_intervals)), str)
    cohort_assigned_state.fill(np.nan)
    cohort_event = np.empty((len(unique_ids), len(cohort_intervals)))
    cohort_event.fill(np.nan)
    cohort_count = np.empty((len(unique_ids), len(cohort_intervals)))
    cohort_count.fill(np.nan)
    event_dict = {}
    for row in sorted_data.itertuples():
        event_id = row[1]
        event_time = row[2]
        event_state = row[3]
        c = int((event_time - event_time % dt) / dt)
        event_key = (event_id, c)
        if event_key in event_dict.keys():
            event_dict[event_key].append((event_time, event_state))
        else:
            event_dict[event_key] = [
             (
              event_time, event_state)]

    for i in range(len(unique_ids)):
        for k in range(len(cohort_intervals)):
            event_id = i
            event_cohort = k
            event_key = (i, k)
            if event_key in event_dict.keys():
                event_list = event_dict[(i, k)]
                cohort_assigned_state[(event_id, event_cohort)] = event_list[(len(event_list) - 1)][1]
                cohort_event[(event_id, event_cohort)] = event_list[(len(event_list) - 1)][0]
                cohort_count[(event_id, event_cohort)] = int(len(event_list))
            elif event_key not in event_dict.keys() and event_cohort > 0:
                cohort_assigned_state[(event_id, event_cohort)] = cohort_assigned_state[(event_id, event_cohort - 1)]
                cohort_event[(event_id, event_cohort)] = cohort_event[(event_id, event_cohort - 1)]
                cohort_count[(event_id, event_cohort)] = cohort_count[(event_id, event_cohort - 1)]
            elif event_key not in event_dict.keys() and event_cohort == 0:
                cohort_assigned_state[(event_id, event_cohort)] = np.nan
                cohort_event[(event_id, event_cohort)] = np.nan
                cohort_count[(event_id, event_cohort)] = np.nan
                continue

    cohort_data = []
    for i in range(len(unique_ids)):
        for c in range(len(cohort_intervals)):
            cohort_data.append((i, c, cohort_assigned_state[i][c], cohort_event[i][c], cohort_count[i][c]))

    cohort_data = pd.DataFrame(cohort_data, columns=['ID', 'Cohort', 'State', 'EventTime', 'Count'])
    return (cohort_data, cohort_intervals)