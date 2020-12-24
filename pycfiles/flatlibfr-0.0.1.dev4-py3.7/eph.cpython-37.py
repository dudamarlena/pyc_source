# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/flatlibfr/ephem/eph.py
# Compiled at: 2019-10-17 02:47:28
# Size of source mod 2**32: 3019 bytes
"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    flatlibfr translation of const by Stéphane Bressani (s.bressani@bluewin.ch)
    
    This module implements functions for retrieving 
    astronomical and astrological data from an ephemeris.
    
    It is as middle layer between the Swiss Ephemeris 
    and user software. Objects are treated as python 
    dicts and jd/lat/lon as float.
  
"""
from . import swe
from . import tools
from flatlibfr import angle
from flatlibfr import const

def getObject(ID, jd, lat, lon):
    """ Returns an object for a specific date and 
    location.
    
    """
    if ID == const.SOUTH_NODE:
        obj = swe.sweObject(const.NORTH_NODE, jd)
        obj.update({'id':const.SOUTH_NODE, 
         'lon':angle.norm(obj['lon'] + 180)})
    else:
        if ID == const.PARS_FORTUNA:
            pflon = tools.pfLon(jd, lat, lon)
            obj = {'id':ID, 
             'lon':pflon, 
             'lat':0, 
             'lonspeed':0, 
             'latspeed':0}
        else:
            if ID == const.SYZYGY:
                szjd = tools.syzygyJD(jd)
                obj = swe.sweObject(const.MOON, szjd)
                obj['id'] = const.SYZYGY
            else:
                obj = swe.sweObject(ID, jd)
    _signInfo(obj)
    return obj


def getHouses(jd, lat, lon, hsys):
    """ Returns lists of houses and angles. """
    houses, angles = swe.sweHouses(jd, lat, lon, hsys)
    for house in houses:
        _signInfo(house)

    for angle in angles:
        _signInfo(angle)

    return (
     houses, angles)


def getFixedStar(ID, jd):
    """ Returns a fixed star. """
    star = swe.sweFixedStar(ID, jd)
    _signInfo(star)
    return star


def nextSolarReturn(jd, lon):
    """ Return the JD of the next solar return. """
    return tools.solarReturnJD(jd, lon, True)


def prevSolarReturn(jd, lon):
    """ Returns the JD of the previous solar return. """
    return tools.solarReturnJD(jd, lon, False)


def nextSunrise(jd, lat, lon):
    """ Returns the JD of the next sunrise. """
    return swe.sweNextTransit(const.SUN, jd, lat, lon, 'RISE')


def nextSunset(jd, lat, lon):
    """ Returns the JD of the next sunset. """
    return swe.sweNextTransit(const.SUN, jd, lat, lon, 'SET')


def lastSunrise(jd, lat, lon):
    """ Returns the JD of the last sunrise. """
    return nextSunrise(jd - 1.0, lat, lon)


def lastSunset(jd, lat, lon):
    """ Returns the JD of the last sunset. """
    return nextSunset(jd - 1.0, lat, lon)


def nextStation(ID, jd):
    """ Returns the aproximate jd of the next station. """
    return tools.nextStationJD(ID, jd)


def _signInfo(obj):
    """ Appends the sign id and longitude to an object. """
    lon = obj['lon']
    obj.update({'sign':const.LIST_SIGNS[int(lon / 30)], 
     'signlon':lon % 30})