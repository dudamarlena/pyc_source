# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/netana/plotutil.py
# Compiled at: 2014-10-05 14:59:21
# Size of source mod 2**32: 2906 bytes
import os, sys, time
from matplotlib import pyplot as plt
import numpy as np

def matplot(fn='', units='Hz', ylab=None):
    if ylab != None:
        matplotdc(fn, ylab)
    else:
        matplotac(fn, units)


def matplotdc(fn='', ylab='None'):
    """ This module formats the commands Matplotlib
        to plot the DC network valuse of a circuit. The only
        parameters required are the filename and the Y axis label.
        """
    if ylab == 'Volts':
        xlab = 'Node Number'
    else:
        xlab = 'Mash Number'
    mag = np.genfromtxt(fn, usecols=2, skip_footer=1)
    bfn = os.path.basename(fn)
    name = bfn[:bfn.find('.')] + '\n'
    plt.title(name)
    plt.ylabel(ylab)
    plt.xlabel(xlab)
    plt.grid(True)
    labs = range(1, len(mag) + 1)
    plt.plot(labs, mag, 'r-o')
    ts = time.ctime()
    plt.figtext(0.02, 0.015, ts, fontsize=7, ha='left')
    plt.show()


def matplotac(fn='', units='Hz'):
    """
        This module formats the commands required by Matplotlib
        to plot the network analysis response/tansfer fuction
        of an AC network where the output report contains three cols of
        data in the following order: frequency, magnitude (dB),
        and phase angle (degrees).

        This function "matplotac" is called with file name of the data file
        to be plotted and the frequency units string such as Hz, Kz, Mz).
        The units argument defaults to 'Hz'.

        call as follows:  plotutil.matplotac(fn, units='Hz')
        """
    data = np.genfromtxt(fn, usecols=(0, 1, 2), skip_footer=1)
    freq, mag, pa = data[:, 0], data[:, 1], data[:, 2]
    plt.figure(1)
    plt.subplot(211)
    bfn = os.path.basename(fn)
    name = bfn[:bfn.find('.')] + '\n'
    plt.title(name)
    plt.ylabel('Gain (db)')
    plt.grid(True)
    plt.plot(freq, mag)
    plt.subplot(212)
    plt.ylabel('Phase Angle (Deg.)')
    plt.xlabel('Frequency (' + units[0] + units[1].lower() + ')')
    plt.grid(True)
    plt.plot(freq, pa)
    ts = time.ctime()
    plt.figtext(0.02, 0.015, ts, fontsize=7, ha='left')
    plt.show()


if __name__ == '__main__':
    os.chdir('/home/jim/test')
    matplot('Wein_Bridge.report', 'Hz')
    matplot(fn='LadderNode10.report', ylab='Volts')
    matplot(fn='LadderMash9.report', ylab='Amps')