# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/PyGS/utils.py
# Compiled at: 2013-06-04 20:12:48
__doc__ = '\nCreated on Dec 3, 2012\n\n@author: Steven\n'
import numpy as np

def FD_bins(data):
    """
        Calculates the optimal number of bins for a histogram based on Freedman-Diaconis equation
        """
    from scipy.stats import scoreatpercentile as sap
    data = np.array(data)
    IQR = sap(data, 75) - sap(data, 25)
    width = 2 * IQR / len(data) ** (1.0 / 3.0)
    bins = np.ceil((max(data) - min(data)) / width)
    return bins


def sph2car(r, theta, phi):
    """
    Takes a spherical polar co-ordinate vector and returns a cartesian one
    """
    x = r * np.cos(theta) * np.sin(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(phi)
    return (
     x, y, z)


def car2sph(x, y, z):
    """
    Takes a cartesian vector and returns a spherical polar one
    """
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    theta = np.arctan2(y, x)
    phi = np.arccos(z / r)
    return (
     r, theta, phi)