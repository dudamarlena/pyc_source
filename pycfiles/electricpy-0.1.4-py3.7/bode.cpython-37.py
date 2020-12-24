# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\electricpy\bode.py
# Compiled at: 2019-10-11 18:12:36
# Size of source mod 2**32: 13096 bytes
"""
--------------------
`electricpy.bode.py`
--------------------

Included Functions
------------------
- Transfer Function Bode Plot Generator     bode
- S-Domain Bode Plot Generator              sbode
- Z-Domain Bode Plot Generator              zbode
"""
import matplotlib.pyplot as _plt
import numpy as _np
import scipy.signal as _sig
from numpy import pi as _pi
from cmath import exp as _exp

def _sys_condition(system, feedback):
    if len(system) == 2:
        num = system[0]
        den = system[1]
        if str(type(num)) == tuple:
            num = convolve(num)
        if str(type(den)) == tuple:
            den = convolve(den)
        if feedback:
            ld = len(den)
            ln = len(num)
            if ld > ln:
                num = _np.append(_np.zeros(ld - ln), num)
            if ld < ln:
                den = _np.append(_np.zeros(ln - ld), den)
            den = den + num
        for i in range(len(num)):
            if num[i] != 0:
                num = num[i:]
                break

        for i in range(len(den)):
            if den[i] != 0:
                den = den[i:]
                break

        system = (
         num, den)
    return system


def bode(system, mn=0.001, mx=1000, npts=100, title='', xlim=False, ylim=False, sv=False, disp3db=False, lowcut=None, magnitude=True, angle=True, freqaxis='rad'):
    """
    System Bode Plotting Function
    
    A simple function to generate the Bode Plot for magnitude
    and frequency given a transfer function system.
    
    Parameters
    ----------
    system:         transfer function object
                    The Transfer Function; can be provided as the following:
                    - 1 (instance of lti)
                    - 2 (num, den)
                    - 3 (zeros, poles, gain)
                    - 4 (A, B, C, D)
    mn:             float, optional
                    The minimum frequency to be calculated for. default=0.01.
    mx:             float, optional
                    The maximum frequency to be calculated for. default=1000.
    npts:           float, optional
                    The number of points over which to calculate the system.
                    default=100.
    title:          string, optional
                    Additional string to be added to plot titles;
                    default="".
    xlim:           list of float, optional
                    Limit in x-axis for graph plot. Accepts tuple of: (xmin, xmax).
                    Default is False.
    ylim:           list of float, optional
                    Limit in y-axis for graph plot. Accepts tuple of: (ymin, ymax).
                    Default is False.
    sv:             bool, optional
                    Save the plots as PNG files. Default is False.
    disp3db:        bool, optional
                    Control argument to enable the display of the 3dB line,
                    default=False.
    lowcut:         float, optional
                    An additional marking line that can be plotted, default=None
    magnitude:      bool, optional
                    Control argument to enable plotting of magnitude, default=True
    angle:          bool, optional
                    Control argument to enable plotting of angle, default=True
    freqaxis:       string, optional
                    Control argument to specify the freqency axis in degrees or
                    radians, default is radians (rad)
    """
    system = _sys_condition(system, False)
    degrees = False
    if freqaxis.lower().find('deg') != -1:
        degrees = True
        mn = 2 * _np.pi * mn
        mx = 2 * _np.pi * mx
    mn = _np.log10(mn)
    mx = _np.log10(mx)
    wover = _np.logspace(mn, mx, npts)
    w, mag, ang = _sig.bode(system, wover)
    if magnitude:
        magTitle = 'Magnitude ' + title
        _plt.title(magTitle)
        if degrees:
            _plt.plot(w / (2 * _np.pi), mag)
            _plt.xlabel('Frequency (Hz)')
        else:
            _plt.plot(w, mag)
            _plt.xlabel('Frequency (rad/sec)')
        _plt.xscale('log')
        _plt.grid(which='both')
        _plt.ylabel('Magnitude (dB)')
        if disp3db:
            _plt.axhline(-3)
        if lowcut != None:
            _plt.axhline(lowcut)
        if xlim != False:
            _plt.xlim(xlim)
        if ylim != False:
            _plt.ylim(ylim)
        if sv:
            _plt.savefig(magTitle + '.png')
        _plt.show()
    if angle:
        angTitle = 'Angle ' + title
        _plt.title(angTitle)
        if degrees:
            _plt.plot(w / (2 * _np.pi), ang)
            _plt.xlabel('Frequency (Hz)')
        else:
            _plt.plot(w, ang)
            _plt.xlabel('Frequency (rad/sec)')
        _plt.xscale('log')
        _plt.grid(which='both')
        _plt.ylabel('Angle (degrees)')
        if xlim != False:
            _plt.xlim(xlim)
        if ylim != False:
            _plt.ylim(ylim)
        if sv:
            _plt.savefig(angTitle + '.png')
        _plt.show()


def sbode(f, NN=1000, title='', xlim=False, ylim=False, mn=0, mx=1000, disp3db=False, lowcut=None, magnitude=True, angle=True):
    """
    S-Domain Bode Plotting Function
    
    Parameters
    ----------
    f:              function
                    The Input Function, must be callable function object.
    NN:             int, optional
                    The Interval over which to be generated, default=1000
    title:          string, optional
                    Additional string to be added to plot titles;
                    default="".
    xlim:           list of float, optional
                    Limit in x-axis for graph plot. Accepts tuple of: (xmin, xmax).
                    Default is False.
    ylim:           list of float, optional
                    Limit in y-axis for graph plot. Accepts tuple of: (ymin, ymax).
                    Default is False.
    mn:             float, optional
                    The minimum W value to be generated, default=0
    mx:             float, optional
                    The maximum W value to be generated, default=1000
    sv:             bool, optional
                    Save the plots as PNG files. Default is False.
    disp3db:        bool, optional
                    Control argument to enable the display of the 3dB line,
                    default=False.
    lowcut:         float, optional
                    An additional marking line that can be plotted, default=None
    magnitude:      bool, optional
                    Control argument to enable plotting of magnitude, default=True
    angle:          bool, optional
                    Control argument to enable plotting of angle, default=True
    """
    W = _np.linspace(mn, mx, NN)
    H = _np.zeros(NN, dtype=(_np.complex))
    for n in range(0, NN):
        s = complex(0.0, 1.0) * W[n]
        H[n] = f(s)

    if magnitude:
        _plt.semilogx(W, 20 * _np.log10(abs(H)), 'k')
        _plt.ylabel('|H| dB')
        _plt.xlabel('Frequency (rad/sec)')
        _plt.title(title + ' Magnitude')
        _plt.grid(which='both')
        if disp3db:
            _plt.axhline(-3)
        if lowcut != None:
            _plt.axhline(lowcut)
        if xlim != False:
            _plt.xlim(xlim)
        if ylim != False:
            _plt.ylim(ylim)
        if sv:
            _plt.savefig(title + ' Magnitude.png')
        _plt.show()
    aaa = _np.angle(H)
    for n in range(NN):
        if aaa[n] > _pi:
            aaa[n] = aaa[n] - 2 * _pi

    if angle:
        _plt.title(title + ' Phase')
        _plt.semilogx(W, 180 / _pi * aaa, 'k')
        _plt.ylabel('H phase (degrees)')
        _plt.xlabel('Frequency (rad/sec)')
        _plt.grid(which='both')
        if xlim != False:
            _plt.xlim(xlim)
        if ylim != False:
            _plt.ylim(ylim)
        if sv:
            _plt.savefig(title + ' Phase.png')
        _plt.show()


def zbode(f, dt=0.01, NN=1000, title='', mn=0, mx=2 * _pi, xlim=False, ylim=False, approx=False, disp3db=False, lowcut=None, magnitude=True, angle=True):
    """
    Z-Domain Bode Plotting Function
    
    Parameters
    ----------
    f:              function
                    The Input Function, must be callable function object.
                    Must be specified as transfer function of type:
                    - S-Domain (when approx=False, default)
                    - Z-Domain (when approx=True)
    dt:             float, optional
                    The time-step used, default=0.01
    NN:             int, optional
                    The Interval over which to be generated, default=1000
    mn:             float, optional
                    The minimum phi value to be generated, default=0
    mx:             float, optional
                    The maximum phi value to be generated, default=2*pi
    approx:         bool, optional
                    Control argument to specify whether input funciton
                    should be treated as Z-Domain function or approximated
                    Z-Domain function. default=False
    title:          string, optional
                    Additional string to be added to plot titles;
                    default="".
    xlim:           list of float, optional
                    Limit in x-axis for graph plot. Accepts tuple of: (xmin, xmax).
                    Default is False.
    ylim:           list of float, optional
                    Limit in y-axis for graph plot. Accepts tuple of: (ymin, ymax).
                    Default is False.
    sv:             bool, optional
                    Save the plots as PNG files. Default is False.
    disp3db:        bool, optional
                    Control argument to enable the display of the 3dB line,
                    default=False.
    lowcut:         float, optional
                    An additional marking line that can be plotted, default=None
    magnitude:      bool, optional
                    Control argument to enable plotting of magnitude, default=True
    angle:          bool, optional
                    Control argument to enable plotting of angle, default=True
    """
    phi = _np.linspace(mn, mx, NN)
    H = _np.zeros(NN, dtype=(_np.complex))
    for n in range(0, NN):
        z = _exp(complex(0.0, 1.0) * phi[n])
        if approx != False:
            s = approx(z, dt)
            H[n] = f(s)
        else:
            H[n] = dt * f(z)

    if magnitude:
        _plt.semilogx(180 / _pi * phi, 20 * _np.log10(abs(H)), 'k')
        _plt.ylabel('|H| dB')
        _plt.xlabel('Frequency (degrees)')
        _plt.title(title + ' Magnitude')
        _plt.grid(which='both')
        if disp3db:
            _plt.axhline(-3)
        if lowcut != None:
            _plt.axhline(lowcut)
        if xlim != False:
            _plt.xlim(xlim)
        if ylim != False:
            _plt.ylim(ylim)
        if sv:
            _plt.savefig(title + ' Magnitude.png')
        _plt.show()
    aaa = _np.angle(H)
    for n in range(NN):
        if aaa[n] > _pi:
            aaa[n] = aaa[n] - 2 * _pi

    if angle:
        _plt.semilogx(180 / _pi * phi, 180 / _pi * aaa, 'k')
        _plt.ylabel('H (degrees)')
        _plt.grid(which='both')
        _plt.xlabel('Frequency (degrees)')
        _plt.title(title + ' Phase')
        if xlim != False:
            _plt.xlim(xlim)
        if ylim != False:
            _plt.ylim(ylim)
        if sv:
            _plt.savefig(title + ' Phase.png')
        _plt.show()