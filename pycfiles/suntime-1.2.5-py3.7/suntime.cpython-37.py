# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/suntime/suntime.py
# Compiled at: 2019-08-26 08:45:56
# Size of source mod 2**32: 7127 bytes
import calendar, math, datetime
from dateutil import tz

class SunTimeException(Exception):

    def __init__(self, message):
        super(SunTimeException, self).__init__(message)


class Sun:
    __doc__ = '\n    Approximated calculation of sunrise and sunset datetimes. Adapted from:\n    https://stackoverflow.com/questions/19615350/calculate-sunrise-and-sunset-times-for-a-given-gps-coordinate-within-postgresql\n    '

    def __init__(self, lat, lon):
        self._lat = lat
        self._lon = lon

    def get_sunrise_time(self, date=None):
        """
        Calculate the sunrise time for given date.
        :param lat: Latitude
        :param lon: Longitude
        :param date: Reference date. Today if not provided.
        :return: UTC sunrise datetime
        :raises: SunTimeException when there is no sunrise and sunset on given location and date
        """
        date = datetime.date.today() if date is None else date
        sr = self._calc_sun_time(date, True)
        if sr is None:
            raise SunTimeException('The sun never rises on this location (on the specified date)')
        else:
            return sr

    def get_local_sunrise_time(self, date=None, local_time_zone=tz.tzlocal()):
        """
        Get sunrise time for local or custom time zone.
        :param date: Reference date. Today if not provided.
        :param local_time_zone: Local or custom time zone.
        :return: Local time zone sunrise datetime
        """
        date = datetime.date.today() if date is None else date
        sr = self._calc_sun_time(date, True)
        if sr is None:
            raise SunTimeException('The sun never rises on this location (on the specified date)')
        else:
            return sr.astimezone(local_time_zone)

    def get_sunset_time(self, date=None):
        """
        Calculate the sunset time for given date.
        :param lat: Latitude
        :param lon: Longitude
        :param date: Reference date. Today if not provided.
        :return: UTC sunset datetime
        :raises: SunTimeException when there is no sunrise and sunset on given location and date.
        """
        date = datetime.date.today() if date is None else date
        ss = self._calc_sun_time(date, False)
        if ss is None:
            raise SunTimeException('The sun never sets on this location (on the specified date)')
        else:
            return ss

    def get_local_sunset_time(self, date=None, local_time_zone=tz.tzlocal()):
        """
        Get sunset time for local or custom time zone.
        :param date: Reference date
        :param local_time_zone: Local or custom time zone.
        :return: Local time zone sunset datetime
        """
        date = datetime.date.today() if date is None else date
        ss = self._calc_sun_time(date, False)
        if ss is None:
            raise SunTimeException('The sun never sets on this location (on the specified date)')
        else:
            return ss.astimezone(local_time_zone)

    def _calc_sun_time(self, date, isRiseTime=True, zenith=90.8):
        """
        Calculate sunrise or sunset date.
        :param date: Reference date
        :param isRiseTime: True if you want to calculate sunrise time.
        :param zenith: Sun reference zenith
        :return: UTC sunset or sunrise datetime
        :raises: SunTimeException when there is no sunrise and sunset on given location and date
        """
        day = date.day
        month = date.month
        year = date.year
        TO_RAD = math.pi / 180.0
        N1 = math.floor(275 * month / 9)
        N2 = math.floor((month + 9) / 12)
        N3 = 1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3)
        N = N1 - N2 * N3 + day - 30
        lngHour = self._lon / 15
        if isRiseTime:
            t = N + (6 - lngHour) / 24
        else:
            t = N + (18 - lngHour) / 24
        M = 0.9856 * t - 3.289
        L = M + 1.916 * math.sin(TO_RAD * M) + 0.02 * math.sin(TO_RAD * 2 * M) + 282.634
        L = self._force_range(L, 360)
        RA = 1 / TO_RAD * math.atan(0.91764 * math.tan(TO_RAD * L))
        RA = self._force_range(RA, 360)
        Lquadrant = math.floor(L / 90) * 90
        RAquadrant = math.floor(RA / 90) * 90
        RA = RA + (Lquadrant - RAquadrant)
        RA = RA / 15
        sinDec = 0.39782 * math.sin(TO_RAD * L)
        cosDec = math.cos(math.asin(sinDec))
        cosH = (math.cos(TO_RAD * zenith) - sinDec * math.sin(TO_RAD * self._lat)) / (cosDec * math.cos(TO_RAD * self._lat))
        if cosH > 1:
            return
        elif cosH < -1:
            return
            if isRiseTime:
                H = 360 - 1 / TO_RAD * math.acos(cosH)
        else:
            H = 1 / TO_RAD * math.acos(cosH)
        H = H / 15
        T = H + RA - 0.06571 * t - 6.622
        UT = T - lngHour
        UT = self._force_range(UT, 24)
        hr = self._force_range(int(UT), 24)
        min = round((UT - int(UT)) * 60, 0)
        if min == 60:
            hr += 1
            min = 0
        if hr == 24:
            hr = 0
            day += 1
            if day > calendar.monthrange(year, month)[1]:
                day = 1
                month += 1
                if month > 12:
                    month = 1
                    year += 1
        return datetime.datetime(year, month, day, hr, (int(min)), tzinfo=(tz.tzutc()))

    @staticmethod
    def _force_range(v, max):
        if v < 0:
            return v + max
        if v >= max:
            return v - max
        return v


if __name__ == '__main__':
    sun = Sun(85.0, 21.0)
    try:
        print(sun.get_local_sunrise_time())
        print(sun.get_local_sunset_time())
        abd = datetime.date(2014, 1, 3)
        abd_sr = sun.get_local_sunrise_time(abd)
        abd_ss = sun.get_local_sunset_time(abd)
        print(abd_sr)
        print(abd_ss)
    except SunTimeException as e:
        try:
            print('Error: {0}'.format(e))
        finally:
            e = None
            del e