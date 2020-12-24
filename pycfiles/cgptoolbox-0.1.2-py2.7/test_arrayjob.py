# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\test\test_arrayjob.py
# Compiled at: 2013-01-14 06:47:43
"""Usage demo of utils.arrayjob. Submit with: python -m utils.test_arrayjob."""
from cgp.utils.arrayjob import *
set_NID(16)
import numpy as np
infile = 'input.npy'
outfile = 'output.npy'
n = 43

@qopt('-l walltime=00:01:00')
def setup():
    """Initialize data."""
    np.save(infile, np.arange(n))


def work():
    """Process chunk ID of workpieces."""
    x = memmap_chunk(infile)
    x += 1


def wrapup():
    """Summarize results."""
    np.save(outfile, sum(np.load(infile)))


if __name__ == '__main__':
    arun(setup, par(work), wrapup, loglevel='DEBUG')

def report():
    """Report results, perhaps while they are being computed."""
    print np.load(outfile)