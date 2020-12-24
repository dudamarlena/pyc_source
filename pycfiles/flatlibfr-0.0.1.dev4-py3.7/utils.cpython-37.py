# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/flatlibfr/utils.py
# Compiled at: 2019-10-17 02:47:28
# Size of source mod 2**32: 2416 bytes
"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    flatlibfr translation of const by Stéphane Bressani (s.bressani@bluewin.ch)
    
    This module provides generic utility functions. 
"""
import math
from . import angle

def ascdiff(decl, lat):
    """ Returns the Ascensional Difference of a point. """
    delta = math.radians(decl)
    phi = math.radians(lat)
    ad = math.asin(math.tan(delta) * math.tan(phi))
    return math.degrees(ad)


def dnarcs(decl, lat):
    """ Returns the diurnal and nocturnal arcs of a point. """
    dArc = 180 + 2 * ascdiff(decl, lat)
    nArc = 360 - dArc
    return (dArc, nArc)


def isAboveHorizon(ra, decl, mcRA, lat):
    """ Returns if an object's 'ra' and 'decl' 
    is above the horizon at a specific latitude, 
    given the MC's right ascension.
    
    """
    dArc, _ = dnarcs(decl, lat)
    dist = abs(angle.closestdistance(mcRA, ra))
    return dist <= dArc / 2.0 + 0.0003


def eqCoords(lon, lat):
    """ Converts from ecliptical to equatorial coordinates. 
    This algorithm is described in book 'Primary Directions', 
    pp. 147-150.
    
    """
    _lambda = math.radians(lon)
    _beta = math.radians(lat)
    _epson = math.radians(23.44)
    decl = math.asin(math.sin(_epson) * math.sin(_lambda) * math.cos(_beta) + math.cos(_epson) * math.sin(_beta))
    ED = math.acos(math.cos(_lambda) * math.cos(_beta) / math.cos(decl))
    ra = ED if lon < 180 else math.radians(360) - ED
    if abs(angle.closestdistance(lon, 0)) < 5 or abs(angle.closestdistance(lon, 180)) < 5:
        a = math.sin(ra) * math.cos(decl)
        b = math.cos(_epson) * math.sin(_lambda) * math.cos(_beta) - math.sin(_epson) * math.sin(_beta)
        if math.fabs(a - b) > 0.0003:
            ra = math.radians(360) - ra
    return (
     math.degrees(ra), math.degrees(decl))