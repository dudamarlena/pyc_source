# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fluid/common/distance.py
# Compiled at: 2006-12-05 08:29:05
"""Distances along Earth's surface"""
import numpy as N
DEG2RAD = 2 * N.pi / 360
RAD2DEG = 1 / DEG2RAD
DEG2MIN = 60.0
DEG2NM = 60.0
NM2M = 1852.0

def distance(lat, lon, lat_c=None, lon_c=None, method='simplest'):
    """Calculate distances along Earth's surface

    !!!! Uncomplete, improve it !!! !!!!!

    -> Simplest method based on Seawater routines for MatLab

    Input:
        - lat => [deg] Latitude
        - lon => [deg] Longitude
        - lat_c => [deg] Central latitude, or the reference position
        - lon_c => [deg] Central longitude, or the reference position
        - method =>
    Output:
        - L => [m] If lat_c and lon_c are given is the distance of each point
                     to the [lat_c,lon_c]. Otherwise is the distance between
                     the sucessive point, like L(2->1), L(3->2), L(4->3) ...
    """
    if lat_c is not None and lon_c is not None:
        fac = N.cos((lat_c + lat) / 2.0 * N.pi / 180)
        L = ((lat - lat_c) ** 2 + ((lon - lon_c) * fac) ** 2) ** 0.5
        L = L * DEG2NM * NM2M
        return L
    elif lat_c is None and lon_c is None:
        fac = N.cos((lat[:-1] + lat[1:]) / 2.0 * N.pi / 180.0)
        L = ((lat[:-1] - lat[1:]) ** 2 + ((lon[:-1] - lon[1:]) * fac) ** 2) ** 0.5
        L = L * DEG2NM * NM2M
        return L
    else:
        return
    return