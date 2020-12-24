# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/stock/util.py
# Compiled at: 2017-01-31 01:11:19
# Size of source mod 2**32: 3577 bytes
import io, zipfile, csv, time, calendar, datetime, pandas as pd
from dateutil import relativedelta
from . import config as C

def to_ja(date):
    japan = date + datetime.timedelta(hours=9)
    return int(japan.strftime('%s')) * 1000


def series_to_json(series, japan=True):
    return list([to_ja(a), b] for a, b in zip(series.index.values.tolist(), series.values.tolist()) if not pd.isnull(b))


def df_to_series(df, color=None, type=None):
    series = []
    if isinstance(df, pd.core.series.Series):
        return [{'name': df.name, 'data': series_to_json(df)}]
    for index, (name, data) in enumerate(df_to_json(df).items()):
        series.append({'name': name, 
         'data': data})

    return series


def df_to_json(df):
    d = {}
    for key, val in df.items():
        d[key] = series_to_json(val)

    return d


class DateRange(object):

    def __init__(self, start=None, end=None):
        if isinstance(end, str):
            end = str2date(start)
        if isinstance(start, str):
            start = str2date(start)
        if end is None:
            end = datetime.date.today()
        if start is None:
            start = end - relativedelta.relativedelta(days=C.DEFAULT_DAYS_PERIOD)
        self.end = end
        self.start = start

    def to_dict(self):
        return {'start': str(self.start), 'end': str(self.end)}

    def to_short_dict(self):
        return {'sy': self.start.year, 
         'sm': self.start.month, 
         'sd': self.start.day, 
         'ey': self.end.year, 
         'em': self.end.month, 
         'ed': self.end.day}


def dict_inverse(dct):
    return {v:k for k, v in dct.items()}


def str2date(datestr):
    if datestr:
        t = time.strptime(datestr, '%Y-%m-%d')
        return datetime.date.fromtimestamp(time.mktime(t))


def str_to_date(s):
    import datetime
    for fmt in C.DATE_FORMATS:
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except:
            pass

    else:
        raise ValueError


def read_csv_zip(fn, content):
    ls = []
    with zipfile.ZipFile(io.BytesIO(content)) as (fh):
        for f in fh.infolist():
            csv_fh = io.StringIO(fh.open(f.filename).read().decode())
            for row in csv.reader(csv_fh):
                ls.append(fn(row))

    return ls


def last_date():
    """株の最後の日を返す"""
    now = datetime.datetime.today() + relativedelta.relativedelta(hours=9)
    weekday = now.weekday()
    if weekday in [calendar.SUNDAY, calendar.SATURDAY]:
        dt = now + relativedelta.relativedelta(weekday=relativedelta.FR(-1))
    else:
        dt = now - relativedelta.relativedelta(days=1)
    return dt.date()


def fix_value(value, split_stock_dates, today=None):
    """
    Need to convert by split stock dates
    """
    for date in split_stock_dates:
        if today < date.date:
            value *= date.from_number / float(date.to_number)

    return value