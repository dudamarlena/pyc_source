# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/cloudbackup/utils/tz.py
# Compiled at: 2017-05-12 15:59:18
"""
TimeZone Utility
"""
from __future__ import print_function
import logging, pytz, tzlocal, tzlocal.windows_tz

def get_timezone(WindowsZoneName=True):
    """
    Get the TimeZone Name

    if WindowsZoneName is True, then it returns the name used by the Microsoft Windows Platform
    otherwise it returns the Olsen name (used by all other platforms)

    Note: this needs to get tested on Windows
    """
    log = logging.getLogger(__name__)
    localzone = tzlocal.get_localzone()
    if localzone is None:
        log.error('tzlocal did not provide a time zone configuration')
        raise pytz.UnknownTimeZoneError('Cannot find  any time zone configuration')
    else:
        olsen_name = localzone.zone
        if WindowsZoneName:
            try:
                windows_name = tzlocal.windows_tz.tz_win[olsen_name]
                log.info('Mappped Olsen Time Zone Name (' + olsen_name + ') to Windows Time Zone Name (' + windows_name + ')')
                return windows_name
            except LookupError:
                log.error('Unable to map Olsen Time Zone Name (' + olsen_name + ') to Windows Time Zone Name')
                return 'Unknown'

        else:
            return olsen_name
    return


def get_v1_timezone_name_list():
    return sorted(tzlocal.windows_tz.win_tz.keys())


def get_v2_timezone_name_list():
    return sorted(tzlocal.windows_tz.tz_win.keys())