# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/Clumsy/signal/butterworth.py
# Compiled at: 2018-11-21 20:12:55
# Size of source mod 2**32: 11786 bytes
__doc__ = 'butterworth.py script used for consctructing various Butterworth Filters'
import numpy as np
from scipy.signal import filtfilt, firwin, sosfiltfilt, butter, tf2zpk
try:
    from collections import Sequence
except ImportError as e:
    try:
        print('Import error from collections import Sequence')
    finally:
        e = None
        del e

except Exception as e:
    try:
        print(e)
    finally:
        e = None
        del e

from copy import deepcopy
import warnings
from xarray import DataArray
from ptsa.data.timeseries import TimeSeries
from ptsa.data.common import get_axis_index
from ptsa.data.filters import BaseFilter
import traits.api
from Clumsy.signal.timeseriesLF import TimeSeriesLF
__all__ = [
 'butterworth_filter', 'ButterworthFilter', 'check_stability', 'FIR_bandpass_filter']

def check_stability(b, a):
    """utility function that checks the stability of the denom and nom of a filter to ensure it's valid

    Parameters
    ----------
    b: Numerator polynomials of the IIR filter
    a: Denominator polynomials of the IIR filter

    Returns
    -------
    None or a warning if unstable filter

    Example Use:
    --------
    b,a = butter(inputs)
    check_stability(b,a)
    """
    z, p, k = tf2zpk(b, a)
    try:
        assert np.max(np.abs(p)) <= 1
    except:
        unstable_msg = 'Filter is not stable! np.max(np.abs(p)) must be less than 1 but instead is: {} please use sos approach instead'
        warnings.warn(unstable_msg.format(np.max(np.abs(p))), UserWarning)


def apply_correct_filter(filter_inputs, correct_filter, dat, axis):
    """Utility function to apply correct filter to butterworth

    Parameters
    ----------
    filter_inputs: single argument or argument in tuple
    correct_filter: correct filter to apply either filtfilt or sosfiltfilt
    dat: data to apply filter on
    axis: axis on which to apply the filter

    Returns
    -------
    Filtered data
    """
    if type(filter_inputs) == tuple:
        return correct_filter(filter_inputs, *(dat,), **{'axis': axis})
    return correct_filter(filter_inputs, dat, axis=axis)


def butterworth_filter(data=None, freq=(1, 100), filt_type='bandpass', order=4, sample_rate=None, axis=-1, filter_output='sos', linear_filter=False):
    """
    Function for applying a butterworth filter onto data.

    Parameters
    ----------
    data: TimeSeries like
    freq: array-like or int/float depending on filt_type
    filt_type: filter type to use (e.g. 'pass', 'high', 'low', 'highpass',
                'lowpass', 'bandpass', 'band', 'stop', 'bandstop')
    order: int, order of the filter
    sample_rate: int/float, number of samples in a second
    axis: int, axis to filter by default -1
    filter_output: output method for filter, by uses default second order sections
                 valid = ('ba', 'sos')
    linear_filter: bool, NOT IMPLEMENTED YET

    Returns
    -------

    """
    valid_filt_type = ('pass', 'high', 'low', 'highpass', 'lowpass', 'bandpass', 'band',
                       'stop', 'bandstop')
    if filt_type not in valid_filt_type:
        raise ValueError('{} was not found in not valid filters\n{}'.format(filt_type, valid_filt_type))
    elif filt_type in ('high', 'low', 'lowpass', 'highpass'):
        if not type(freq) == float:
            if not type(freq) == int:
                _warning = 'Please use an int or a float for freq input, inputted freq={},type(freq)={}'
                raise TypeError(_warning.format(freq, type(freq)))
        else:
            is_timeseries = True if issubclass(type(data), TimeSeries) else False
            if is_timeseries:
                coords = data.coords
                dims = data.dims
                attrs = data.attrs
                name = data.name
                if sample_rate is None:
                    sample_rate = float(data['samplerate'].data)
        nyquist = sample_rate / 2
        if filt_type in ('low', 'high', 'highpass', 'lowpass'):
            Wn = freq / nyquist
    else:
        Wn = np.asarray(freq) / nyquist
    correct_filter = sosfiltfilt if filter_output == 'sos' else filtfilt
    if linear_filter:
        raise NotImplementedError('linear_filt not implemented yet')
    constructed_filter = butter(N=order, Wn=Wn,
      btype=filt_type,
      analog=False,
      output=filter_output)
    if filter_output != 'sos':
        check_stability(*constructed_filter)
    filtered_data = apply_correct_filter(filter_inputs=constructed_filter, correct_filter=correct_filter,
      dat=(np.array(data)),
      axis=axis)
    if is_timeseries:
        return TimeSeriesLF(data=filtered_data, coords=coords, dims=dims, attrs=attrs, name=name)
    return filtered_data


class ButterworthFilter(BaseFilter):
    """ButterworthFilter"""
    order = traits.api.Int
    filt_type = traits.api.Str
    design_valid = ('sos', 'ba', 'zpk')
    valid_filt_type = ('pass', 'high', 'low', 'highpass', 'lowpass', 'bandpass', 'band',
                       'stop', 'bandstop')

    def __init__(self, timeseries, freq_range, order=4, filt_type='stop', filter_output='sos'):
        super(ButterworthFilter, self).__init__(timeseries)
        self.freq_range = freq_range
        self.order = order
        self.filt_type = filt_type
        self.filter_output = filter_output

    def filter(self):
        """
        Applies Butterworth filter to input time series and returns filtered TimeSeries object
        Returns
        -------
        filtered: TimeSeries
            The filtered time series
        """
        time_axis_index = get_axis_index((self.timeseries), axis_name='time')
        filtered_array = butterworth_filter(data=(np.array(self.timeseries)), freq=(self.freq_range),
          filt_type=(self.filt_type),
          sample_rate=(float(self.timeseries['samplerate'])),
          axis=time_axis_index,
          filter_output=(self.filter_output),
          order=(self.order),
          linear_filter=False)
        if issubclass(type(filtered_array), TimeSeries):
            return filtered_array
        coords_dict = {coord_name:DataArray(coord.copy()) for coord_name, coord in list(self.timeseries.coords.items())}
        coords_dict['samplerate'] = self.timeseries['samplerate']
        dims = [dim_name for dim_name in self.timeseries.dims]
        filtered_timeseries = TimeSeries(filtered_array, dims=dims, coords=coords_dict)
        filtered_timeseries.attrs = self.timeseries.attrs.copy()
        return filtered_timeseries


def FIR_bandpass_filter(data, lowcut, highcut, fs, order=1000, window='hanning'):
    """Applies a forward reverse FIR bandpass filter according to the parameters
    ----------
    data : TimeSeries or array_like
        The data we would like to apply a bandpass to
    lowcut : float or 1D array_like
        Low cutoff frequency of filter (expressed in the same units as `nyq`)
        The values 0 and `nyq` must not be included in `lowcut`.
    highcut : float or 1D array_like
        High cutoff frequency of filter (expressed in the same units as `nyq`)
        The values 0 and `nyq` must not be included in `highcut`.
    fs : float or 1D array_like
        Sampling frequency of the timeseries

    Order : int or float, by default 1000
        The order of the filter to compute. Increasing the value give better frequency
        resolution of worse temporal resolution
    window : string or tuple of string and parameter values, by default hanning.
        Desired window to use. See `scipy.signal.get_window` for a list
        of windows and required parameters.

    Returns
    -------
    data_filt_ts: TimeSeries
        Data filtered between lowcut and highcut as a TimeSeries object
    data_filt: array_like
        Data filtered between lowcut and highcut as an array_like object

    References
    ----------
    https://gist.github.com/andrewgiessel/7589513
    http://mpastell.com/2010/01/18/fir-with-scipy/
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html#scipy.signal.filtfilt
    """
    n = order + 1
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    lowpass_filt = firwin(n, cutoff=low, window=window)
    highpass_filt = -firwin(n, cutoff=high, window=window)
    highpass_filt[n // 2] = highpass_filt[(n // 2)] + 1
    band_pass_filt = -(lowpass_filt + highpass_filt)
    band_pass_filt[n // 2] = band_pass_filt[(n // 2)] + 1
    data_filt = filtfilt(b=band_pass_filt, a=[1], x=data)
    if issubclass(type(data), TimeSeries):
        data_filt_ts = deepcopy(data)
        data_filt_ts.data = data_filt
        return data_filt_ts
    return data_filt