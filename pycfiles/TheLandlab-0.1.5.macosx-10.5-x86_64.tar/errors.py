# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/io/netcdf/errors.py
# Compiled at: 2014-09-23 12:37:24


class Error(Exception):
    """
    Base class for errors in this package.
    """
    pass


class NotRasterGridError(Error):
    """
    Raise this error if the grid defined in the netcdf file is not
    uniform rectilinear with constant spacing in all dimensions.
    """
    pass