# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/python-dateutil/dateutil/tzwin.py
# Compiled at: 2018-07-11 18:15:31
import datetime, struct
from six.moves import winreg
__all__ = [
 'tzwin', 'tzwinlocal']
ONEWEEK = datetime.timedelta(7)
TZKEYNAMENT = 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Time Zones'
TZKEYNAME9X = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Time Zones'
TZLOCALKEYNAME = 'SYSTEM\\CurrentControlSet\\Control\\TimeZoneInformation'

def _settzkeyname():
    handle = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    try:
        winreg.OpenKey(handle, TZKEYNAMENT).Close()
        TZKEYNAME = TZKEYNAMENT
    except WindowsError:
        TZKEYNAME = TZKEYNAME9X

    handle.Close()
    return TZKEYNAME


TZKEYNAME = _settzkeyname()

class tzwinbase(datetime.tzinfo):
    """tzinfo class based on win32's timezones available in the registry."""

    def utcoffset(self, dt):
        if self._isdst(dt):
            return datetime.timedelta(minutes=self._dstoffset)
        else:
            return datetime.timedelta(minutes=self._stdoffset)

    def dst(self, dt):
        if self._isdst(dt):
            minutes = self._dstoffset - self._stdoffset
            return datetime.timedelta(minutes=minutes)
        else:
            return datetime.timedelta(0)

    def tzname(self, dt):
        if self._isdst(dt):
            return self._dstname
        else:
            return self._stdname

    def list():
        """Return a list of all time zones known to the system."""
        handle = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        tzkey = winreg.OpenKey(handle, TZKEYNAME)
        result = [ winreg.EnumKey(tzkey, i) for i in range(winreg.QueryInfoKey(tzkey)[0])
                 ]
        tzkey.Close()
        handle.Close()
        return result

    list = staticmethod(list)

    def display(self):
        return self._display

    def _isdst(self, dt):
        if not self._dstmonth:
            return False
        else:
            dston = picknthweekday(dt.year, self._dstmonth, self._dstdayofweek, self._dsthour, self._dstminute, self._dstweeknumber)
            dstoff = picknthweekday(dt.year, self._stdmonth, self._stddayofweek, self._stdhour, self._stdminute, self._stdweeknumber)
            if dston < dstoff:
                return dston <= dt.replace(tzinfo=None) < dstoff
            return not dstoff <= dt.replace(tzinfo=None) < dston
            return


class tzwin(tzwinbase):

    def __init__(self, name):
        self._name = name
        with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as (handle):
            with winreg.OpenKey(handle, '%s\\%s' % (TZKEYNAME, name)) as (tzkey):
                keydict = valuestodict(tzkey)
        self._stdname = keydict['Std'].encode('iso-8859-1')
        self._dstname = keydict['Dlt'].encode('iso-8859-1')
        self._display = keydict['Display']
        tup = struct.unpack('=3l16h', keydict['TZI'])
        self._stdoffset = -tup[0] - tup[1]
        self._dstoffset = self._stdoffset - tup[2]
        self._stdmonth, self._stddayofweek, self._stdweeknumber, self._stdhour, self._stdminute = tup[4:9]
        self._dstmonth, self._dstdayofweek, self._dstweeknumber, self._dsthour, self._dstminute = tup[12:17]
        return

    def __repr__(self):
        return 'tzwin(%s)' % repr(self._name)

    def __reduce__(self):
        return (
         self.__class__, (self._name,))


class tzwinlocal(tzwinbase):

    def __init__(self):
        with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as (handle):
            with winreg.OpenKey(handle, TZLOCALKEYNAME) as (tzlocalkey):
                keydict = valuestodict(tzlocalkey)
            self._stdname = keydict['StandardName'].encode('iso-8859-1')
            self._dstname = keydict['DaylightName'].encode('iso-8859-1')
            try:
                with winreg.OpenKey(handle, '%s\\%s' % (TZKEYNAME, self._stdname)) as (tzkey):
                    _keydict = valuestodict(tzkey)
                    self._display = _keydict['Display']
            except OSError:
                self._display = None

        self._stdoffset = -keydict['Bias'] - keydict['StandardBias']
        self._dstoffset = self._stdoffset - keydict['DaylightBias']
        tup = struct.unpack('=8h', keydict['StandardStart'])
        self._stdmonth, self._stddayofweek, self._stdweeknumber, self._stdhour, self._stdminute = tup[1:6]
        tup = struct.unpack('=8h', keydict['DaylightStart'])
        self._dstmonth, self._dstdayofweek, self._dstweeknumber, self._dsthour, self._dstminute = tup[1:6]
        return

    def __reduce__(self):
        return (self.__class__, ())


def picknthweekday(year, month, dayofweek, hour, minute, whichweek):
    """dayofweek == 0 means Sunday, whichweek 5 means last instance"""
    first = datetime.datetime(year, month, 1, hour, minute)
    weekdayone = first.replace(day=(dayofweek - first.isoweekday()) % 7 + 1)
    for n in range(whichweek):
        dt = weekdayone + (whichweek - n) * ONEWEEK
        if dt.month == month:
            return dt


def valuestodict(key):
    """Convert a registry key's values to a dictionary."""
    dict = {}
    size = winreg.QueryInfoKey(key)[1]
    for i in range(size):
        data = winreg.EnumValue(key, i)
        dict[data[0]] = data[1]

    return dict