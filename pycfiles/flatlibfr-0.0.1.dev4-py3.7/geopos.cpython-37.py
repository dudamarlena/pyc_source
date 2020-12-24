# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/flatlibfr/geopos.py
# Compiled at: 2019-10-17 02:47:28
# Size of source mod 2**32: 2282 bytes
"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    flatlibfr translation of const by Stéphane Bressani (s.bressani@bluewin.ch)

    This module provides functions and a class for handling 
    geographic positions. Each latitude/longitude is an angle 
    represented by a <float> value.

"""
from . import angle
LAT = 0
LON = 1
SIGN = {'N':'+', 
 'S':'-',  'E':'+',  'W':'-'}
CHAR = {LAT: {'+':'N',  '-':'S'}, 
 LON: {'+':'E',  '-':'W'}}

def toFloat(value):
    """ Converts angle representation to float. 
    Accepts angles and strings such as "12W30:00".
    
    """
    if isinstance(value, str):
        value = value.upper()
        for char in ('N', 'S', 'E', 'W'):
            if char in value:
                value = SIGN[char] + value.replace(char, ':')
                break

    return angle.toFloat(value)


def toList(value):
    """ Converts angle float to signed list. """
    return angle.toList(value)


def toString(value, mode):
    """ Converts angle float to string. 
    Mode refers to LAT/LON.
    
    """
    string = angle.toString(value)
    sign = string[0]
    separator = CHAR[mode][sign]
    string = string.replace(':', separator, 1)
    return string[1:]


class GeoPos:
    __doc__ = ' This class represents a geographic position \n    on the planet specified by a given lat and lon.\n    \n    Objects of this class can be instantiated with\n    GeoPos("45N32", "128W45") or another angle type\n    such as strings, signed lists or floats. \n    \n    '

    def __init__(self, lat, lon):
        self.lat = toFloat(lat)
        self.lon = toFloat(lon)

    def slists(self):
        """ Return lat/lon as signed lists. """
        return [
         toList(self.lat),
         toList(self.lon)]

    def strings(self):
        """ Return lat/lon as strings. """
        return [
         toString(self.lat, LAT),
         toString(self.lon, LON)]

    def __str__(self):
        strings = self.strings()
        return '<%s %s>' % (strings[0], strings[1])