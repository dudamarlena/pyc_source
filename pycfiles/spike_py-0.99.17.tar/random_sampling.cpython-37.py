# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/Algo/random_sampling.py
# Compiled at: 2020-01-31 06:35:54
# Size of source mod 2**32: 12674 bytes
r"""
random_sampling.py

Created by Marc-Andre on 2013-03-21.
modified 1 july 2014 for interactive mode.
modified february 2017 for python3 compat.

Copyright (c) 2013 IGBMC. All rights reserved.

Generates random sampling for NUS FT spectroscopy

can be used
    as a standalone by answering to the prompted questions
    as a library by importing the code
    the program displays the results - closing the display will generate the files

The program generates two files.
one with the delay values, typically used for the acquisition process,
and one with index values, typically used for the analysis.

Parameters that define the sampling are :

the size of the complete sampling
SIZE = 20000

the sampling ratio  - 0.3 means sampling 30% of the entries
RATIO = 0.2

thus with SIZE = 1000, RATIO = 0.3    300 values out of 1000  will be generated

the dwell time (Nyquist frequency) - used for the delay list
DWELL = 0.0033

the sampling protocole defines how the random points are chosen.
three different protocoles are available : random / poisson / uniform  (sampling P out of N)
PROTOCOLE = "poisson"
    points are sampled so that the gaps between sample points follow a poisson law of $\mu$ = P/N
PROTOCOLE = "uniform"
    points are sampled so that the gaps between sample points follow a uniform law
    so all gaps from 1 to N/P are equiprobable
PROTOCOLE = "random"
    there points are simply sampled at random, using a uniform sampline of P out on N
    the gap distribution follows an exponential law

HEAD determines a number of points that will be kept linearly sampled in the beginning of the sampling
usefull for allowing regular analysis of the data
HEAD = 100

Additional parameters :
The seed of the random generator.
This allows the program to be run several time with reproducible results
The same seed will generate the same values.
Changing the seed will change the values no SEED will generate a new distribution, any integer number will do.
None draws a new distribution each time.
SEED = 1234

file basename of the stored files
FNAME = "Sampling_file"
    generates two files : 
    - the delay list used by the spectrometer - named 'filename'.delay
    - the sampling function used for analysis - named 'filename'.list

if PLOT is True, then the program displays the results - closing the display will generate the files
PLOT = True

Use in a program as follows :

import random_sampling as rs
rs.SIZE = 10000
rs.DWELL = 0.005
rs.RATIO = 0.12
rs.FNAME = "My_file"        # generate 2 files : My_file   and   My_file.list
rs.PROTOCOLE = "poisson"

#then either
rs.main()                       # creates both files - default is no display

#or
sampling =  poisson_gap(SIZE, ratio=RATIO)
...
"""
from __future__ import print_function, division
import numpy as np
from scipy.stats import poisson
import time, unittest, sys
import matplotlib.pyplot as plt
SEED = None
SIZE = 20000
DWELL = 0.0033
RATIO = 0.2
PROTOCOLE = 'poisson'
FNAME = 'Sampling_file'
PLOT = False
HEAD = 0

def random_gap(size, ratio=0.5):
    """
    for a sampling function of 'size' long
    generate a random sampling with sampling 'ratio'
    the first 'head' values are kept linearly sampled
    """
    global HEAD
    ssize = int(size * ratio)
    head = min(HEAD, ssize - 1)
    perm = np.random.permutation(size - head) + head
    samp = np.zeros(ssize, dtype=int)
    samp[head:ssize] = perm[:ssize - head]
    samp[0:head] = list(range(head))
    samp.sort()
    samp[ssize - 1] = size - 1
    return samp


def poisson_gap(size, ratio=0.5):
    """
    for a sampling function of 'size' long
    generate a random sampling with sampling 'ratio' with poisson distribution of gap
    the first 'head' values are kept linearly sampled
    """
    ssize = int(size * ratio)
    head = min(HEAD, ssize - 1)
    mu0 = (size - head) / (size * ratio - head)
    mu = mu0
    samp = list(range(head))
    rv = poisson(mu)
    n = head
    while 1:
        if len(samp) == ssize:
            break
        samp.append(n)
        prev = n
        while prev == n:
            n += rv.rvs()

    samp = correct(samp, size)
    return np.array(samp)


def uniform_gap(size, ratio=0.5):
    """
    for a sampling function of 'size' long
    generate a random sampling with sampling 'ratio' with uniform distribution of gap
    the first 'head' values are kept linearly sampled
    """
    ssize = int(size * ratio)
    head = min(HEAD, ssize - 1)
    mu0 = 2 * (size - head) / (size * ratio - head)
    mu = mu0
    samp = list(range(head))
    n = head
    while 1:
        if len(samp) == ssize:
            break
        samp.append(n)
        prev = n
        while prev == n:
            n += int(mu * np.random.rand())

    samp = correct(samp, size)
    return np.array(samp)


def correct_size(sampling, targetsize):
    """this removes trailing entries in sampling until its size is equal to targetsize"""
    while len(sampling) > targetsize:
        sampling.pop(-1)

    return sampling


def correct(sampling, targetsize):
    """this corrects entries in sampling so that entries go from 0 to targetsize-1, and removes duplicates"""
    ratio = float(max(sampling)) / targetsize
    newsamp = []
    for i, s in enumerate(sampling):
        val = min(int(round(s / ratio)), targetsize - 1)
        while val in newsamp:
            print(val)
            val = val - 1
            if val < 0:
                raise Exception('run failed, please rerun')

        newsamp.append(val)

    return newsamp


def write(filename, sampling, dwell, size, ratio, proto):
    """ given sampling and dwell
    generates two files : 
        - the delay list used by the spectrometer - named 'filename'.delay
        - the sampling function used for analysis - named 'filename'.list
    """
    global SEED
    F = open(filename + '.delay', 'w')
    G = open(filename + '.list', 'w')
    for FG in (F, G):
        FG.write('#File generated by random_sampling.py\n')
        FG.write('# Date : %s\n' % time.ctime())
        FG.write('#\n')
        FG.write('# Initial size  : %d\n' % size)
        FG.write('# sampled size  : %d\n' % len(sampling))
        FG.write('# sampling ratio: %f\n' % ratio)
        FG.write('# Protocole     : %s\n' % proto)
        FG.write('# Dwell time    : %f\n' % dwell)
        FG.write('# linear zone   : %d\n' % min(HEAD, len(sampling) - 1))
        FG.write('# seed          : %s\n' % SEED)
        FG.write('#\n')

    for i in sampling:
        F.write('%f\n' % (dwell * i))
        G.write('%d\n' % i)

    F.close()
    G.close()


def realize(size, sampling):
    """returns a buffer filled with 1.0 and 0.0 realizing the sampling"""
    disp = np.zeros(size)
    disp[sampling] = 1.0
    return disp


def plotit2(size, sampling):
    """plots the result along with the PSF and the gap histogram """
    import numpy.fft as fft
    plt.subplot(221)
    gaps = sampling[1:] - sampling[:-1]
    plt.hist(gaps, bins=(np.arange(max(gaps))))
    plt.title('gap distribution')
    plt.subplot(223)
    disp = realize(size, sampling)
    psf = fft.fftshift(fft.fft(disp))
    apsf = abs(psf)
    plt.plot(apsf)
    sig = apsf.max()
    noise = psf[:len(psf) // 3].std()
    snr = 20 * np.log10(sig / noise)
    plt.text(1, 0.9 * sig, 'SNR : %.2f dB' % snr)
    plt.title('Point Spread Function of the sampling')
    plt.subplot(224)
    plt.plot(sampling)
    plt.title('cumulative')
    plt.subplot(222)
    plotit(size, sampling)


def plotit(size, sampling):
    """plots the result"""
    global PROTOCOLE
    disp = realize(size, sampling)
    plt.plot(disp)
    plt.ylim(ymax=1.1, ymin=(-0.1))
    plt.title('Measure on %d points, %sly sampled at %.2f %%' % (size, PROTOCOLE, 100.0 * len(sampling) / size))


class Tests(unittest.TestCase):

    def test1(self):
        global FNAME
        global HEAD
        global PROTOCOLE
        global RATIO
        global SEED
        global SIZE
        PROTOCOLE = 'poisson'
        SIZE = 20000
        HEAD = 10
        RATIO = 0.25
        SEED = 12345
        FNAME = 'TestFile'
        sampling = main()
        print(sampling.sum(), sampling.std())
        self.assertTrue(sampling.max() == 19999)
        self.assertTrue(sampling.sum() == 49886308)
        self.assertAlmostEqual(sampling.std(), 5780.85909618678)


def main():
    global DWELL
    global PLOT
    global SEED
    if SEED is None:
        SEED = int(100 * time.time()) % 4294967200
    else:
        np.random.seed(SEED)
        if PROTOCOLE == 'random':
            sampling = random_gap(SIZE, ratio=RATIO)
        else:
            if PROTOCOLE == 'poisson':
                sampling = poisson_gap(SIZE, ratio=RATIO)
            else:
                if PROTOCOLE == 'uniform':
                    sampling = uniform_gap(SIZE, ratio=RATIO)
                else:
                    print('UNKNOWN PROTOCOLE')
                    sys.exit(0)
    print('generated {0} {1}ly sampled points out of {2} contiguous points.'.format(len(sampling), PROTOCOLE, SIZE))
    print('from {0} to {1}'.format(sampling[0], sampling[(-1)]))
    if PLOT:
        plotit2(SIZE, sampling)
        plt.show()
    write(FNAME, sampling, DWELL, SIZE, RATIO, PROTOCOLE)
    print('result written to file {0}.list and {0}.delay'.format(FNAME))
    return sampling


def get_val(prompt, defval):
    """a typed version of input(), with default value"""
    if sys.version_info[0] < 3:
        z = raw_input('%s, (%s)  ' % (prompt, defval))
    else:
        z = input('%s, (%s)  ' % (prompt, defval))
    t = type(defval)
    if t == str:
        if z == '':
            z = defval
    else:
        try:
            z = eval(z)
        except SyntaxError:
            z = defval

    print(z)
    return z


def get_from_input():
    """prompt the user and populates the values"""
    global DWELL
    global FNAME
    global HEAD
    global PLOT
    global PROTOCOLE
    global RATIO
    global SEED
    global SIZE
    print('Please Enter values')
    SIZE = get_val('Size of the starting list', SIZE)
    RATIO = get_val('Sampling ratio', RATIO)
    print('This will generate a %d long sampling' % int(SIZE * RATIO))
    DWELL = get_val('dwell time (Nyquist frequency) - used for the delay list', DWELL)
    PROTOCOLE = get_val('sampling protocole defines how the random points are chosen: random/poisson/uniform', PROTOCOLE)
    HEAD = get_val('number of points that will be kept linearly sampled in the beginning of the sampling', HEAD)
    SEED = get_val('seed of the random generator (positive integer - the same seed generates the same list - None is a new list each time)', SEED)
    FNAME = get_val('file basename of the stored files', FNAME)
    PLOT = True
    PLOT = get_val('displays the results - closing the display will generate the files: True/False', PLOT)


def parse_arg(argv=None):
    """read arg line and act"""
    if not argv:
        argv = sys.argv
    elif len(argv) == 1:
        print('try running "%s help" for documentation' % argv[0])
        param = get_from_input()
        main()
    else:
        if argv[1] in ('help', 'HELP', '?'):
            print(__doc__)
            sys.exit(0)
        else:
            print('unknown argument, try "%s help"' % argv[0])


if __name__ == '__main__':
    parse_arg()
    PLOT = True