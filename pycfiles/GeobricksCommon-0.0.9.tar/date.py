# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/geobricks/geobricks/server/geobricks_common/geobricks_common/core/date.py
# Compiled at: 2015-06-16 09:19:26
import calendar, datetime
from geobricks_common.core.log import logger
log = logger(__file__)

def get_daterange(date):
    """
    :param date: format "%dmy-%dmy" or "dmy" or "my" or "y"
    :return:
    """
    log.info(date)
    date = date.split('-')
    from_date = None
    to_date = None
    try:
        try:
            if len(date) == 1:
                date = date[0]
                if len(date) == 4:
                    from_date, to_date = get_range_dates_metadata_yearly(date)
                if len(date) == 6:
                    from_date, to_date = get_range_dates_metadata_montly(date)
                if len(date) == 8:
                    from_date, to_date = get_range_dates_metadata_daily(date)
            elif len(date) == 2:
                from_d = date[0]
                to_d = date[1]
                if len(from_d) == 4:
                    from_date, to_date = get_range_from_to_dates_metadata_yearly(from_d, to_d)
                if len(from_d) == 6:
                    from_date, to_date = get_range_from_to_dates_metadata_monthly(from_d, to_d)
                if len(from_d) == 8:
                    from_date, to_date = get_range_from_to_dates_metadata_daily(from_d, to_d)
        except Exception as e:
            log.error(e)

    finally:
        return (
         from_date, to_date)


def get_range_dates_metadata_yearly(year):
    """
    :param my: monthyear date (i.e. 2015)
    :return: the from and to date in milliseconds (i.e. 01-01-2015 to 31-12-3015
    """
    from_date = datetime.datetime(int(year), int(1), 1)
    last_day = calendar.monthrange(int(year), int(12))[1]
    to_date = datetime.datetime(int(year), int(12), last_day)
    from_date_result = calendar.timegm(from_date.timetuple()) * 1000
    to_date_result = calendar.timegm(to_date.timetuple()) * 1000
    return (from_date_result, to_date_result)


def get_range_dates_metadata_montly(my):
    """
    :param my: monthyear date (i.e. 012015 - january 2015)
    :return: the from and to date in milliseconds
    """
    year = int(my[:4])
    month = int(my[4:6])
    from_date = datetime.datetime(int(year), month, 1)
    last_day = calendar.monthrange(int(year), month)[1]
    to_date = datetime.datetime(int(year), int(month), last_day)
    from_date_result = calendar.timegm(from_date.timetuple()) * 1000
    to_date_result = calendar.timegm(to_date.timetuple()) * 1000
    return (from_date_result, to_date_result)


def get_range_dates_metadata_daily(dmy):
    """
    The from and to day returned are the same in this case
    :param dmy: daymonthyear date (i.e. 01012015 - first january 2015)
    :return:
    """
    year = int(dmy[:4])
    month = int(dmy[4:6])
    day = int(dmy[6:8])
    from_date = datetime.datetime(int(year), month, day)
    from_date_result = calendar.timegm(from_date.timetuple()) * 1000
    return (from_date_result, from_date_result)


def get_range_from_to_dates_metadata_yearly(from_y, to_y):
    """
    :param my: monthyear date (i.e. 2015)
    :return: the from and to date in milliseconds (i.e. 01-01-2015 to 31-12-3015
    """
    from_date = datetime.datetime(int(from_y), int(1), 1)
    last_day = calendar.monthrange(int(to_y), int(12))[1]
    to_date = datetime.datetime(int(to_y), int(12), last_day)
    from_date_result = calendar.timegm(from_date.timetuple()) * 1000
    to_date_result = calendar.timegm(to_date.timetuple()) * 1000
    return (from_date_result, to_date_result)


def get_range_from_to_dates_metadata_monthly(from_my, to_my):
    """
    :param my: monthyear date (i.e. 2015)
    :return: the from and to date in milliseconds (i.e. 01-01-2015 to 31-12-3015
    """
    from_year = int(from_my[:4])
    from_month = int(from_my[4:6])
    to_year = int(to_my[:4])
    to_month = int(to_my[4:6])
    from_date = datetime.datetime(int(from_year), from_month, 1)
    last_day = calendar.monthrange(int(to_year), to_month)[1]
    to_date = datetime.datetime(int(to_year), int(to_month), last_day)
    from_date_result = calendar.timegm(from_date.timetuple()) * 1000
    to_date_result = calendar.timegm(to_date.timetuple()) * 1000
    return (from_date_result, to_date_result)


def get_range_from_to_dates_metadata_daily(from_dmy, to_dmy):
    """
    The from and to day returned are the same in this case
    :param dmy: daymonthyear date (i.e. 01012015 - first january 2015)
    :return:
    """
    from_year = int(from_dmy[:4])
    from_day = int(from_dmy[4:6])
    from_month = int(from_dmy[6:8])
    to_year = int(to_dmy[:4])
    to_month = int(to_dmy[4:6])
    to_day = int(to_dmy[6:8])
    from_date = datetime.datetime(int(from_year), from_month, from_day)
    to_date = datetime.datetime(int(to_year), to_month, to_day)
    from_date_result = calendar.timegm(from_date.timetuple()) * 1000
    to_date_result = calendar.timegm(to_date.timetuple()) * 1000
    return (from_date_result, from_date_result)


def day_of_the_year_to_date(day, year):
    """
    Convert a day of an year to a date
    @param day: day of the year
    @type day: str | int
    @param year: year of reference
    @type year: str | int
    @return: the date of the day/year i.e. "2012-01-20"
    """
    year = year if type(year) is str else str(year)
    day = day if type(day) is str else str(day)
    day = '00' + day if len(day) == 1 else day
    day = '0' + day if len(day) == 2 else day
    first_of_year = datetime.datetime(int(year), 1, 1).replace(month=1, day=1)
    ordinal = first_of_year.toordinal() - 1 + int(day)
    return datetime.date.fromordinal(ordinal)