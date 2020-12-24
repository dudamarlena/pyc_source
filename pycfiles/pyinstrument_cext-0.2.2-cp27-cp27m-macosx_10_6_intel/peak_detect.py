# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\curve\peak_detect.py
# Compiled at: 2013-10-26 10:06:03
import numpy as np
from math import pi, log
import pylab
from scipy import fft, ifft
from scipy.optimize import curve_fit
i = 10000
x = np.linspace(0, 3.5 * pi, i)
y = 0.3 * np.sin(x) + np.sin(1.3 * x) + 0.9 * np.sin(4.2 * x) + 0.06 * np.random.randn(i)

def _datacheck_peakdetect(x_axis, y_axis):
    if x_axis is None:
        x_axis = range(len(y_axis))
    if len(y_axis) != len(x_axis):
        raise (
         ValueError,
         'Input vectors y_axis and x_axis must have same length')
    y_axis = np.array(y_axis)
    x_axis = np.array(x_axis)
    return (
     x_axis, y_axis)


def _peakdetect_parabole_fitter(raw_peaks, x_axis, y_axis, points):
    """
    Performs the actual parabole fitting for the peakdetect_parabole function.
    
    keyword arguments:
    raw_peaks -- A list of either the maximium or the minimum peaks, as given
        by the peakdetect_zero_crossing function, with index used as x-axis
    x_axis -- A numpy list of all the x values
    y_axis -- A numpy list of all the y values
    points -- How many points around the peak should be used during curve
        fitting, must be odd.
    
    return -- A list giving all the peaks and the fitted waveform, format:
        [[x, y, [fitted_x, fitted_y]]]
        
    """
    func = lambda x, k, tau, m: k * (x - tau) ** 2 + m
    fitted_peaks = []
    for peak in raw_peaks:
        index = peak[0]
        x_data = x_axis[index - points // 2:index + points // 2 + 1]
        y_data = y_axis[index - points // 2:index + points // 2 + 1]
        tau = x_axis[index]
        m = peak[1]
        p0 = (
         -m, tau, m)
        popt, pcov = curve_fit(func, x_data, y_data, p0)
        x, y = popt[1:3]
        x2 = np.linspace(x_data[0], x_data[(-1)], points * 10)
        y2 = func(x2, *popt)
        fitted_peaks.append([x, y, [x2, y2]])

    return fitted_peaks


def peakdetect(y_axis, x_axis=None, lookahead=300, delta=0):
    """
    Converted from/based on a MATLAB script at: 
    http://billauer.co.il/peakdet.html
    
    function for detecting local maximas and minmias in a signal.
    Discovers peaks by searching for values which are surrounded by lower
    or larger values for maximas and minimas respectively
    
    keyword arguments:
    y_axis -- A list containg the signal over which to find peaks
    x_axis -- (optional) A x-axis whose values correspond to the y_axis list
        and is used in the return to specify the postion of the peaks. If
        omitted an index of the y_axis is used. (default: None)
    lookahead -- (optional) distance to look ahead from a peak candidate to
        determine if it is the actual peak (default: 200) 
        '(sample / period) / f' where '4 >= f >= 1.25' might be a good value
    delta -- (optional) this specifies a minimum difference between a peak and
        the following points, before a peak may be considered a peak. Useful
        to hinder the function from picking up false peaks towards to end of
        the signal. To work well delta should be set to delta >= RMSnoise * 5.
        (default: 0)
            delta function causes a 20% decrease in speed, when omitted
            Correctly used it can double the speed of the function
    
    return -- two lists [max_peaks, min_peaks] containing the positive and
        negative peaks respectively. Each cell of the lists contains a tupple
        of: (position, peak_value) 
        to get the average peak value do: np.mean(max_peaks, 0)[1] on the
        results to unpack one of the lists into x, y coordinates do: 
        x, y = zip(*tab)
    """
    max_peaks = []
    min_peaks = []
    dump = []
    x_axis, y_axis = _datacheck_peakdetect(x_axis, y_axis)
    length = len(y_axis)
    if lookahead < 1:
        raise ValueError, "Lookahead must be '1' or above in value"
    if not (np.isscalar(delta) and delta >= 0):
        raise ValueError, 'delta must be a positive number'
    mn, mx = np.Inf, -np.Inf
    for index, (x, y) in enumerate(zip(x_axis[:-lookahead], y_axis[:-lookahead])):
        if y > mx:
            mx = y
            mxpos = x
        if y < mn:
            mn = y
            mnpos = x
        if y < mx - delta and mx != np.Inf:
            if y_axis[index:index + lookahead].max() < mx:
                max_peaks.append([mxpos, mx])
                dump.append(True)
                mx = np.Inf
                mn = np.Inf
                if index + lookahead >= length:
                    break
                continue
        if y > mn + delta and mn != -np.Inf:
            if y_axis[index:index + lookahead].min() > mn:
                min_peaks.append([mnpos, mn])
                dump.append(False)
                mn = -np.Inf
                mx = -np.Inf
                if index + lookahead >= length:
                    break

    try:
        if dump[0]:
            max_peaks.pop(0)
        else:
            min_peaks.pop(0)
        del dump
    except IndexError:
        pass

    return [
     max_peaks, min_peaks]


def peakdetect_fft(y_axis, x_axis, pad_len=5):
    """
    Performs a FFT calculation on the data and zero-pads the results to
    increase the time domain resolution after performing the inverse fft and
    send the data to the 'peakdetect' function for peak 
    detection.
    
    Omitting the x_axis is forbidden as it would make the resulting x_axis
    value silly if it was returned as the index 50.234 or similar.
    
    Will find at least 1 less peak then the 'peakdetect_zero_crossing'
    function, but should result in a more precise value of the peak as
    resolution has been increased. Some peaks are lost in an attempt to
    minimize spectral leakage by calculating the fft between two zero
    crossings for n amount of signal periods.
    
    The biggest time eater in this function is the ifft and thereafter it's
    the 'peakdetect' function which takes only half the time of the ifft.
    Speed improvementd could include to check if 2**n points could be used for
    fft and ifft or change the 'peakdetect' to the 'peakdetect_zero_crossing',
    which is maybe 10 times faster than 'peakdetct'. The pro of 'peakdetect'
    is that it resutls in one less lost peak. It should also be noted that the
    time used by the ifft function can change greatly depending on the input.
    
    keyword arguments:
    y_axis -- A list containg the signal over which to find peaks
    x_axis -- A x-axis whose values correspond to the y_axis list and is used
        in the return to specify the postion of the peaks.
    pad_len -- (optional) By how many times the time resolution should be
        increased by, e.g. 1 doubles the resolution. The amount is rounded up
        to the nearest 2 ** n amount (default: 5)
    
    return -- two lists [max_peaks, min_peaks] containing the positive and
        negative peaks respectively. Each cell of the lists contains a tupple
        of: (position, peak_value) 
        to get the average peak value do: np.mean(max_peaks, 0)[1] on the
        results to unpack one of the lists into x, y coordinates do: 
        x, y = zip(*tab)
    """
    x_axis, y_axis = _datacheck_peakdetect(x_axis, y_axis)
    zero_indices = zero_crossings(y_axis, window=11)
    last_indice = -1 - (1 - len(zero_indices) & 1)
    fft_data = fft(y_axis[zero_indices[0]:zero_indices[last_indice]])
    padd = lambda x, c: x[:len(x) // 2] + [0] * c + x[len(x) // 2:]
    n = lambda x: int(log(x) / log(2)) + 1
    fft_padded = padd(list(fft_data), 2 ** n(len(fft_data) * pad_len) - len(fft_data))
    sf = len(fft_padded) / float(len(fft_data))
    y_axis_ifft = ifft(fft_padded).real * sf
    x_axis_ifft = np.linspace(x_axis[zero_indices[0]], x_axis[zero_indices[last_indice]], len(y_axis_ifft))
    max_peaks, min_peaks = peakdetect(y_axis_ifft, x_axis_ifft, 500, delta=abs(np.diff(y_axis).max() * 2))
    data_len = int(np.diff(zero_indices).mean()) / 10
    data_len += 1 - data_len & 1
    fitted_wave = []
    for peaks in [max_peaks, min_peaks]:
        peak_fit_tmp = []
        index = 0
        for peak in peaks:
            index = np.where(x_axis_ifft[index:] == peak[0])[0][0] + index
            x_fit_lim = x_axis_ifft[index - data_len // 2:index + data_len // 2 + 1]
            y_fit_lim = y_axis_ifft[index - data_len // 2:index + data_len // 2 + 1]
            peak_fit_tmp.append([x_fit_lim, y_fit_lim])

        fitted_wave.append(peak_fit_tmp)

    pylab.plot(x_axis, y_axis)
    pylab.hold(True)
    pylab.plot(x_axis_ifft, y_axis_ifft)
    pylab.show()
    return [
     max_peaks, min_peaks]


def peakdetect_parabole(y_axis, x_axis, points=9):
    """
    Function for detecting local maximas and minmias in a signal.
    Discovers peaks by fitting the model function: y = k (x - tau) ** 2 + m
    to the peaks. The amount of points used in the fitting is set by the
    points argument.
    
    Omitting the x_axis is forbidden as it would make the resulting x_axis
    value silly if it was returned as index 50.234 or similar.
    
    will find the same amount of peaks as the 'peakdetect_zero_crossing'
    function, but might result in a more precise value of the peak.
    
    keyword arguments:
    y_axis -- A list containg the signal over which to find peaks
    x_axis -- A x-axis whose values correspond to the y_axis list and is used
        in the return to specify the postion of the peaks.
    points -- (optional) How many points around the peak should be used during
        curve fitting, must be odd (default: 9)
    
    return -- two lists [max_peaks, min_peaks] containing the positive and
        negative peaks respectively. Each cell of the lists contains a list
        of: (position, peak_value) 
        to get the average peak value do: np.mean(max_peaks, 0)[1] on the
        results to unpack one of the lists into x, y coordinates do: 
        x, y = zip(*max_peaks)
    """
    x_axis, y_axis = _datacheck_peakdetect(x_axis, y_axis)
    points += 1 - points % 2
    max_raw, min_raw = peakdetect_zero_crossing(y_axis)
    max_peaks = []
    min_peaks = []
    max_ = _peakdetect_parabole_fitter(max_raw, x_axis, y_axis, points)
    min_ = _peakdetect_parabole_fitter(min_raw, x_axis, y_axis, points)
    max_peaks = map(lambda x: [x[0], x[1]], max_)
    max_fitted = map(lambda x: x[(-1)], max_)
    min_peaks = map(lambda x: [x[0], x[1]], min_)
    min_fitted = map(lambda x: x[(-1)], min_)
    return [
     max_peaks, min_peaks]


def peakdetect_sine(y_axis, x_axis, points=9, lock_frequency=False):
    """
    Function for detecting local maximas and minmias in a signal.
    Discovers peaks by fitting the model function:
    y = A * sin(2 * pi * f * x - tau) to the peaks. The amount of points used
    in the fitting is set by the points argument.
    
    Omitting the x_axis is forbidden as it would make the resulting x_axis
    value silly if it was returned as index 50.234 or similar.
    
    will find the same amount of peaks as the 'peakdetect_zero_crossing'
    function, but might result in a more precise value of the peak.
    
    The function might have some problems if the sine wave has a
    non-negligible total angle i.e. a k*x component, as this messes with the
    internal offset calculation of the peaks, might be fixed by fitting a 
    k * x + m function to the peaks for offset calculation.
    
    keyword arguments:
    y_axis -- A list containg the signal over which to find peaks
    x_axis -- A x-axis whose values correspond to the y_axis list and is used
        in the return to specify the postion of the peaks.
    points -- (optional) How many points around the peak should be used during
        curve fitting, must be odd (default: 9)
    lock_frequency -- (optional) Specifies if the frequency argument of the
        model function should be locked to the value calculated from the raw
        peaks or if optimization process may tinker with it. (default: False)
    
    return -- two lists [max_peaks, min_peaks] containing the positive and
        negative peaks respectively. Each cell of the lists contains a tupple
        of: (position, peak_value) 
        to get the average peak value do: np.mean(max_peaks, 0)[1] on the
        results to unpack one of the lists into x, y coordinates do: 
        x, y = zip(*tab)
    """
    x_axis, y_axis = _datacheck_peakdetect(x_axis, y_axis)
    points += 1 - points % 2
    max_raw, min_raw = peakdetect_zero_crossing(y_axis)
    max_peaks = []
    min_peaks = []
    offset = np.mean([np.mean(max_raw, 0)[1], np.mean(min_raw, 0)[1]])
    Hz = []
    for raw in [max_raw, min_raw]:
        if len(raw) > 1:
            peak_pos = [ x_axis[index] for index in zip(*raw)[0] ]
            Hz.append(np.mean(np.diff(peak_pos)))

    Hz = 1 / np.mean(Hz)
    if lock_frequency:
        func = lambda x, A, tau: A * np.sin(2 * pi * Hz * (x - tau) + pi / 2)
    else:
        func = lambda x, A, Hz, tau: A * np.sin(2 * pi * Hz * (x - tau) + pi / 2)
    fitted_peaks = []
    for raw_peaks in [max_raw, min_raw]:
        peak_data = []
        for peak in raw_peaks:
            index = peak[0]
            x_data = x_axis[index - points // 2:index + points // 2 + 1]
            y_data = y_axis[index - points // 2:index + points // 2 + 1]
            tau = x_axis[index]
            A = peak[1]
            if lock_frequency:
                p0 = (
                 A, tau)
            else:
                p0 = (
                 A, Hz, tau)
            y_data -= offset
            popt, pcov = curve_fit(func, x_data, y_data, p0)
            x = popt[(-1)]
            y = popt[0]
            x2 = np.linspace(x_data[0], x_data[(-1)], points * 10)
            y2 = func(x2, *popt)
            y += offset
            y2 += offset
            y_data += offset
            peak_data.append([x, y, [x2, y2]])

        fitted_peaks.append(peak_data)

    max_peaks = map(lambda x: [x[0], x[1]], fitted_peaks[0])
    max_fitted = map(lambda x: x[(-1)], fitted_peaks[0])
    min_peaks = map(lambda x: [x[0], x[1]], fitted_peaks[1])
    min_fitted = map(lambda x: x[(-1)], fitted_peaks[1])
    return [
     max_peaks, min_peaks]


def peakdetect_sine_locked(y_axis, x_axis, points=9):
    """
    Convinience function for calling the 'peakdetect_sine' function with
    the lock_frequency argument as True.
    
    keyword arguments:
    y_axis -- A list containg the signal over which to find peaks
    x_axis -- A x-axis whose values correspond to the y_axis list and is used
        in the return to specify the postion of the peaks.
    points -- (optional) How many points around the peak should be used during
        curve fitting, must be odd (default: 9)
        
    return -- see 'peakdetect_sine'
    """
    return peakdetect_sine(y_axis, x_axis, points, True)


def peakdetect_zero_crossing(y_axis, x_axis=None, window=11):
    """
    Function for detecting local maximas and minmias in a signal.
    Discovers peaks by dividing the signal into bins and retrieving the
    maximum and minimum value of each the even and odd bins respectively.
    Division into bins is performed by smoothing the curve and finding the
    zero crossings.
    
    Suitable for repeatable signals, where some noise is tolerated. Excecutes
    faster than 'peakdetect', although this function will break if the offset
    of the signal is too large. It should also be noted that the first and
    last peak will probably not be found, as this function only can find peaks
    between the first and last zero crossing.
    
    keyword arguments:
    y_axis -- A list containg the signal over which to find peaks
    x_axis -- (optional) A x-axis whose values correspond to the y_axis list
        and is used in the return to specify the postion of the peaks. If
        omitted an index of the y_axis is used. (default: None)
    window -- the dimension of the smoothing window; should be an odd integer
        (default: 11)
    
    return -- two lists [max_peaks, min_peaks] containing the positive and
        negative peaks respectively. Each cell of the lists contains a tupple
        of: (position, peak_value) 
        to get the average peak value do: np.mean(max_peaks, 0)[1] on the
        results to unpack one of the lists into x, y coordinates do: 
        x, y = zip(*tab)
    """
    x_axis, y_axis = _datacheck_peakdetect(x_axis, y_axis)
    zero_indices = zero_crossings(y_axis, window=window)
    period_lengths = np.diff(zero_indices)
    bins_y = [ y_axis[index:index + diff] for index, diff in zip(zero_indices, period_lengths)
             ]
    bins_x = [ x_axis[index:index + diff] for index, diff in zip(zero_indices, period_lengths)
             ]
    even_bins_y = bins_y[::2]
    odd_bins_y = bins_y[1::2]
    even_bins_x = bins_x[::2]
    odd_bins_x = bins_x[1::2]
    hi_peaks_x = []
    lo_peaks_x = []
    if abs(even_bins_y[0].max()) > abs(even_bins_y[0].min()):
        hi_peaks = [ bin.max() for bin in even_bins_y ]
        lo_peaks = [ bin.min() for bin in odd_bins_y ]
        for bin_x, bin_y, peak in zip(even_bins_x, even_bins_y, hi_peaks):
            hi_peaks_x.append(bin_x[np.where(bin_y == peak)[0][0]])

        for bin_x, bin_y, peak in zip(odd_bins_x, odd_bins_y, lo_peaks):
            lo_peaks_x.append(bin_x[np.where(bin_y == peak)[0][0]])

    else:
        hi_peaks = [ bin.max() for bin in odd_bins_y ]
        lo_peaks = [ bin.min() for bin in even_bins_y ]
        for bin_x, bin_y, peak in zip(odd_bins_x, odd_bins_y, hi_peaks):
            hi_peaks_x.append(bin_x[np.where(bin_y == peak)[0][0]])

        for bin_x, bin_y, peak in zip(even_bins_x, even_bins_y, lo_peaks):
            lo_peaks_x.append(bin_x[np.where(bin_y == peak)[0][0]])

    max_peaks = [ [x, y] for x, y in zip(hi_peaks_x, hi_peaks) ]
    min_peaks = [ [x, y] for x, y in zip(lo_peaks_x, lo_peaks) ]
    return [
     max_peaks, min_peaks]


def _smooth(x, window_len=11, window='hanning'):
    """
    smooth the data using a window of the requested size.
    
    This method is based on the convolution of a scaled window on the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd 
            integer
        window: the type of window from 'flat', 'hanning', 'hamming', 
            'bartlett', 'blackman'
            flat window will produce a moving average smoothing.
 
    output:
        the smoothed signal
        
    example:
 
    t = linspace(-2,2,0.1)
    x = sin(t)+randn(len(t))*0.1
    y = _smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, 
    numpy.convolve, scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if a list instead of
    a string   
    """
    if x.ndim != 1:
        raise ValueError, 'smooth only accepts 1 dimension arrays.'
    if x.size < window_len:
        raise ValueError, 'Input vector needs to be bigger than window size.'
    if window_len < 3:
        return x
    if window not in ('flat', 'hanning', 'hamming', 'bartlett', 'blackman'):
        raise (
         ValueError,
         ("Window is not one of '{0}', '{1}', '{2}', '{3}', '{4}'").format(*('flat', 'hanning',
                                                                    'hamming', 'bartlett',
                                                                    'blackman')))
    s = np.r_[(x[window_len - 1:0:-1], x, x[-1:-window_len:-1])]
    if window == 'flat':
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')
    y = np.convolve(w / w.sum(), s, mode='valid')
    return y


def zero_crossings(y_axis, window=11):
    """
    Algorithm to find zero crossings. Smoothens the curve and finds the
    zero-crossings by looking for a sign change.
    
    
    keyword arguments:
    y_axis -- A list containg the signal over which to find zero-crossings
    window -- the dimension of the smoothing window; should be an odd integer
        (default: 11)
    
    return -- the index for each zero-crossing
    """
    length = len(y_axis)
    x_axis = np.asarray(range(length), int)
    y_axis = _smooth(y_axis, window)[:length]
    zero_crossings = np.where(np.diff(np.sign(y_axis)))[0]
    indices = [ x_axis[index] for index in zero_crossings ]
    diff = np.diff(indices)
    if diff.std() / diff.mean() > 0.2:
        print diff.std() / diff.mean()
        print np.diff(indices)
        raise (ValueError,
         ('False zero-crossings found, indicates problem {0} or {1}').format('with smoothing window', 'problem with offset'))
    if len(zero_crossings) < 1:
        raise (
         ValueError, 'No zero crossings found')
    return indices


def _test_zero():
    _max, _min = peakdetect_zero_crossing(y, x)


def _test():
    _max, _min = peakdetect(y, x, delta=0.3)


def _test_graph():
    i = 10000
    x = np.linspace(0, 3.7 * pi, i)
    y = 0.3 * np.sin(x) + np.sin(1.3 * x) + 0.9 * np.sin(4.2 * x) + 0.06 * np.random.randn(i)
    y *= -1
    x = range(i)
    _max, _min = peakdetect(y, x, 750, 0.3)
    xm = [ p[0] for p in _max ]
    ym = [ p[1] for p in _max ]
    xn = [ p[0] for p in _min ]
    yn = [ p[1] for p in _min ]
    plot = pylab.plot(x, y)
    pylab.hold(True)
    pylab.plot(xm, ym, 'r+')
    pylab.plot(xn, yn, 'g+')
    _max, _min = peak_det_bad.peakdetect(y, 0.7, x)
    xm = [ p[0] for p in _max ]
    ym = [ p[1] for p in _max ]
    xn = [ p[0] for p in _min ]
    yn = [ p[1] for p in _min ]
    pylab.plot(xm, ym, 'y*')
    pylab.plot(xn, yn, 'k*')
    pylab.show()