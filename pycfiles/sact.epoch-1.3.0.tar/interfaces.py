# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vaab/lib/python/site-packages/sact/epoch/interfaces.py
# Compiled at: 2013-01-07 09:29:19
from zope.interface import Interface, Attribute

class ITimeZone(Interface):
    """Standard TimeZone interface as defined in datetime module"""

    def utcoffset(dt):
        """Return offset of local time from UTC, in minutes"""
        pass

    def dst(dt):
        """Return the daylight saving time (DST) adjustment, in minutes"""
        pass

    def tzname(dt):
        """Return the time zone name corresponding to the datetime object dt"""
        pass


class ITime(Interface):
    """Factory to make time object.

    minimal interface

    """

    def now():
        """Return a time object that represent the current time"""
        pass


class IClock(Interface):
    """Factory to make time object.

    minimal interface

    """

    def time():
        """Return a time object that represent the current time"""
        pass


class IManageableClock(IClock):
    is_running = Attribute('Freeze the return result of now() command')

    def set(date):
        """Set the result of now() command to date"""
        pass

    def stop():
        """Freeze the return result of now() command"""
        pass

    def start():
        """Unfreeze the return result of now() command"""
        pass

    def wait(timelapse=None, days=0, hours=0, minutes=0, seconds=0):
        """Shortcut to alter_now relative

        Should accept negative value also.

        """
        pass