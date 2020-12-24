# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/Clumsy/sleep/detection_utils.py
# Compiled at: 2018-11-23 11:45:40
# Size of source mod 2**32: 4627 bytes
import numpy as np
from numba import jit
from ptsa.data.timeseries import TimeSeries
from scipy.stats import zscore
__all__ = [
 'find_consecutive_data',
 'find_containing_intervals',
 'chop_intervals',
 'init_channel_events',
 'jit_find_containing_intervals']

def find_consecutive_data(data, stepsize=1):
    """Splits Data into a list of arrays where there is more than a single step of 1

    Parameters
    ----------
    data: np.array of zeroes and ones, the data to split
    stepsize: int, by default 1

    Returns
    -------
    list of split data
    """
    return np.split(data, np.where(np.diff(data) != stepsize)[0] + 1)


def zscore_amp_threshold(data, minimum_amplitude=3):
    """Applies z-score threshold on data"""
    z_data = zscore(data, -1)
    above_thres = z_data > minimum_amplitude
    return above_thres


def sampling_freq_to_minimum_duration(ts, desired_length_in_ms=20):
    """Computes the minimum window length that corresponds with the desired length in ms"""
    sr = float(ts['samplerate'])
    window_length = int(float(desired_length_in_ms) / 1000 / (1 / sr))
    return window_length


@jit(nopython=True)
def jit_find_containing_intervals(channel, duration):
    """Find intervals where there is an amplitude and duration crossing

    NOTES: Uses numba to vastly improve the speed of this (x10)
           through the use of just-in-time (jit) compiling of the code
           Use the function find_containing_intervals which acts as a wrapper on this
           rather than this function itself
    ------
    INPUTS:
    ------
    channel: bool array, True if above amplitude Threshold else False

    ------
    OUTPUTS:
    ------
    (n x 2) array of start, stop indicies
    """
    count = 0
    starts, stops = [], []
    for i, j in enumerate(channel):
        if count == duration:
            starts.append(i - duration)
        if i == 0:
            continue
        if j:
            count += 1
            continue
        if not j:
            if count >= duration:
                stops.append(i)
            count = 0
            continue

    return (starts, stops)


def find_containing_intervals(ts):
    """Find intervals where there is an amplitude and duration crossing
    ------
    INPUTS:
    ------
    ts: TimeSeriesX object; instantaneous amplitude envelope

    ------
    OUTPUTS:
    ------
    data: list, [ch x array(n x 2)] of start, stop indicies
    """
    duration = sampling_freq_to_minimum_duration(ts)
    bool_arr = zscore_amp_threshold(ts)
    data = [np.vstack(jit_find_containing_intervals(channel, duration)).T for channel in bool_arr]
    return data


def chop_intervals(intervals, timeseries, ch_index, return_timeseries=False):
    """Chops intervals produced by find_containing_intervals and returns a chopped timeseries for the ch
    -----
    INPUTS:
    intervals: output of find_containing_intervals()
    timeseries: TimeSeriesX, must be amplitude envelope
    ch_index: int, index to channel
    return_timeseries: whether or not to return it as a TimeSeriesX object (True) or list (False)
    ------
    OUTPUTS:
    chopped_channel: TimeSeriesX, timeseries chopped between amplitude and duration threshold crossing
    """
    channel_interval = intervals[ch_index]
    chopped_channel = []
    for start, stop in zip(channel_interval[:, 0], channel_interval[:, 1]):
        chopped_channel.append(timeseries[ch_index, start:stop])

    if return_timeseries:
        chopped_channel = TimeSeries.concat(chopped_channel, 'time')
    return chopped_channel


def init_channel_events(intervals, ch_index, path, subject='R1293P'):
    """Creates a behavioral record array indiciating the start/stops of potential ripples
    """
    fields = np.dtype([('subject', 'O'), ('path', 'O'), ('start', int), ('stop', int), ('duration', int)])
    events = np.zeros((len(intervals[ch_index])), dtype=fields)
    events['start'] = intervals[ch_index][:, 0]
    events['stop'] = intervals[ch_index][:, 1]
    events['subject'] = np.array([subject] * len(intervals[ch_index]))
    events['path'] = np.array([path] * len(intervals[ch_index]))
    events['duration'] = events['stop'] - events['start']
    events = events.view(np.recarray)
    return events