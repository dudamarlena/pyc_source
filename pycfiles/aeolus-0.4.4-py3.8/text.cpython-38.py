# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aeolus/plot/text.py
# Compiled at: 2019-10-29 08:08:29
# Size of source mod 2**32: 1455 bytes
"""Text-related formatting functions."""
import itertools, string
from LatLon23 import Latitude, Longitude
from ..exceptions import ArgumentError
__all__ = ('fmt_lonlat', 'subplot_label_generator')

def fmt_lonlat(value, lon_or_lat, degree=False):
    r"""
    Convert longitude or latitude value to string with a hemisphere identifier.

    Parameters
    ----------
    value: int
        Value of longitude or latitude. Note that this function is only for integer values.
    lon_or_lat: str
        Longitude or latitude
    degree: bool, optional
        If true, a TeX degree symbol is included

    Returns
    -------
    str

    Examples
    --------
    >>> fmt_lonlat(-25, "lon")
    '25W'
    >>> fmt_lonlat(89, "lat", degree=True)
    '89$^\\degree$N'
    >>> fmt_lonlat(0, "lon")
    '0'
    """
    if lon_or_lat.lower().startswith('lat'):
        res = Latitude(value)
    else:
        if lon_or_lat.lower().startswith('lon'):
            res = Longitude(value)
        else:
            raise ArgumentError('2nd arg or the function should start with `lon` or `lat`')
    out = res.to_string('%d%H')
    if degree:
        out = out[:-1] + '$^\\degree$' + out[(-1)]
    if value == 0:
        out = out[:-1]
    return out


def subplot_label_generator():
    """Return generator of alphabetic labelling of subplots."""
    for i in itertools.count(1):
        for p in itertools.product((string.ascii_lowercase), repeat=i):
            (yield ''.join(p))