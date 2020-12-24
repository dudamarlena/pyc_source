# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/datetime.py
# Compiled at: 2017-06-28 12:42:21
# Size of source mod 2**32: 2887 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import time
from datetime import datetime, timezone, timedelta
from wasp_general.verify import verify_type

def local_tz():
    """ Return current system timezone shift from UTC

        :return: datetime.timezone
        """
    return timezone(timedelta(0, time.timezone * -1))


@verify_type(dt=(datetime, None), local_value=bool)
def utc_datetime(dt=None, local_value=True):
    """ Convert local datetime and/or datetime without timezone information to UTC datetime with timezone
        information.

        :param dt: local datetime to convert. If is None, then system datetime value is used
        :param local_value: whether dt is a datetime in system timezone or UTC datetime without timezone information
        :return: datetime in UTC with tz set
        """
    if dt is None:
        return datetime.now(tz=timezone.utc)
    result = dt
    if result.utcoffset() is None:
        if local_value is False:
            return result.replace(tzinfo=timezone.utc)
        result = result.replace(tzinfo=local_tz())
    return result.astimezone(timezone.utc)


@verify_type(dt=(datetime, None), utc_value=bool)
def local_datetime(dt=None, utc_value=True):
    """ Convert UTC datetime and/or datetime without timezone information to local datetime with timezone
        information

        :param dt: datetime in UTC to convert. If is None, then system datetime value is used
        :param utc_value: whether dt is a datetime in UTC or in system timezone without timezone information
        :return: datetime for system (local) timezone with tz set
        """
    if dt is None:
        return datetime.now(tz=local_tz())
    result = dt
    if result.utcoffset() is None:
        if utc_value is False:
            return result.replace(tzinfo=local_tz())
        result = result.replace(tzinfo=timezone.utc)
    return result.astimezone(local_tz())