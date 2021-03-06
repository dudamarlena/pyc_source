# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/date.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 10795 bytes
__doc__ = 'PyAMS_utils.date module\n\nThis module provides several functions concerning conversion, parsing and formatting of\ndates and datetimes.\n'
from datetime import datetime
from zope.datetime import parseDatetimetz
from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import Interface
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.tales import ITALESExtension
from pyams_utils.request import check_request
from pyams_utils.timezone import gmtime, tztime
__docformat__ = 'restructuredtext'
from pyams_utils import _

def unidate(value):
    """Get specified date converted to unicode ISO format

    Dates are always assumed to be stored in GMT timezone

    :param date value: input date to convert to unicode
    :return: unicode; input date converted to unicode

    >>> from datetime import datetime
    >>> from pyams_utils.date import unidate
    >>> value = datetime(2016, 11, 15, 10, 13, 12)
    >>> unidate(value)
    '2016-11-15T10:13:12+00:00'
    >>> unidate(None) is None
    True
    """
    if value is not None:
        value = gmtime(value)
        return value.isoformat('T')


def parse_date(value):
    """Get date specified in unicode ISO format to Python datetime object

    Dates are always assumed to be stored in GMT timezone

    :param str value: unicode date to be parsed
    :return: datetime; the specified value, converted to datetime

    >>> from pyams_utils.date import parse_date
    >>> parse_date('2016-11-15T10:13:12+00:00')
    datetime.datetime(2016, 11, 15, 10, 13, 12, tzinfo=<StaticTzInfo 'GMT'>)
    >>> parse_date(None) is None
    True
    """
    if value is not None:
        return gmtime(parseDatetimetz(value))


def date_to_datetime(value):
    """Get datetime value converted from a date or datetime object

    :param date/datetime value: a date or datetime value to convert
    :return: datetime; input value converted to datetime

    >>> from datetime import date, datetime
    >>> from pyams_utils.date import date_to_datetime
    >>> value = date(2016, 11, 15)
    >>> date_to_datetime(value)
    datetime.datetime(2016, 11, 15, 0, 0)
    >>> value = datetime(2016, 11, 15, 10, 13, 12)
    >>> value
    datetime.datetime(2016, 11, 15, 10, 13, 12)
    >>> date_to_datetime(value) is value
    True
    >>> date_to_datetime(None) is None
    True
    """
    if not value:
        return
    if isinstance(value, datetime):
        return value
    return datetime(value.year, value.month, value.day)


SH_DATE_FORMAT = _('%d/%m/%Y')
SH_DATETIME_FORMAT = _('%d/%m/%Y - %H:%M')
EXT_DATE_FORMAT = _('on %d/%m/%Y')
EXT_DATETIME_FORMAT = _('on %d/%m/%Y at %H:%M')

def format_date(value, format_string=EXT_DATE_FORMAT, request=None):
    """Format given date with the given format

    :param datetime value: the value to format
    :param str format_string: a format string to use by `strftime` function
    :param request: the request from which to extract localization info for translation
    :return: str; input datetime converted to given format

    >>> from datetime import datetime
    >>> from pyams_utils.date import format_date, SH_DATE_FORMAT
    >>> value = datetime(2016, 11, 15, 10, 13, 12)
    >>> format_date(value)
    'on 15/11/2016'
    >>> format_date(value, SH_DATE_FORMAT)
    '15/11/2016'
    >>> format_date(None)
    '--'
    """
    if not value:
        return '--'
    if request is None:
        request = check_request()
    localizer = request.localizer
    return datetime.strftime(tztime(value), localizer.translate(format_string))


def format_datetime(value, format_string=EXT_DATETIME_FORMAT, request=None):
    """Format given datetime with the given format including time

    :param datetime value: the value to format
    :param str format_string: a format string to use by `strftime` function
    :param request: request; the request from which to extract localization info for translation
    :return: str; input datetime converted to given format

    >>> from datetime import datetime
    >>> from pyams_utils.date import format_datetime, SH_DATETIME_FORMAT
    >>> value = datetime(2016, 11, 15, 10, 13, 12)
    >>> format_datetime(value)
    'on 15/11/2016 at 10:13'
    >>> format_datetime(value, SH_DATETIME_FORMAT)
    '15/11/2016 - 10:13'
    >>> format_datetime(None)
    '--'
    """
    return format_date(value, format_string, request)


def get_age(value, request=None):
    """Get 'human' age of a given datetime (including timezone) compared to current datetime
    (in UTC)

    :param datetime value: input datetime to be compared with current datetime
    :return: str; the delta value, converted to months, weeks, days, hours or minutes

    >>> from datetime import datetime, timedelta
    >>> from pyams_utils.date import get_age
    >>> now = datetime.utcnow()
    >>> get_age(now)
    'less than 5 minutes ago'
    >>> get_age(now - timedelta(minutes=10))
    '10 minutes ago'
    >>> get_age(now - timedelta(hours=2))
    '2 hours ago'
    >>> get_age(now - timedelta(days=1))
    'yesterday'
    >>> get_age(now - timedelta(days=2))
    'the day before yesterday'
    >>> get_age(now - timedelta(days=4))
    '4 days ago'
    >>> get_age(now - timedelta(weeks=2))
    '2 weeks ago'
    >>> get_age(now - timedelta(days=80))
    '3 months ago'
    >>> get_age(None)
    '--'
    """
    if not value:
        return '--'
    if request is None:
        request = check_request()
    translate = request.localizer.translate
    now = gmtime(datetime.utcnow())
    delta = now - gmtime(value)
    if delta.days > 60:
        result = translate(_('%d months ago')) % int(round(delta.days * 1.0 / 30))
    else:
        if delta.days > 10:
            result = translate(_('%d weeks ago')) % int(round(delta.days * 1.0 / 7))
        else:
            if delta.days > 2:
                result = translate(_('%d days ago')) % delta.days
            else:
                if delta.days == 2:
                    result = translate(_('the day before yesterday'))
                else:
                    if delta.days == 1:
                        result = translate(_('yesterday'))
                    else:
                        hours = int(round(delta.seconds * 1.0 / 3600))
                        if hours > 1:
                            result = translate(_('%d hours ago')) % hours
                        else:
                            if delta.seconds > 300:
                                result = translate(_('%d minutes ago')) % int(round(delta.seconds * 1.0 / 60))
                            else:
                                result = translate(_('less than 5 minutes ago'))
    return result


def get_duration(first, last=None, request=None):
    """Get 'human' delta as string between two dates

    :param datetime first: start date
    :param datetime last: end date, or current date (in UTC) if None
    :param request: the request from which to extract localization infos
    :return: str; approximate delta between the two input dates

    >>> from datetime import datetime
    >>> from pyams_utils.date import get_duration
    >>> from pyramid.testing import DummyRequest
    >>> request = DummyRequest()
    >>> date1 = datetime(2015, 1, 1)
    >>> date2 = datetime(2014, 3, 1)
    >>> get_duration(date1, date2, request)
    '10 months'

    Dates order is not important:

    >>> get_duration(date2, date1, request)
    '10 months'
    >>> date2 = datetime(2014, 11, 10)
    >>> get_duration(date1, date2, request)
    '7 weeks'
    >>> date2 = datetime(2014, 12, 26)
    >>> get_duration(date1, date2, request)
    '6 days'

    For durations lower than 2 days, duration also display hours:

    >>> date1 = datetime(2015, 1, 1)
    >>> date2 = datetime(2015, 1, 2, 15, 10, 0)
    >>> get_duration(date1, date2, request)
    '1 day and 15 hours'
    >>> date2 = datetime(2015, 1, 2)
    >>> get_duration(date1, date2, request)
    '24 hours'
    >>> date2 = datetime(2015, 1, 1, 13, 12)
    >>> get_duration(date1, date2, request)
    '13 hours'
    >>> date2 = datetime(2015, 1, 1, 1, 15)
    >>> get_duration(date1, date2, request)
    '75 minutes'
    >>> date2 = datetime(2015, 1, 1, 0, 0, 15)
    >>> get_duration(date1, date2, request)
    '15 seconds'
    >>> now = datetime.utcnow()
    >>> delta = now - date1
    >>> get_duration(date1, None, request) == '%d months' % int(round(delta.days * 1.0 / 30))
    True
    """
    if last is None:
        last = datetime.utcnow()
    assert isinstance(first, datetime) and isinstance(last, datetime)
    if request is None:
        request = check_request()
    translate = request.localizer.translate
    first, last = min(first, last), max(first, last)
    delta = last - first
    if delta.days > 60:
        result = translate(_('%d months')) % int(round(delta.days * 1.0 / 30))
    else:
        if delta.days > 10:
            result = translate(_('%d weeks')) % int(round(delta.days * 1.0 / 7))
        else:
            if delta.days >= 2:
                result = translate(_('%d days')) % delta.days
            else:
                hours = int(round(delta.seconds * 1.0 / 3600))
                if delta.days == 1:
                    if hours == 0:
                        result = translate(_('24 hours'))
                    else:
                        result = translate(_('%d day and %d hours')) % (delta.days, hours)
                else:
                    if hours > 2:
                        result = translate(_('%d hours')) % hours
                    else:
                        minutes = int(round(delta.seconds * 1.0 / 60))
                        if minutes > 2:
                            result = translate(_('%d minutes')) % minutes
                        else:
                            result = translate(_('%d seconds')) % delta.seconds
    return result


@adapter_config(name='timestamp', context=(Interface, Interface, Interface), provides=ITALESExtension)
class TimestampTalesAdapter(ContextRequestViewAdapter):
    """TimestampTalesAdapter"""

    def render(self, context=None, formatting=None):
        """Render TALES extension"""
        if context is None:
            context = self.request.context
        if formatting == 'iso':
            format_func = datetime.isoformat
        else:
            format_func = datetime.timestamp
        zdc = IZopeDublinCore(context, None)
        if zdc is not None:
            return format_func(tztime(zdc.modified))
        return format_func(tztime(datetime.utcnow()))