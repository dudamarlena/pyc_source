# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\renderrun.py
# Compiled at: 2019-11-27 14:52:49
# Size of source mod 2**32: 6265 bytes
"""
renderrun - common functions for rendering information related to running
==============================================================================

"""
import math
from . import timeu
dbtime = timeu.asctime('%Y-%m-%d')
rndrtim = timeu.asctime('%m/%d/%Y')

class softwareError(Exception):
    pass


def getprecision(distance, surface='road'):
    """
    get the precision for rendering, based on distance
    
    precision might be different for time vs. age group adjusted time
    
    :param distance: distance (miles)
    :param surface: 'road', 'track' or 'trail', default 'road'
    :rtype: (timeprecision,agtimeprecision)
    """
    meterspermile = 1609
    if surface == 'track':
        timeprecision = 1
        agtimeprecision = 1
    else:
        timeprecision = 0
        agtimeprecision = 0
    return (timeprecision, agtimeprecision)


def renderdate(dbdate):
    """
    create date for display
    
    :param dbdate: date from database ('yyyy-mm-dd')
    """
    try:
        dtdate = dbtime.asc2dt(dbdate)
        rval = rndrtim.dt2asc(dtdate)
    except ValueError:
        rval = dbdate

    return rval


def adjusttime(rawtime, precision, useceiling=True):
    """
    adjust raw time based on precision
    
    :param rawtime: time in seconds
    :param precision: number of places after decimal point
    :param useceiling: True if ceiling function to be used (round up)
    
    :rtype: adjusted time in seconds (float)
    """
    multiplier = 10 ** precision
    fixedtime = rawtime * multiplier
    if useceiling:
        adjfixedtime = math.ceil(fixedtime)
    else:
        adjfixedtime = round(fixedtime)
    adjtime = adjfixedtime / multiplier
    return adjtime


def rendertime(dbtime, precision, useceiling=True):
    """
    create time for display
    
    :param dbtime: time in seconds
    :param precision: number of places after decimal point
    :param useceiling: True if ceiling function to be used (round up)
    """
    if precision > 0:
        adjtime = adjusttime(dbtime, precision, useceiling)
        wholetime = int(adjtime)
        fractime = adjtime - wholetime
        fracformat = '{{0:0.{0}f}}'.format(precision)
        rettime = fracformat.format(fractime)
        remdbtime = wholetime
        if rettime[0] != '0':
            raise softwareError('formatted adjusted time fraction does not have leading 0: {0}'.format(adjtime))
        rettime = rettime[1:]
    else:
        if useceiling:
            remdbtime = int(math.ceil(dbtime))
        else:
            remdbtime = int(round(dbtime))
        rettime = ''
    thisunit = remdbtime % 60
    firstthru = True
    while remdbtime > 0:
        if not firstthru:
            rettime = ':' + rettime
        firstthru = False
        rettime = '{0:02d}'.format(thisunit) + rettime
        remdbtime /= 60
        thisunit = remdbtime % 60

    while rettime[0] == '0':
        rettime = rettime[1:]

    return rettime