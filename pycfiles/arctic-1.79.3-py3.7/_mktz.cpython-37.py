# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/date/_mktz.py
# Compiled at: 2019-02-02 17:02:31
# Size of source mod 2**32: 1121 bytes
import dateutil, six, tzlocal

class TimezoneError(Exception):
    pass


def mktz(zone=None):
    """
    Return a new timezone (tzinfo object) based on the zone using the python-dateutil
    package.

    The concise name 'mktz' is for convenient when using it on the
    console.

    Parameters
    ----------
    zone : `String`
           The zone for the timezone. This defaults to local, returning:
           tzlocal.get_localzone()

    Returns
    -------
    An instance of a timezone which implements the tzinfo interface.

    Raises
    - - - - - -
    TimezoneError : Raised if a user inputs a bad timezone name.
    """
    if zone is None:
        zone = tzlocal.get_localzone().zone
    else:
        zone = six.u(zone)
        tz = dateutil.tz.gettz(zone)
        if not tz:
            raise TimezoneError('Timezone "%s" can not be read' % zone)
        tz.zone = hasattr(tz, 'zone') or zone
        for p in dateutil.tz.TZPATHS:
            if zone.startswith(p):
                tz.zone = zone[len(p) + 1:]
                break

    return tz