# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\timeu.py
# Compiled at: 2019-11-27 15:02:29
# Size of source mod 2**32: 11230 bytes
"""
timeu -- time methods
============================

Common time methods
"""
import datetime, calendar, tzlocal, pytz

def epoch2dt(epochtime):
    """
    get a datetime object corresponding to an epoch time
    
    :param epochtime: epoch time to convert
    :rtype: datetime object
    """
    return datetime.datetime.utcfromtimestamp(epochtime)


def dt2epoch(dt):
    """
    get an epoch time corresponding to a datetime object 
    
    :param dt: datetime object to convert
    :rtype: int (epoch time)
    """
    if dt.tzinfo:
        UTC = pytz.timezone('UTC')
        utcdt = dt.astimezone(UTC)
    else:
        utcdt = dt
    return int(calendar.timegm(utcdt.timetuple()))


def epoch2localdt(epochtime):
    """
    convert from epoch time to datetime local timezone
    
    :param epochtime: utc time in epoch format
    :rtype: datetime in local timezone
    """
    localtz = tzlocal.get_localzone()
    utc = pytz.utc.localize(epoch2dt(epochtime))
    localtime = utc.astimezone(localtz)
    return localtime


def excel2dt(exceltime):
    """
    get an datetime corresonding to an excel floating time

    raises ValueError if invalid exceltime format (must be int or float, or string version of same)
    
    NOTE: only works for dates after 3/1/1900
    see http://www.lexicon.net/sjmachin/xlrd.html for more details
    
   :param exceltime: time field from excel
    :rtype: datetime.datetime
    """
    exceltime = float(exceltime)
    return __EXCELEPOCH + datetime.timedelta(exceltime)


def dt2excel(dt):
    """
    get an excel floating time from datetime
    
    NOTE: only works for dates after 3/1/1900 due to excel bug
    see http://www.lexicon.net/sjmachin/xlrd.html for more details

    :param dt: datetime field
    :rtype: int or float with excel epoch
    """
    dif = dt - __EXCELEPOCH
    seconds = dif.seconds + dif.microseconds / 1000000.0
    fracdays = seconds / 86400
    return dif.days + fracdays


def tzdt2utcdt(dt, tzid):
    """
    convert datetime of timezone id to UTC
    
    :param dt: datetime.datetime object
    :param tzid: timezone id (e.g., 'America/New_York')
    :rtype: datetime.datetime at UTC
    """
    tz = pytz.timezone(tzid)
    utc = pytz.timezone('UTC')
    d_tz = tz.normalize(tz.localize(dt))
    d_utc = d_tz.astimezone(utc)
    return d_utc


def utcdt2tzdt(dt, tzid):
    """
    convert UTC datetime to timezone
    
    :param dt: datetime.datetime object
    :param tzid: timezone id (e.g., 'America/New_York')
    :rtype: datetime.datetime at timezone
    """
    tz = pytz.timezone(tzid)
    utc = pytz.timezone('UTC')
    d_tz = utc.normalize(utc.localize(dt))
    localetime = d_tz.astimezone(tz)
    return localetime


def age(asof, dob):
    """
    get age as of a date based on birth date
    
    :param asof: datetime object, get age asof date based on dob birth date
    :param dob: datetime object, get age asof date based on dob birth date
    """
    return asof.year - dob.year - int((asof.month, asof.day) < (dob.month, dob.day))


def timesecs(asctime):
    """
    calculate time in seconds from string time
    
    :param asctime: string time
    :rtype: float, time in seconds
    """
    timefields = asctime.split(':')
    thistime = 0.0
    for timefield in timefields:
        thistime *= 60
        thistime += float(timefield)

    return thistime


def racetimesecs(asctime, distance, fastpace, slowpace):
    """
    calculate time in seconds from string time

    if pace is faster than fastpace, multiply by 60
    if pace is slower than slowpace, divide by 60
    
    :param asctime: string time
    :param distance: distance in units
    :param fastpace: fast pace in seconds per unit
    :param slowpace: slow pace in seconds per unit
    :rtype: float, time in seconds
    """
    timefields = asctime.split(':')
    thistime = 0.0
    for timefield in timefields:
        thistime *= 60
        thistime += float(timefield)

    pace = thistime / distance
    if pace < fastpace:
        thistime *= 60
    else:
        if pace > slowpace:
            thistime /= 60
    return thistime


class asctime:
    __doc__ = '\n    asctime -- provide formatting methods for ascii time format\n    \n    :param ascformat: time format for ascii conversion.  See http://docs.python.org/2/library/datetime.html#strftime-strptime-behavior for formats\n    '

    def __init__(self, ascformat):
        self.ascformat = ascformat

    def asc2dt(self, asctime):
        """
        convert ASCII time to datetime object
        
        :param asctime: ASCII time
        :rtype: datetime.datetime object
        """
        return datetime.datetime.strptime(asctime, self.ascformat)

    def dt2asc(self, dt):
        """
        convert datetime object to ASCII TIME
        
        :param dt: datetime.datetime object
        :rtype: ASCII time
        """
        return datetime.datetime.strftime(dt, self.ascformat)

    def asc2epoch(self, asctime):
        """
        convert ASCII time to epoch time
        
        :param asctime: ASCII time
        :rtype: int (epoch time)
        """
        return dt2epoch(datetime.datetime.strptime(asctime, self.ascformat))

    def epoch2asc(self, epoch):
        """
        convert epoch time to ASCII time
        
        :param epoch: int (epoch time)
        :rtype: ASCII time
        """
        return datetime.datetime.strftime(epoch2dt(epoch), self.ascformat)

    def asc2excel(self, asctime):
        """
        convert ASCII time to excel time
        
        :param asctime: ASCII time
        :rtype: int or float (excel time)
        """
        return dt2excel(datetime.datetime.strptime(asctime, self.ascformat))

    def excel2asc(self, excel):
        """
        convert excel time to ASCII time
        
        :param excel: int or float (excel time)
        :rtype: ASCII time
        """
        return datetime.datetime.strftime(excel2dt(excel), self.ascformat)


__EXCELEPOCH = asctime('%Y-%m-%d').asc2dt('1899-12-30')