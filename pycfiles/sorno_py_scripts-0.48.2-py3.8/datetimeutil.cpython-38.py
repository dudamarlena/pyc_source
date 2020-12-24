# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sorno/datetimeutil.py
# Compiled at: 2020-03-16 00:44:32
# Size of source mod 2**32: 5265 bytes
"""datetimeutil converts between different datetime related objects.

In this module, make sure we don't use the tzinfo
parameter in the constructor datetime.datetime. Instead,
always gets a timezone from pytz, then do localize (and
normalize after that).
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime, re, time
from dateutil import parser as dateutilparser
import pytz, six, tzlocal
ISO_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
ISO_FORMAT_WITH_TZ_NAME = '%Y-%m-%dT%H:%M:%S%z%Z'
LOCAL_TIMEZONE = tzlocal.get_localzone()
_mst_timezone = pytz.timezone('US/Mountain')
GO_REFERENCE_TIME = _mst_timezone.normalize(_mst_timezone.localize(datetime.datetime(2006, 1, 2, 15, 4, 5)))
TIMESTAMP_REGEX = re.compile('((?<=\\D)|^)(\\d{10,19})((?=\\D)|$)')
_timestamp_units = [
 's', 'ms', 'us', 'ns']

def real_localize(dt, tz):
    """Attach timezone info to a datetime object.

    This is basically tz.normalize(tz.localize(dt))

    Args:
        dt: A datetime.
        tz: A pytz timezone.

    Returns:
        A datetime object which is a clone of the given dt, with the given
        timezone info attached.
    """
    return tz.normalize(tz.localize(dt))


def convert_timezone(dt, tz=LOCAL_TIMEZONE):
    """Converts a datetime object to a specific timezone.

    By default, the datetime object is converted into local timezone."""
    return tz.normalize(dt.astimezone(tz))


def datetime_to_timestamp(dt):
    """Converts datetime to a UNIX timestamp.

    Args:
        dt: A datetime. The datetime to be converted.

    Returns:
        An integer that represents the converted UNIX timestamp in seconds.
    """
    dt = convert_timezone(dt, tz=LOCAL_TIMEZONE)
    return time.mktime(dt.timetuple())


def timestamp_to_local_datetime(timestamp):
    """Converts timestamp to a datetime with local timezone info.

    Args:
        timestamp: An int. The UNIX timestamp in seconds to be converted.

    Returns:
        The converted datetime object with local timezone info.
    """
    dt = datetime.datetime.fromtimestamp(timestamp, LOCAL_TIMEZONE)
    return dt


def number_to_local_datetime(number):
    """Guesses the units of a timestamp.

    Args:
        number: An int. The number that is assumed to be a UNIX timestamp
            without units specified.

    Returns:
        A tuple of (datetime, str). The first element is the datetime object
        for the timestamp with local one info. The second element is the guessed
        unit, which can be s, ms, us, or ns. Raise ValueError if a valid
        conversion cannot be done.
    """
    i = 0
    n = number
    while n > 10000000000:
        n /= 1000
        i += 1
        if i >= len(_timestamp_units):
            raise ValueError('number %s is too big' % number)

    dt = datetime.datetime.fromtimestamp(n, LOCAL_TIMEZONE)
    return (dt, _timestamp_units[i])


_COMMON_DATETIME_FORMATS_AND_LAMBDA = (
 (
  '%Y-%m-%dT%H:%M:%S.%fZ',
  lambda dt: dt.replace(tzinfo=(pytz.utc)).astimezone(LOCAL_TIMEZONE)),)

def guess_local_datetime--- This code section failed: ---

 L. 149         0  LOAD_GLOBAL              _COMMON_DATETIME_FORMATS_AND_LAMBDA
                2  GET_ITER         
                4  FOR_ITER             62  'to 62'
                6  UNPACK_SEQUENCE_2     2 
                8  STORE_FAST               'dt_format'
               10  STORE_FAST               'func'

 L. 150        12  SETUP_FINALLY        36  'to 36'

 L. 151        14  LOAD_FAST                'func'
               16  LOAD_GLOBAL              datetime
               18  LOAD_ATTR                datetime
               20  LOAD_METHOD              strptime
               22  LOAD_FAST                's'
               24  LOAD_FAST                'dt_format'
               26  CALL_METHOD_2         2  ''
               28  CALL_FUNCTION_1       1  ''
               30  POP_TOP          
               32  POP_BLOCK        
               34  JUMP_BACK             4  'to 4'
             36_0  COME_FROM_FINALLY    12  '12'

 L. 152        36  DUP_TOP          
               38  LOAD_GLOBAL              ValueError
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    58  'to 58'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 153        50  POP_EXCEPT       
               52  JUMP_BACK             4  'to 4'
               54  POP_EXCEPT       
               56  JUMP_BACK             4  'to 4'
             58_0  COME_FROM            42  '42'
               58  END_FINALLY      
               60  JUMP_BACK             4  'to 4'

 L. 155        62  LOAD_GLOBAL              dateutilparser
               64  LOAD_METHOD              parse
               66  LOAD_FAST                's'
               68  CALL_METHOD_1         1  ''
               70  STORE_FAST               'dt'

 L. 156        72  LOAD_FAST                'dt'
               74  LOAD_ATTR                tzinfo
               76  POP_JUMP_IF_FALSE    88  'to 88'

 L. 157        78  LOAD_FAST                'dt'
               80  LOAD_METHOD              astimezone
               82  LOAD_GLOBAL              LOCAL_TIMEZONE
               84  CALL_METHOD_1         1  ''
               86  RETURN_VALUE     
             88_0  COME_FROM            76  '76'

 L. 159        88  LOAD_GLOBAL              LOCAL_TIMEZONE
               90  LOAD_METHOD              localize
               92  LOAD_FAST                'dt'
               94  CALL_METHOD_1         1  ''
               96  RETURN_VALUE     

Parse error at or near `POP_EXCEPT' instruction at offset 54


def strftime(format, mixed, localize=False):
    """Formats a time to a string.

    Just like time.strftime
    (https://docs.python.org/2/library/time.html#time.strftime) but this function
    can take different types of "time" object. It can take a timestamp in
    seconds, a datetime object, or a struct_time
    (https://docs.python.org/2/library/time.html#time.struct_time).

    If mixed is a datetime with a timezone, the result of strftime
    """
    dt = None
    if type(mixed) in six.integer_types or type(mixed) == float:
        dt = timestamp_to_local_datetime(mixed)
    else:
        if type(mixed) == datetime.datetime:
            dt = mixed
        else:
            if type(mixed) == time.struct_time:
                dt = timestamp_to_local_datetime(time.mktime(mixed))
    return dt.strftime(format)