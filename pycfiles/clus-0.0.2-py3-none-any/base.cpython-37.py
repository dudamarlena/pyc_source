# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/Clumsy/sleep/base.py
# Compiled at: 2018-11-24 16:08:24
# Size of source mod 2**32: 6969 bytes
__doc__ = 'base.py Script for base detector that other detectors inherit from'
from ptsa.data.timeseries import TimeSeries
from ptsa.data.common import get_axis_index
from scipy.stats import zscore
import numpy as np, pandas as pd
from Clumsy import rolling_window_full, ButterworthFilter
from numba import jit
import traits.api
from .detection_utils import jit_find_containing_intervals, find_consecutive_data
__all__ = [
 'BaseDetector']

class BaseDetector(traits.api.HasTraits):
    """BaseDetector"""
    valid = {'spindles':[
      'rms'], 
     'ripples':[
      'buzsaki'], 
     'slow-waves':[
      'amplitude', 'duration', 'fast'], 
     'ied':[
      'buzsaki']}
    time_series = traits.api.Instance(TimeSeries)
    event_type = traits.api.Str
    method = traits.api.Str

    def __init__(self, time_series, event_type=None, method=None):
        """

        Parameters
        ----------
        time_series:TimeSeriesLF/ TimeSeries object,
        event_type
        method
        """
        if not issubclass(type(time_series), TimeSeries):
            raise TypeError('Please input a time_series object')
        super(BaseDetector, self).__init__()
        self.time_series = time_series
        self.event_type = event_type
        self.method = method

    @staticmethod
    def remove_linenoise(ts, harmonic=1, line_noise=60):
        for i in np.arange(1, harmonic + 1):
            freqs = (
             line_noise * i - 2, line_noise * i + 2)
            ts = ts.filter_with(ButterworthFilter, freq_range=freqs, order=4, filt_type='stop', filter_output='sos')

        return ts

    def _dim_to_axis(self, dim):
        return get_axis_index(self.time_series, dim)

    def _duration_to_samples(self, duration):
        return self.time_series._TimeSeries__duration_to_samples(duration)

    @staticmethod
    def find_intervals(boolean_arr, min_sample, max_sample, contacts_df=None):
        """Find intervals where there is an amplitude and duration crossing

        Parameters
        ----------
        boolean_arr: np.array dtype=bool, shape = n chs x samples
                     Array indicating True if valid amplitude threshold or False if not
        min_sample: minimum time in samples to count as a valid duration interval
        max_sample: int or None,
                    minimum time in samples to count as a valid duration interval
        contacts_df: CMLReader contacts data frame

        Returns
        -------

        """
        try:
            fs_roi = contacts_df['ind.region']
            stein_roi = contacts_df['stein.region']
            hemi = ['left' if x == -1 else 'right' for x in np.sign(contacts_df['ind.x'])]
            channels = contacts_df['label']
        except AttributeError:
            fs_roi = ''
            stein_roi = ''
            hemi = ''
            channels = ''
        except Exception as e:
            try:
                print(e)
                fs_roi = ''
                stein_roi = ''
                hemi = ''
                channels = ''
            finally:
                e = None
                del e

        dataframe = []
        for index, ch_arr in enumerate(boolean_arr):
            start, stops = jit_find_containing_intervals(ch_arr, min_sample)
            df = pd.DataFrame(start, columns=['start'])
            try:
                df['stop'] = stops
            except ValueError as e:
                try:
                    if len(start) != len(stops):
                        continue
                    print(e)
                finally:
                    e = None
                    del e

            df['duration'] = df['stop'] - df['start']
            df['channel'] = channels[index]
            df['fs region'] = fs_roi[index]
            df['hemisphere'] = hemi[index]
            df['stein region'] = stein_roi[index]
            if max_sample is not None:
                df = df[(df['duration'] < max_sample)]
            dataframe.append(df)

        try:
            return pd.concat(dataframe)
        except ValueError as e:
            try:
                print(e)
                return dataframe
            finally:
                e = None
                del e

    def rootmeansquare(self, window, asteps=None):
        """Applies a moving root mean square of window seconds over timeseries

        Parameters
        ----------
        window: float/int, Time in seconds to apply window over
        asteps: float/int, Time in seconds to allow window non-overlap
                 Aligned at the last axis, new steps for the original array, ie. for
                 creation of non-overlapping windows. (Equivalent to slicing result)

        Returns
        -------
        rms: np.array, array of root mean square
        """
        window_size = self.time_series._TimeSeries__duration_to_samples(window)
        asteps = self.time_series._TimeSeries__duration_to_samples(asteps)
        rolled_data = rolling_window_full((self.time_series.data ** 2), window=window_size, asteps=asteps)
        rms = np.mean(rolled_data, -1)
        rms = np.sqrt(rms)
        return rms

    @staticmethod
    def percentile_threshold(data, threshold=92, axis=1):
        """Apply a percentile based threshold to the data

        Parameters
        ----------
        data: array_like
              data to apply threshold on
        threshold: array_like of float
                   Percentile or sequence of percentiles to compute, which must be between
                   0 and 100 inclusive.
        axis: int
              axis to threshold over

        Returns
        -------
        bool_arr, locations where inputted data is above desired threshold
        """
        percentiles = np.percentile(data, q=threshold, axis=axis)
        return data > percentiles[:, None]

    @staticmethod
    def zscore_threshold(data, threshold=3, axis=-1):
        """Use z-score to find out where data is at n threshold above the standard deviation of the mean

        Parameters
        ----------
        data
        threshold
        axis

        Returns
        -------
        bool_arr, locations where inputted data is above desired threshold
        """
        zdata = zscore(data, axis=axis)
        return zdata > threshold

    @staticmethod
    def threshold_value_from_array(data, threshold):
        return data > threshold