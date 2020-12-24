# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/Clumsy/signal/notchfilter.py
# Compiled at: 2018-11-05 17:00:12
# Size of source mod 2**32: 1892 bytes
import mne.filter as _notch_filter
from ptsa.data.common import get_axis_index
from ptsa.data.timeseries import TimeSeries
from Clumsy.signal.rolling import reorder_dims
import numpy as np

def notch_filter(timeseries, europe=False):
    """Wrapper around mne's notch_filter function

    Parameters
    ----------
    timeseries
    europe

    Returns
    -------
    notch filtered data (no line noise)

    Notes
    -------
    mne implicitly assumes that time is the last dimension in the timeseries
    """
    reordered = False
    if (len(timeseries.shape) > 1) & (get_axis_index(timeseries, 'time') + 1 != len(timeseries.shape)):
        reordered = True
        timeseries = reorder_dims(timeseries, -1, get_axis_index(timeseries, 'time'))
    freqs = np.arange(60, 241, 60) if not europe else np.arange(50, 201, 50)
    filtered = _notch_filter(x=(timeseries.data.astype(np.float64)), Fs=(timeseries['samplerate']), freqs=freqs)
    return TimeSeries(filtered, coords=(timeseries.coords), dims=(timeseries.dims))


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    np.random.seed(0)
    t = np.arange(0, 2, 0.001)
    x = 30 * np.random.randn(len(t)) + 50 * np.sin(t * 2 * np.pi * 1.3) + 30 * np.sin(t * 2 * np.pi * 18 - 0.3)
    x[500:1000] += 80 * np.sin(t[500:1000] * 2 * np.pi * 10)
    Fs = 1000
    alpha = (8, 12)
    y = x + 80 * np.sin(t * 2 * np.pi * 60)
    ts = TimeSeries(data=y, coords={'time':t,  'samplerate':Fs}, dims=['time'])
    filtered = notch_filter(timeseries=ts)
    fig, ax = plt.subplots(ncols=3, figsize=(12, 4))
    ax[0].plot(x)
    ax[1].plot(ts)
    ax[2].plot(filtered)
    plt.show()