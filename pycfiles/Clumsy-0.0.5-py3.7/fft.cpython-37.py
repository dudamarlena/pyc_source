# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/Clumsy/signal/fft.py
# Compiled at: 2018-11-21 20:12:55
# Size of source mod 2**32: 4263 bytes
import numpy as np
from ptsa.data.common import get_axis_index
from ptsa.data.timeseries import TimeSeries
from scipy import signal
from Clumsy.signal.timeseriesLF import TimeSeriesLF
__all__ = [
 'psd']

def psd(x, Fs=None, method='mean', window='hann', nperseg=None, noverlap=None, filtlen=1.0):
    """

    Estimating the power spectral density (PSD) of a time series from short-time Fourier
    Transform (mean, median), or the entire signal's FFT smoothed (medfilt).
    Parameters
    -----------
    x : array_like 1d
        Time series of measurement values.
    Fs : float, Hz
        Sampling frequency of the x time series.
    method : { 'mean', 'median', 'medfilt'}, optional
        Methods to calculate the PSD. Defaults to 'mean'.
            'mean' is the same as Welch's method (mean of STFT).
            'median' uses median of STFT instead of mean to minimize outlier effect.
            'medfilt' filters the entire signal raw FFT with a median filter to smooth.
    The next 3 parameters are only relevant for method = {'mean', 'median'}
    window : str or tuple or array_like, optional
        Desired window to use. Defaults to a Hann window.
            See scipy.signal.get_window for a list of windows and required parameters.
            If window is array_like, this array will be used as the window and its length must be nperseg.
    nperseg : int, optional
        Length of each segment, in number of samples. Defaults to None.
            If None, and window is str or tuple, is set to 1 second of data.
            If None, and window is array_like, is set to the length of the window.
    noverlap : int, optional
        Number of points to overlap between segments. If None, noverlap = nperseg // 2. Defaults to None.
    filtlen : float, Hz, optional
        (For medfilt method) Length of median filter in Hz.
    Returns
    -------
    freq : ndarray
        Array of sample frequencies.
    Pxx : ndarray
        Power spectral density of x.

    References
    ----------
    Mostly relies on scipy.signal.spectrogram and numpy.fft
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html

    This is just a wrapper for timeseries object's around Voytek lab's neurodsp See:
    https://github.com/voytekresearch/neurodsp
    """
    is_timeseries = True if issubclass(type(x), TimeSeries) else False
    if Fs is None:
        if is_timeseries:
            Fs = int(x.samplerate.data)
    elif method in ('mean', 'median'):
        if nperseg is None:
            if isinstance(window, str) or isinstance(window, tuple):
                nperseg = int(Fs)
            else:
                nperseg = len(window)
        else:
            nperseg = int(nperseg)
        if noverlap is not None:
            noverlap = int(noverlap)
        else:
            freq, _, spg = signal.spectrogram(x, Fs, window, nperseg, noverlap)
            if method is 'mean':
                Pxx = np.mean(spg, axis=(-1))
            else:
                if method is 'median':
                    Pxx = np.median(spg, axis=(-1))
    else:
        if method is 'medfilt':
            FT = np.fft.fft(x)[:int(np.ceil(len(x) / 2.0))]
            freq = np.fft.fftfreq(len(x), 1.0 / Fs)[:int(np.ceil(len(x) / 2.0))]
            filtlen_samp = int(int(filtlen / (freq[1] - freq[0])) / 2 * 2 + 1)
            Pxx = signal.medfilt(np.abs(FT) ** 2.0 / (Fs * len(x)), filtlen_samp)
        else:
            raise ValueError('Unknown PSD method: %s' % method)
    if is_timeseries:
        shell = x.sel(time=(x['time'].data[:1]))
        coords = {k:v for k, v in list(shell.coords.items())}
        coords['frequency'] = freq
        dims = shell.dims + ('frequency', )
        data = np.expand_dims(Pxx, axis=(get_axis_index(shell, 'time')))
        powers_ts = TimeSeriesLF(data=data, dims=dims, coords=coords)
        return powers_ts
    return (freq, Pxx)