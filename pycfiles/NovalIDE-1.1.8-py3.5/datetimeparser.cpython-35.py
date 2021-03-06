# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/util/datetimeparser.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 3570 bytes
import datetime
try:
    import dateutil.parser
    DATEUTIL_INSTALLED = True
except ImportError:
    DATEUTIL_INSTALLED = False

ISO_8601_DATE_FORMAT = '%Y-%m-%d'
ISO_8601_TIME_FORMAT = '%H:%M:%S'
ISO_8601_DATETIME_FORMAT = '%s %s' % (ISO_8601_DATE_FORMAT,
 ISO_8601_TIME_FORMAT)
DEFAULT_DATETIME = datetime.datetime(1, 1, 1, 0, 0, 0, 0)

def format(dateobj, formatstr=None):
    if formatstr != None and _isDateTimeObject(dateobj):
        return dateobj.strftime(str(formatstr))
    return str(dateobj)


def parse(datestr, formatstr=None, asdate=False, astime=False):
    """Instantiates and returns a datetime instance from the datestr datetime
       representation.
       
       Optionally, a format string may be used. The format is only loosely
       interpreted, its only purpose beeing to determine if the year is first
       or last in datestr, and whether the day is in front or follows the
       month. If no formatstr is passed in, dateutil tries its best to parse
       the datestr. The default date format is YYYY-mm-dd HH:SS.
       
       If asdate is True, returns a date instance instead of a datetime
       instance, if astime is True, returns a time instance instead of a
       datetime instance."""
    dayfirst, yearfirst = _getDayFirstAndYearFirst(formatstr)
    rtn = None
    try:
        if DATEUTIL_INSTALLED:
            rtn = dateutil.parser.parse(str(datestr), fuzzy=True, dayfirst=dayfirst, yearfirst=yearfirst, default=DEFAULT_DATETIME)
        else:
            rtn = DEFAULT_DATETIME
    except:
        rtn = DEFAULT_DATETIME

    if asdate and isinstance(rtn, datetime.datetime):
        rtn = datetime.date(rtn.year, rtn.month, rtn.day)
    elif astime and isinstance(rtn, datetime.datetime):
        rtn = datetime.time(rtn.hour, rtn.minute, rtn.second, rtn.microsecond)
    return rtn


def _isDateTimeObject(obj):
    return isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date) or isinstance(obj, datetime.time)


def _getDayFirstAndYearFirst(formatstr):
    dayFirst = False
    yearFirst = False
    gotYear = False
    gotMonth = False
    gotDay = False
    if formatstr == None:
        formatstr = ''
    for c in formatstr:
        if c.lower() == 'y':
            if gotYear:
                pass
            else:
                if not gotDay and not gotMonth:
                    yearFirst = True
                gotYear = True
        else:
            if c.lower() == 'm':
                if gotMonth:
                    pass
                else:
                    if not gotDay:
                        dayFirst = False
                    gotMonth = True
            elif c.lower() == 'd':
                if gotDay:
                    pass
                else:
                    if not gotMonth:
                        dayFirst = True
                    gotDay = True

    return (
     dayFirst, yearFirst)