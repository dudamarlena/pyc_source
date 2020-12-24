# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sqlstring/utils.py
# Compiled at: 2016-05-11 11:22:05
# Size of source mod 2**32: 1373 bytes
"""
General purpose utility library..
"""
import math

class Constants(object):
    __doc__ = '\n    Constants.\n    '

    class Earth(object):
        __doc__ = '\n        Earth constants.\n        '
        GRAVITY = 9.80665

    class Mars(object):
        __doc__ = '\n        Mars constants.\n        '
        GRAVITY = 9


def orbital_speed(planet, planatary_radius, altitude):
    """
    Calculate the orbital speed of an object.

    v = R*sqrt(g/(R+h))

    >>> from math import *
    >>> round(orbital_speed(Constants.Earth, 600000, 70), 3)
    2425.552
    """
    total_altitude = planatary_radius + altitude
    speed = planatary_radius * math.sqrt(planet.GRAVITY / total_altitude)
    return speed


def circumference(radius):
    """
    Calculate the circumference of an object.

    2*pi*r

    >>> from math import *
    >>> round(circumference(600000), 3)
    3769911.184
    """
    distance = 2 * math.pi * radius
    return distance


def orbital_period(planet, planatary_radius, altitude):
    """
    Calculate the orbital period of an object.

    d = v*t

    >>> from math import *
    >>> round(orbital_period(Constants.Earth, 600000, 70), 3)
    1554.43
    """
    cir = circumference(planatary_radius + altitude)
    return cir / orbital_speed(planet, planatary_radius, altitude)