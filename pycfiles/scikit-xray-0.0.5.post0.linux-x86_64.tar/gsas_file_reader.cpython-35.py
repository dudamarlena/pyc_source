# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/io/gsas_file_reader.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 8933 bytes
"""
    This is the module for reading files created in GSAS file formats
    https://subversion.xor.aps.anl.gov/trac/pyGSAS
"""
from __future__ import absolute_import, division, print_function
import six, os, numpy as np

def gsas_reader(file):
    """
    Parameters
    ----------
    file: str
        GSAS powder data file

    Returns
    --------
     tth : ndarray
        twotheta values (degrees) shape (N, ) array

    intensity : ndarray
        intensity values shape (N, ) array

    err : ndarray
        error value of intensity shape(N, ) array
    """
    if os.path.splitext(file)[1] != '.gsas':
        raise IOError('Provide a file with diffraction data saved in GSAS, file extension has to be .gsas ')
    with open(file, 'r') as (fi):
        S = fi.readlines()[1]
        mode = S.split()[9]
    try:
        tth, intensity, err = _func_look_up[mode](file)
    except KeyError:
        raise ValueError("Provide a correct mode of the GSAS file, file modes could be in 'STD', 'ESD', 'FXYE' ")

    return (
     tth, intensity, err)


def _get_fxye_data(file):
    """
    Parameters
    ----------
    file: str
        GSAS powder data file

    Return
    ------
    tth : ndarray
        twotheta values (degrees) shape (N, ) array

    intensity : ndarray
        intensity values shape (N, ) array

    err : ndarray
        error value of intensity shape(N, ) array

    """
    tth = []
    intensity = []
    err = []
    with open(file, 'r') as (fi):
        S = fi.readlines()[2:]
        for line in S:
            vals = line.split()
            tth.append(float(vals[0]))
            f = float(vals[1])
            s = float(vals[2])
            if f <= 0.0:
                intensity.append(0.0)
            else:
                intensity.append(float(vals[1]))
            if s > 0.0:
                err.append(1.0 / float(vals[2]) ** 2)
            else:
                err.append(0.0)

    return [
     np.array(tth), np.array(intensity), np.array(err)]


def _get_esd_data(file):
    """
    Parameters
    ----------
    file: str
        GSAS powder data file

    Return
    ------
    tth : ndarray
        twotheta values (degrees) shape (N, ) array

    intensity : ndarray
        intensity values shape (N, ) array

    err : ndarray
        error value of intensity shape(N, ) array

    """
    tth = []
    intensity = []
    err = []
    with open(file, 'r') as (fi):
        S = fi.readlines()[1:]
        start = float(S[0].split()[5]) / 100.0
        step = float(S[0].split()[6]) / 100.0
        j = 0
        for line in S[1:]:
            for i in range(0, 80, 16):
                xi = start + step * j
                yi = _sfloat(line[i:i + 8])
                ei = _sfloat(line[i + 8:i + 16])
                tth.append(xi)
                if yi > 0.0:
                    intensity.append(yi)
                else:
                    intensity.append(0.0)
                if ei > 0.0:
                    err.append(1.0 / ei ** 2)
                else:
                    err.append(0.0)
                j += 1

    N = len(tth)
    return [np.array(tth), np.array(intensity), np.array(err)]


def _get_std_data(file):
    """
    Parameters
    ----------
    file: str
        GSAS powder data file

    Return
    ------
    tth : ndarray
        twotheta values (degrees) shape (N, ) array

    intensity : ndarray
        intensity values shape (N, ) array

    err : ndarray
        error value of intensity shape(N, ) array

    """
    tth = []
    intensity = []
    err = []
    with open(file, 'r') as (fi):
        S = fi.readlines()[1:]
        start = float(S[0].split()[5]) / 100.0
        step = float(S[0].split()[6]) / 100.0
        nch = float(S[0].split()[2])
        j = 0
        for line in S[1:]:
            for i in range(0, 80, 8):
                xi = start + step * j
                ni = max(_sint(line[i:i + 2]), 1)
                yi = max(_sfloat(line[i + 2:i + 8]), 0.0)
                if yi:
                    vi = yi / ni
                else:
                    yi = 0.0
                    vi = 0.0
                if j < nch:
                    tth.append(xi)
                    if vi <= 0.0:
                        intensity.append(0.0)
                        err.append(0.0)
                    else:
                        intensity.append(yi)
                        err.append(1.0 / vi)
                    j += 1

    N = len(tth)
    return [np.array(tth), np.array(intensity), np.array(err)]


_func_look_up = {'STD': _get_std_data, 'ESD': _get_esd_data, 'FXYE': _get_fxye_data}

def _sfloat(S):
    """
    convert a string to a float, treating an all-blank string as zero
    Parameter
    ---------
    S : str
        string that need to be converted as float treating an
        all-blank string as zero

    Returns
    -------
    float or zero
    """
    if S.strip():
        return float(S)
    else:
        return 0.0


def _sint(S):
    """
    convert a string to an integer, treating an all-blank string as zero
    Parameter
    ---------
    S : str
        string that need to be converted as integer treating an all-blank
        strings as zero

    Returns
    -------
    integer or zero
    """
    if S.strip():
        return int(S)
    else:
        return 0