# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gtimes/gpstime.py
# Compiled at: 2014-12-10 10:51:33
"""
A Python implementation of GPS related time conversions.

Copyright 2002 by Bud P. Bruegger, Sistema, Italy
mailto:bud@sistema.it
http://www.sistema.it

Modifications for GPS seconds by Duncan Brown

PyUTCFromGpsSeconds added by Ben Johnson

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation; either version 2 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License along
with this program; if not, write to the Free Software Foundation, Inc., 59
Temple Place, Suite 330, Boston, MA  02111-1307  USA

GPS Time Utility functions

This file contains a Python implementation of GPS related time conversions.

The two main functions convert between UTC and GPS time (GPS-week, time of
week in seconds, GPS-day, time of day in seconds).  The other functions are
convenience wrappers around these base functions.  

A good reference for GPS time issues is:
http://www.oc.nps.navy.mil/~jclynch/timsys.html

Note that python time types are represented in seconds since (a platform
dependent Python) Epoch.  This makes implementation quite straight forward
as compared to some algorigthms found in the literature and on the web.  
"""
__author__ = 'Benedikt G. Ofeigsson <bgo@vedur.is> edited from Duncan Brown <duncan@gravity.phys.uwm.edu>'
__date__ = '$Date: 2012/03/6'
__version__ = '$Revision: 1.6 $'[11:-2]
import time, math, calendar, datetime, pytz
from dateutil.tz import tzlocal
secsInWeek = 604800
secsInDay = 86400
gpsEpoch = (1980, 1, 6, 0, 0, 0)

def dayOfWeek(year, month, day):
    """
    Returns day of week: 0=Sun, 1=Mon, .., 6=Sat
    """
    hr = 12
    t = time.mktime((year, month, day, hr, 0, 0, 0, 0, -1))
    pyDow = time.localtime(t)[6]
    gpsDow = (pyDow + 1) % 7
    return gpsDow


def gpsWeek(year, month, day):
    """
    Returns (full) gpsWeek for given date (in UTC)
    """
    hr = 12
    return gpsFromUTC(year, month, day, hr, 0, 0)[0]


def julianDay(year, month, day):
    """returns julian day=day since Jan 1 of year"""
    hr = 12
    t = time.mktime((year, month, day, hr, 0, 0.0, 0, 0, -1))
    julDay = time.localtime(t)[7]
    return julDay


def mkUTC(year, month, day, hour, min, sec):
    """
    Similar to python's mktime but for utc
    """
    spec = [
     year, month, day, hour, min, sec] + [0, 0, 0]
    utc = time.mktime(spec) - time.timezone
    return utc


def ymdhmsFromPyUTC(pyUTC):
    """
    Returns tuple from a python time value in UTC
    """
    ymdhmsXXX = time.gmtime(pyUTC)
    return ymdhmsXXX[:-3]


def wtFromUTCpy(pyUTC, leapSecs=16):
    """
    Convenience function:
    BGO 07.01.2013: changed the default leapsecond to 16
         allows to use python UTC times and
         returns only week and tow"""
    ymdhms = ymdhmsFromPyUTC(pyUTC)
    wSowDSoD = apply(gpsFromUTC, ymdhms + (leapSecs,))
    return wSowDSoD[0:2]


def gpsFromUTC(year, month, day, hour, min, sec, leapSecs=16):
    """
    Converts UTC to: gpsWeek, secsOfWeek, gpsDay, secsOfDay

    a good reference is:  http://www.oc.nps.navy.mil/~jclynch/timsys.html

    This is based on the following facts (see reference above):

    GPS time is basically measured in (atomic) seconds since 
    January 6, 1980, 00:00:00.0  (the GPS Epoch)
    
    The GPS week starts on Saturday midnight (Sunday morning), and runs
    for 604800 seconds. 

    Currently, GPS time is 13 seconds ahead of UTC (see above reference).
    While GPS SVs transmit this difference and the date when another leap
    second takes effect, the use of leap seconds cannot be predicted.  This
    routine is precise until the next leap second is introduced and has to be
    updated after that.
    BGO 07.01.2013: changed the default leapsecond to 16

    SOW = Seconds of Week
    SOD = Seconds of Day

    Note:  Python represents time in integer seconds, fractions are lost!!!
    """
    secFract = sec % 1
    epochTuple = gpsEpoch + (-1, -1, 0)
    t0 = time.mktime(epochTuple)
    t = time.mktime((year, month, day, hour, min, sec, -1, -1, 0))
    t = t + leapSecs
    tdiff = t - t0
    gpsSOW = tdiff % secsInWeek + secFract
    gpsWeek = int(math.floor(tdiff / secsInWeek))
    gpsDay = int(math.floor(gpsSOW / secsInDay))
    gpsSOD = gpsSOW % secsInDay
    return (gpsWeek, gpsSOW, gpsDay, gpsSOD)


def UTCFromGps(gpsWeek, SOW, leapSecs=16):
    """
    Converts gps week and seconds to UTC
    BGO 07.01.2013: changed the default leapsecond to 16

    see comments of inverse function!

    SOW = seconds of week
    gpsWeek is the full number (not modulo 1024)
    """
    secFract = SOW % 1
    epochTuple = gpsEpoch + (-1, -1, 0)
    t0 = time.mktime(epochTuple) - time.timezone
    tdiff = gpsWeek * secsInWeek + SOW - leapSecs
    t = t0 + tdiff
    year, month, day, hh, mm, ss, dayOfWeek, julianDay, daylightsaving = time.gmtime(t)
    return (
     year, month, day, hh, mm, ss + secFract)


def GpsSecondsFromPyUTC(pyUTC, leapSecs=16):
    """
    Converts the python epoch to gps seconds
    BGO 07.01.2013: changed the default leapsecond to 16

    pyEpoch = the python epoch from time.time()
    """
    t = t = gpsFromUTC(*ymdhmsFromPyUTC(pyUTC))
    return int(t[0] * 60 * 60 * 24 * 7 + t[1])


def PyUTCFromGpsSeconds(gpsseconds):
    """
    Converts gps seconds to the
    python epoch. That is, the time
    that would be returned from time.time()
    at gpsseconds.
    """
    pyUTC


def testTimeStuff():
    print '--------------------'
    print
    print 'The GPS Epoch when everything began (1980, 1, 6, 0, 0, 0, leapSecs=0)'
    w, sow, d, sod = gpsFromUTC(1980, 1, 6, 0, 0, 0, leapSecs=0)
    print '**** week: %s, sow: %s, day: %s, sod: %s' % (w, sow, d, sod)
    print '     and hopefully back:'
    print '**** %s, %s, %s, %s, %s, %s\n' % UTCFromGps(w, sow, leapSecs=0)
    print 'The time of first Rollover of GPS week (1999, 8, 21, 23, 59, 47)'
    w, sow, d, sod = gpsFromUTC(1999, 8, 21, 23, 59, 47)
    print '**** week: %s, sow: %s, day: %s, sod: %s' % (w, sow, d, sod)
    print '     and hopefully back:'
    print '**** %s, %s, %s, %s, %s, %s\n' % UTCFromGps(w, sow, leapSecs=14)
    print 'Today is GPS week 1186, day 3, seems to run ok (2002, 10, 2, 12, 6, 13.56)'
    w, sow, d, sod = gpsFromUTC(2002, 10, 2, 12, 6, 13.56)
    print '**** week: %s, sow: %s, day: %s, sod: %s' % (w, sow, d, sod)
    print '     and hopefully back:'
    print '**** %s, %s, %s, %s, %s, %s\n' % UTCFromGps(w, sow)


def testJulD():
    print '2002, 10, 11 -> 284  ==??== ', julianDay(2002, 10, 11)


def testGpsWeek():
    print '2002, 10, 11 -> 1187  ==??== ', gpsWeek(2002, 10, 11)


def testDayOfWeek():
    print '2002, 10, 12 -> 6  ==??== ', dayOfWeek(2002, 10, 12)
    print '2002, 10, 6  -> 0  ==??== ', dayOfWeek(2002, 10, 6)


def testPyUtilties():
    ymdhms = (2002, 10, 12, 8, 34, 12.3)
    print 'testing for: ', ymdhms
    pyUtc = apply(mkUTC, ymdhms)
    back = ymdhmsFromPyUTC(pyUtc)
    print 'yields     : ', back
    w, t = wtFromUTCpy(pyUtc)
    print 'week and time: ', (w, t)


if __name__ == '__main__':
    testTimeStuff()
    testGpsWeek()
    testJulD()
    testDayOfWeek()
    testPyUtilties()