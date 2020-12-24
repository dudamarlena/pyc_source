# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bayesflare/misc/misc.py
# Compiled at: 2017-04-26 11:11:14
import sys, os, errno

def nextpow2(i):
    """
    Calculates the nearest power of two to the inputed number.

    Parameters
    ----------
    i : int
       An integer.

    Output
    ------
    n : int
       The power of two closest to `i`.
    """
    n = 1
    while n < i:
        n *= 2

    return n


def mkdir(path):
    """
    Recursively makes a folder.

    Parameters
    ----------
    path : str
       A string describing the path where the folder should be created.
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise