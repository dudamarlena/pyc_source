# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/Clumsy/signal/hilbert.py
# Compiled at: 2018-11-05 17:00:12
# Size of source mod 2**32: 3214 bytes
import numpy as np
from xarray import DataArray
from numpy import ceil, log2
from ptsa.data.timeseries import TimeSeries
from ptsa.data.common import get_axis_index
from ptsa.data.filters import BaseFilter, ButterworthFilter
from scipy.signal import hilbert
from copy import deepcopy
import xarray as xr
__all__ = ['HilbertFilter']

class HilbertFilter(BaseFilter):
    """HilbertFilter"""

    def __init__(self, timeseries):
        super(HilbertFilter, self).__init__(timeseries)

    def filter(self):
        """

        Returns
        -------

        """
        time_axis = get_axis_index(self.timeseries, 'time')
        padding = int(2 ** ceil(log2(self.timeseries.shape[time_axis])))
        output = hilbert((self.timeseries), N=padding, axis=time_axis)
        valid_pad = (
         Ellipsis, slice(self.timeseries.shape[time_axis]))
        returned_signal = output[valid_pad]
        coords_dict = {coord_name:DataArray(coord.copy()) for coord_name, coord in list(self.timeseries.coords.items())}
        coords_dict['samplerate'] = self.timeseries['samplerate']
        dims = [dim_name for dim_name in self.timeseries.dims]
        filtered_timeseries = TimeSeries(returned_signal, dims=dims, coords=coords_dict)
        filtered_timeseries.attrs = self.timeseries.attrs.copy()
        return filtered_timeseries


from ptsa.data.timeseries import TimeSeries
from scipy.signal import hilbert

def Hilbert(signal):
    """Applies a hilbert transform to the signal (must be a single channel)

    ### IMPORTANT NOTES####
    This function adds zero padding to speed up the processing of the fast
    fourier transformation(FFT) if the length of the signal passed is
    not a power of two (for example a 49999 lengthed signal
    will take orders of magnitude longer than a 50000 lengthed signal to
    compute a Fast fourier transformation on )

    ------
    INPUTS:
    signal: array like or TimeSeries, MUST BE A SINGLE CHANNEL.
    ------
    OUTPUTS:
        signal: TimeSeriesX, a TimeSeries object of shape signal that is hilbert filtered
    """
    padding = np.zeros(int(2 ** np.ceil(np.log2(len(signal)))) - len(signal))
    tohilbert = np.hstack((signal, padding))
    result = hilbert(tohilbert)
    result = result[0:len(signal)]
    if type(signal) == TimeSeries:
        return TimeSeries(data=result, dims=(signal.dims), coords=(signal.coords))
    return result


def get_amplitude_envelope(signal):
    """Returns that instantaneous amplitude envelope of the analytic signal
       from the Hilbert transformation
    ------
    INPUTS:
    signal: array like or TimeSeriesX.
    """
    _xarray = np.abs(Hilbert(signal))
    return TimeSeries(_xarray, coords=(_xarray.coords))