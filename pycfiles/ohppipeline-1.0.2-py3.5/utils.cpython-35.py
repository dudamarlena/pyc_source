# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ohppipeline/utils/utils.py
# Compiled at: 2020-02-06 11:00:35
# Size of source mod 2**32: 1427 bytes
"""
This module provide utils functions for the rest of the package

:author: C. Hottier
"""
import astropy.units as u
from ccdproc import CCDData
from numpy import ndarray

def getlistccddata(inputlist, unit=u.adu):
    """process a list of fits filename or CCDData to obtain only CCDData

    :param inputlist: list or array-like of fits name or CCDData
    :param unit: the unit (astropy.units) to apply for reading CCDData, default adu
    :returns: list of CCDData

    """
    return [getccddata(f, unit=unit) for f in inputlist]


def getccddata(fits, unit=u.adu):
    """obtain a ccddata from inp 

    :param fits: input information filename, numpy.array, ccdata
    :param unit: the unit to use to create the CCDData, ignore if inp already CCDData, default adu
    :raise ValueError: if the type of fits is not suitable
    :returns: CCDData corresping to inp

    """
    if isinstance(fits, str):
        return CCDData.read(fits, unit=unit)
    if isinstance(fits, ndarray):
        return CCDData(fits, unit=unit)
    if isinstance(fits, CCDData):
        return fits
    raise ValueError('%s type can not be convert to CCData' % type(fits))