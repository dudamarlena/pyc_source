# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/io/tests/test_netCDF_io.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 1207 bytes
"""
This module contains test functions for the file-IO functions
for reading and writing data sets using the netCDF file format.

The files read and written using this function are assumed to 
conform to the format specified for x-ray computed microtomorgraphy
data collected at Argonne National Laboratory, Sector 13, GSECars.
"""
import numpy as np, six
from nose.tools import eq_
import skxray.io.net_cdf_io as ncd

def test_net_cdf_io():
    """
    Test function for netCDF read function load_netCDF()

    Parameters
    ----------
    test_data : str

    Returns
    -------

    """
    pass