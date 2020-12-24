# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyfva/logger.py
# Compiled at: 2020-01-01 14:37:19
# Size of source mod 2**32: 2409 bytes
import logging, datetime, decimal, json, uuid
logger = logging.getLogger('pyfva')

def _get_duration_components(duration):
    days = duration.days
    seconds = duration.seconds
    microseconds = duration.microseconds
    minutes = seconds // 60
    seconds = seconds % 60
    hours = minutes // 60
    minutes = minutes % 60
    return (
     days, hours, minutes, seconds, microseconds)


def duration_iso_string(duration):
    if duration < datetime.timedelta(0):
        sign = '-'
        duration *= -1
    else:
        sign = ''
    days, hours, minutes, seconds, microseconds = _get_duration_components(duration)
    ms = '.{:06d}'.format(microseconds) if microseconds else ''
    return '{}P{}DT{:02d}H{:02d}M{:02d}{}S'.format(sign, days, hours, minutes, seconds, ms)


class DateTimeJSONEncoder(json.JSONEncoder):
    """DateTimeJSONEncoder"""

    def default(self, o):
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        else:
            if isinstance(o, datetime.date):
                return o.isoformat()
            else:
                if isinstance(o, datetime.time):
                    if o.utcoffset() is not None:
                        raise ValueError("JSON can't represent timezone-aware times.")
                    r = o.isoformat()
                    if o.microsecond:
                        r = r[:12]
                    return r
                else:
                    if isinstance(o, datetime.timedelta):
                        return duration_iso_string(o)
                    if isinstance(o, (decimal.Decimal, uuid.UUID)):
                        return str(o)
                if isinstance(o, Exception):
                    return str(o)
            return super().default(o)


def info(data):
    data['sector'] = 'pyfva'
    logger.info(json.dumps(data, cls=DateTimeJSONEncoder))


def warning(data):
    data['sector'] = 'pyfva'
    logger.warning(json.dumps(data, cls=DateTimeJSONEncoder))


def debug(data):
    data['sector'] = 'pyfva'
    logger.debug(json.dumps(data, cls=DateTimeJSONEncoder))


def error(data):
    data['sector'] = 'pyfva'
    logger.error(json.dumps(data, cls=DateTimeJSONEncoder))