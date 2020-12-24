# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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