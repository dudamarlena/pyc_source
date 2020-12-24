# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/Clumsy/sleep/detect.py
# Compiled at: 2018-11-24 16:09:03
# Size of source mod 2**32: 11712 bytes
__doc__ = 'detect.py Module for detection of ripples, spindles, and inter-ictal discharges'
from ptsa.data.timeseries import TimeSeries
from ptsa.data.common import get_axis_index
from scipy.stats import zscore
from Clumsy import rolling_window_full, ButterworthFilter
from numba import jit
import traits.api, numpy as np, pandas as pd
from Clumsy import HilbertFilter
from .detection_utils import jit_find_containing_intervals, find_consecutive_data
from .base import BaseDetector
__all__ = [
 'SpindleDetector',
 'IEDDetector',
 'RippleDetector',
 'BaseDetector']

class SpindleDetector(BaseDetector):
    """SpindleDetector"""
    min_sample, max_sample = (0.5, 3.0)
    min_freq, max_freq = (11.0, 16.0)
    methods = {'rms': {'window':0.2,  'asteps':None, 
             'freq':(11.0, 16), 
             'threshold':92}}

    def __init__(self, time_series, event_type='spindle', method='rms', duration=(0.5, 3)):
        super(BaseDetector, self).__init__(time_series=time_series, event_type=event_type, method=method)
        self.min_sample = self.time_series._TimeSeries__duration_to_samples(duration[0])
        self.max_sample = self.time_series._TimeSeries__duration_to_samples(duration[1])

    def rms(self):
        self.rootmeansquare(window=0.2, asteps=None, dim='time')

    @staticmethod
    def find_intervals(boolean_arr, min_sample, max_sample, contacts_df=None):
        """Find intervals where there is an amplitude and duration crossing
        ------
        INPUTS:
        ------
        ts: TimeSeriesLF object

        ------
        OUTPUTS:
        ------
        data: list, [ch x array(n x 2)] of start, stop indicies
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


class IEDDetector(BaseDetector):
    """IEDDetector"""
    methods = {'buzsaki': {'thres_filtered':2,  'thres_unfiltered':2, 
                 'freq_range':(25, 80)}}

    def __init__(self, time_series, event_type='ied', method='buzsaki'):
        super(BaseDetector, self).__init__(time_series=time_series, event_type=event_type, method=method)
        self.method_d = IEDDetector.methods[method]
        self.frequency = self.method_d['freq_range']

    def detect_ied(self):
        ts = self.remove_linenoise((self.time_series), harmonic=2, line_noise=60)
        ied = ts.filter_with(ButterworthFilter, freq_range=(self.frequency), order=4,
          filt_type='pass',
          filter_output='sos')
        thres_filtered = self.method_d['thres_filtered']
        thres_unfiltered = self.method_d['thres_unfiltered']
        mean = np.mean(ied.data, 1)
        std = np.std(ied.data, 1)
        thres = mean + thres_filtered * std
        thres = thres[:, None]
        boolean_array = ied.data > thres
        mean_raw = np.abs(ts).mean('time')
        std_raw = np.abs(ts).std('time')
        thres_raw = mean_raw.data + thres_unfiltered * std_raw.data
        thres_raw = thres_raw[:, None]
        bool_raw = self.time_series.data > thres_raw
        return bool_raw & boolean_array

    def detect(self):
        boolean_arr = self.detect_ied()
        dfs = []
        for i, boolean_ch in enumerate(boolean_arr):
            consec = find_consecutive_data(np.where(boolean_ch)[0])
            try:
                consec = np.array([x[0] for x in consec])
            except IndexError as e:
                try:
                    continue
                finally:
                    e = None
                    del e

            consec = consec[np.append(True, np.diff(consec) > self._duration_to_samples(duration=1.0))]
            df = pd.DataFrame(consec, columns=['samples'])
            df['channel'] = str(self.time_series.channels[i].data)
            df['event'] = 'IED'
            dfs.append(df)

        try:
            return pd.concat(dfs)
        except ValueError as e:
            try:
                return dfs
            finally:
                e = None
                del e


class RippleDetector(BaseDetector):
    methods = {'buzsaki': {'method':'zscore',  'value threshold':3.0, 
                 'freq_range':(80, 250), 
                 'duration threshold':0.2}}

    def __init__(self, time_series, event_type='ripple', method='buzsaki'):
        super(BaseDetector, self).__init__(time_series=time_series, event_type=event_type, method=method)
        self.method_d = RippleDetector.methods[method]
        self.frequency = self.method_d['freq_range']
        self.order = 4

    @staticmethod
    def _ripple_filter_amplitude_envelope(ts, freq_range=(80, 250), order=4):
        """

        Parameters
        ----------
        ts
        freq_range
        order

        Returns
        -------

        """
        ripple_filt = ts.filter_with(ButterworthFilter, freq_range=freq_range, order=order, filt_type='pass',
          filter_output='sos')
        ripple_filt = ripple_filt.filter_with(HilbertFilter)
        ripple_filt.data = np.abs(ripple_filt)
        return ripple_filt

    def ripple_filter_amplitude_envelope(self):
        return self._ripple_filter_amplitude_envelope(ts=(self.time_series), freq_range=(self.frequency), order=(self.order))

    def detect(self, ripple_filt, contacts):
        from Clumsy import chop_intervals, gaussian_smooth, RippleDetector, SpindleDetector
        ripple_filt = self.ripple_filter_amplitude_envelope()
        ripple_filt = gaussian_smooth(ripple_filt)
        boolean_arr = RippleDetector.zscore_threshold(ripple_filt, threshold=3, axis=(-1))
        min_sample, max_sample = (0.2, None)
        min_sample = ripple_filt._TimeSeries__duration_to_samples(min_sample)
        df = BaseDetector.find_intervals(boolean_arr, min_sample, max_sample, contacts)