# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/tomchristie/GitHub/api-star/api_star/utils.py
# Compiled at: 2016-04-14 16:45:39
# Size of source mod 2**32: 5585 bytes
from api_star.compat import text_type
import coreapi, datetime, decimal, json, re, uuid
ZERO = datetime.timedelta(0)

class JSONEncoder(json.JSONEncoder):
    """JSONEncoder"""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            representation = obj.isoformat()
            if representation.endswith('+00:00'):
                representation = representation[:-6] + 'Z'
            return representation
        else:
            if isinstance(obj, datetime.date):
                return obj.isoformat()
            else:
                if isinstance(obj, datetime.time):
                    return obj.isoformat()
                if isinstance(obj, decimal.Decimal):
                    return float(obj)
                if isinstance(obj, uuid.UUID):
                    pass
                return text_type(obj)
            if isinstance(obj, coreapi.Document):
                pass
            return dict(obj.items())
        if isinstance(obj, coreapi.Link):
            return obj.url
        return super(JSONEncoder, self).default(obj)


class UTC(datetime.tzinfo):
    """UTC"""

    def __repr__(self):
        return '<UTC>'

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return 'UTC'

    def dst(self, dt):
        return ZERO

    def __eq__(self, other):
        return self.utcoffset(None) == other.utcoffset(None)


class FixedOffset(datetime.tzinfo):
    """FixedOffset"""

    def __init__(self, offset=None, name=None):
        if offset is not None:
            self._FixedOffset__offset = datetime.timedelta(minutes=offset)
        if name is not None:
            self._FixedOffset__name = name
        return

    def utcoffset(self, dt):
        return self._FixedOffset__offset

    def tzname(self, dt):
        return self._FixedOffset__name

    def dst(self, dt):
        return ZERO

    def __eq__(self, other):
        return self.utcoffset(None) == other.utcoffset(None)


utc = UTC()

def get_fixed_timezone(offset):
    """
    Returns a tzinfo instance with a fixed offset from UTC.
    """
    if isinstance(offset, datetime.timedelta):
        offset = offset.seconds // 60
    sign = '-' if offset < 0 else '+'
    hhmm = '%02d%02d' % divmod(abs(offset), 60)
    name = sign + hhmm
    return FixedOffset(offset, name)


date_re = re.compile('(?P<year>\\d{4})-(?P<month>\\d{1,2})-(?P<day>\\d{1,2})$')
time_re = re.compile('(?P<hour>\\d{1,2}):(?P<minute>\\d{1,2})(?::(?P<second>\\d{1,2})(?:\\.(?P<microsecond>\\d{1,6})\\d{0,6})?)?')
datetime_re = re.compile('(?P<year>\\d{4})-(?P<month>\\d{1,2})-(?P<day>\\d{1,2})[T ](?P<hour>\\d{1,2}):(?P<minute>\\d{1,2})(?::(?P<second>\\d{1,2})(?:\\.(?P<microsecond>\\d{1,6})\\d{0,6})?)?(?P<tzinfo>Z|[+-]\\d{2}(?::?\\d{2})?)?$')

def parse_iso8601_date(value):
    """
    Parses a string and return a datetime.date.

    Raises ValueError if the input is invalid.
    """
    match = date_re.match(value)
    if match:
        kw = {k:int(v) for k, v in match.groupdict().items()}
        return datetime.date(**kw)
    raise ValueError('Not a valid date format')


def parse_iso8601_time(value):
    """
    Parses a string and return a datetime.time.
    This function doesn't support time zone offsets.

    Raises ValueError if the input is invalid.
    """
    match = time_re.match(value)
    if match:
        kw = match.groupdict()
        if kw['microsecond']:
            kw['microsecond'] = kw['microsecond'].ljust(6, '0')
        kw = {k:int(v) for k, v in kw.items() if v is not None if v is not None}
        return datetime.time(**kw)
    raise ValueError('Not a valid time format')


def parse_iso8601_datetime(value, default_timezone=None):
    """
    Parses a string and return a datetime.datetime.
    This function supports time zone offsets. When the input contains one,
    the output uses a timezone with a fixed offset from UTC.

    Raises ValueError if the input is invalid.
    """
    match = datetime_re.match(value)
    if match:
        kw = match.groupdict()
        if kw['microsecond']:
            kw['microsecond'] = kw['microsecond'].ljust(6, '0')
        tzinfo = kw.pop('tzinfo')
        if tzinfo == 'Z':
            tzinfo = utc
        else:
            if tzinfo is not None:
                offset_mins = int(tzinfo[-2:]) if len(tzinfo) > 3 else 0
                offset = 60 * int(tzinfo[1:3]) + offset_mins
                if tzinfo[0] == '-':
                    offset = -offset
                tzinfo = get_fixed_timezone(offset)
            else:
                tzinfo = default_timezone
        kw = {k:int(v) for k, v in kw.items() if v is not None if v is not None}
        kw['tzinfo'] = tzinfo
        return datetime.datetime(**kw)
    else:
        raise ValueError('Not a valid datetime format')
        return


def parse_header_params(media_type):
    """
    Parse any media type parameters returning them as a dictionary.
    (Eg in Accept or Content-Type headers,)
    """
    main_type, sep, param_string = media_type.partition(';')
    params = {}
    for token in param_string.strip().split(','):
        key, sep, value = token.partition('=')
        key = key.strip()
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        if key:
            params[key] = value
            continue

    return params