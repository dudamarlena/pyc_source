# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\chirp\split\intervalsplit.py
# Compiled at: 2013-12-11 23:17:46
__doc__ = '\nbasic interval-based splitting functionality.\n\nCopyright (C) 2012 Dan Meliza <dmeliza@gmail.com>\nCreated 2012-04-23\n'

def ramp_signal(s, Fs, ramp):
    """
    Apply a squared cosine ramp to a signal. Modifies the signal in place.

    s:    signal (1D, any type)
    Fs:   sampling rate (in units^-1)
    ramp: duration of ramp (in units)
    """
    from numpy import linspace, pi, sin, cos
    n = ramp * Fs
    t = linspace(0, pi / 2, n)
    s[:n] *= sin(t) ** 2
    s[-n:] *= cos(t) ** 2


def split(signal, element, Fs, **kwargs):
    """
    Extract <element> from <signal> based on start and stop time.

    Fs: sampling rate, in kHz
    ramp: if >0, extract <ramp> ms on either side of the interval,
          with a cosine-squared ramp function applied to eliminate
          transients.

    Returns a 1D time series at the same sampling rate as the
    input signal.
    """
    from chirp.common.geom import elementlist
    time_ramp = kwargs.get('time_ramp', 0)
    if elementlist.element_type(element) == 'interval':
        start, stop = element[:2]
    else:
        start, miny, stop, maxy = element.bounds
    start = max((start - time_ramp) * Fs, 0)
    stop = min((stop + time_ramp) * Fs, signal.size)
    S = signal[start:stop].copy()
    if time_ramp > 0:
        ramp_signal(S, Fs, time_ramp)
    return S