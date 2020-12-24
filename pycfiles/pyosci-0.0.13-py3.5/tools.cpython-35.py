# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyosci/tools.py
# Compiled at: 2016-12-13 08:31:16
# Size of source mod 2**32: 1269 bytes
"""
Convenient operations

"""
import numpy as np, scipy.integrate as integrate
from scipy.constants import elementary_charge as ECHARGE
from copy import deepcopy as copy
IMPEDANCE = 50

def average_wf(waveforms):
    """
    Get the average waveform

    Args:
        waveforms (list):

    Returns:
        np.ndarray
    """
    wf0 = copy(waveforms[0])
    for wf in waveforms[1:]:
        wf0 += wf

    return wf0 / float(len(waveforms))


def integrate_wf(header, waveform, method=integrate.simps, impedance=IMPEDANCE):
    """
    Integrate a waveform to get the total charge

    Args:
        header (dict):
        waveform (np.ndarray):

    Returns:
        float
    """
    integral = method(waveform, header['xs'], header['xincr'])
    return integral / impedance


def save_waveform(header, waveform, filename):
    """
    save a waveform together with its header

    Args:
        header (dict):
        waveform (np.ndarray):
        filename (str):
    Returns:
        None
    """
    np.save(filename, (header, waveform))


def load_waveform(filename):
    """
    load a waveform from a file

    Args:
        filenaame (str): 

    Returns:
        dict
    """
    head, wf = np.load(filename)
    return (head, wf)