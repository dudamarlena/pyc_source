# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\utils\datetime_func.py
# Compiled at: 2018-08-27 20:45:27
# Size of source mod 2**32: 8322 bytes
from datetime import date
from datetime import datetime
from datetime import timedelta
from functools import lru_cache
import numpy as np

@lru_cache(maxsize=None)
def to_datetime(var):
    """
    将整形转变为datetime类型
    :param var: int/str, 形如：20120101
    :return: datetime,
    """
    try:
        test_date_time = datetime.strptime(str(var), '%Y%m%d')
    except Exception:
        raise ValueError('input date is illegal, expect like:20170506')

    return test_date_time


def to_int_now_date():
    """
     获取当前日期的int值，如: 20180115
    """
    return datetime.now().strftime('%Y%m%d')


@lru_cache(maxsize=None)
def check_begindate_enddate(begin, end):
    """
    一、输入的整形数据是否符合datatime的要求
    二、判断输入的时间是否在可控区间内
    三、结束时间不能小于开始时间
    :param begin: int/str, like: 20120119
    :param end: int/str, like:20120120
    :return: None
    """
    _b = to_datetime(begin)
    _e = to_datetime(end)
    MIN_TIME = datetime(1900, 1, 1)
    NOW_TIME = datetime.now()
    if MIN_TIME < _b < NOW_TIME:
        if MIN_TIME < _e < NOW_TIME:
            if _b > _e:
                raise ValueError('start date {} > stop date {}'.format(_b, _e))
    else:
        raise ValueError('Expect date from 1900 to now')


def matlab_float_time_to_datetime(ts):
    """
    :param ts: int，float, sequence, matlab类型的浮点数
    :return: datetime or datetime list
    """
    if isinstance(ts, (int, float)):
        return timedelta(days=ts - 367) + datetime(1, 1, 1)
    else:
        ts = np.asarray(ts)
        return [timedelta(days=item - 367) + datetime(1, 1, 1) for item in ts]


def matlab_float_time_to_py_str(ts, p):
    """将matlab浮点型时间转为python字符串型时间，p表示时间格式,比如:%Y-%m-%d %H:%M:%S"""
    if isinstance(ts, (int, float)):
        dt = matlab_float_time_to_datetime(ts)
        return dt.strftime(p)
    else:
        ts = np.asarray(ts)
        dts = matlab_float_time_to_datetime(ts)
        return [dt.strftime(p) for dt in dts]


def matlab_float_time_to_str_date(ts):
    """
    :param ts: int，float, sequence, matlab类型的浮点数
    :return: str or str list，日期格式：20180328 
    """
    if isinstance(ts, (int, float)):
        dt = matlab_float_time_to_datetime(ts)
        return '%4d%02d%02d' % (dt.year, dt.month, dt.day)
    else:
        ts = np.asarray(ts)
        dts = matlab_float_time_to_datetime(ts)
        return ['%4d%02d%02d' % (dt.year, dt.month, dt.day) for dt in dts]


def matlab_float_time_to_str_datetime(ts):
    """
    :param ts: int，float, sequence, matlab类型的浮点数
    :return: str or str list，日期格式：2018-03-28 11:06:20 
    """
    return matlab_float_time_to_py_str(ts, '%Y-%m-%d %H:%M:%S')


def matlab_float_time_to_int_date(ts):
    """
    :param t: 当t 为 int, float 时，返回int。当t为list.tuple,numpy.ndarry时，返回numpy.ndarry
    :return: int or numpy.ndarray, 日期格式：20180328
    """
    result = np.array([])
    if isinstance(ts, (int, float)):
        dt = matlab_float_time_to_datetime(ts)
        return dt.year * 10000 + dt.month * 100 + dt.day
    else:
        ts = np.asarray(ts)
        row = ts.shape[0]
        dts = matlab_float_time_to_datetime(ts)
        temp = [dt.year * 10000 + dt.month * 100 + dt.day for dt in dts.flatten()]
        return temp


def int_date_predate(intdate):
    """
    计算 intdate 前一天 date 
    :param intdate: int，形如:20180302
    :return: int, 返回20180302前一天日期: 20180301
    """
    strdate = str(intdate)
    if not isinstance(intdate, int) or len(strdate) < 8:
        raise ValueError('Input intdate param error,expect like: 20180302')
    y = int(strdate[:4])
    m = int(strdate[4:6])
    d = int(strdate[6:8])
    curdt = datetime(year=y, month=m, day=d)
    predt = curdt - timedelta(days=1)
    intpredate = int('%04d%02d%02d' % (predt.year, predt.month, predt.day))
    return intpredate


def change_to_y_M_D_H_m_s(test_array, istick=False):
    """
    将int型日期切割为由年，月，日，小时，分钟，秒组成的numpy.array
    :param test_array: sequence,
    :param istick: bool, 是否为tick
    :return: numpy.array
    """
    year_array = list()
    month_array = list()
    day_array = list()
    hour_array = list()
    min_array = list()
    second_array = list()
    for i in test_array:
        if i == 0:
            year_array.append(0)
            month_array.append(0)
            day_array.append(0)
            hour_array.append(0)
            min_array.append(0)
            second_array.append(0)
        else:
            temp = timedelta(days=i - 367) + datetime(1, 1, 1)
            year = temp.year
            year_array.append(year)
            month = temp.month
            month_array.append(month)
            day = temp.day
            day_array.append(day)
            hour = temp.hour
            hour_array.append(hour)
            minute = temp.minute
            second = temp.second
            if not istick:
                if second > 58:
                    second = 0
                    minute = minute + 1
                min_array.append(minute)
                second_array.append(second)

    temp_array1 = np.array(year_array, dtype=np.double) * 10000000000000 + np.array(month_array, dtype=np.double) * 100000000000 + np.array(day_array, dtype=np.double) * 1000000000
    temp_array2 = np.array(hour_array, dtype=np.double) * 10000000 + np.array(min_array, dtype=np.double) * 100000 + np.array(second_array, dtype=np.double) * 1000
    temp_array = temp_array1 + temp_array2
    return temp_array


@lru_cache(None)
def int_date_to_ordinal(d):
    """
    将日期转为matlab的datenum,也就是 Gregorian Calendar日历
    
    :param d: int,合法日期，形如：20180116 
    :return: int
    """
    d_s = str(d)
    dt = date(int(d_s[:4]), int(d_s[4:6]), int(d_s[6:]))
    return date.toordinal(dt) + 366


@lru_cache(None)
def ordinal_to_int_date(d):
    """
    将Gregorian Calendar日历转为int date

    :param d: int,合法日期，形如：737070 
    :return: int
    """
    return int(date.fromordinal(d - 366).strftime('%Y%m%d'))


def weekday(data):
    """ 
    data: matlab浮点型日期    
    若为浮点数，返回单个值
    若为numpy.ndarray 结构,将会展开为一维结构,返回一维结构。
    """
    if isinstance(data, float):
        d = timedelta(days=data - 367) + datetime(1, 1, 1)
        return d.weekday()
    else:
        result = data.flatten()
        for i, r in enumerate(result):
            d = timedelta(days=r - 367) + datetime(1, 1, 1)
            result[i] = d.weekday()

        return result


def month(data):
    """ 
    data: matlab浮点型日期    
    若为浮点数，返回单个值
    若为numpy.ndarray 结构,将会展开为一维结构,返回一维结构。
    """
    if isinstance(data, float):
        d = timedelta(days=data - 367) + datetime(1, 1, 1)
        return d.month
    result = data.flatten()
    for i, r in enumerate(result):
        d = timedelta(days=r - 367) + datetime(1, 1, 1)
        result[i] = d.month

    return result


def year(data):
    """ 
    data: matlab浮点型日期    
    若为浮点数，返回单个值
    若为numpy.ndarray 结构,将会展开为一维结构,返回一维结构。
    """
    if isinstance(data, float):
        d = timedelta(days=data - 367) + datetime(1, 1, 1)
        return d.year
    else:
        result = data.flatten()
        for i, r in enumerate(result):
            d = timedelta(days=r - 367) + datetime(1, 1, 1)
            result[i] = d.year

        return result