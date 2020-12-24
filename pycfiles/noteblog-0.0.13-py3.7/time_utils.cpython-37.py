# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/time_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 6244 bytes
"""
@author = super_fazai
@File    : time_utils.py
@Time    : 2016/7/13 18:02
@connect : superonesfazai@gmail.com
"""
import time
from pytz import timezone, country_timezones
from datetime import datetime
import re, functools
from threading import Thread
from .common_utils import get_random_int_number
__all__ = [
 'get_shanghai_time',
 'timestamp_to_regulartime',
 'string_to_datetime',
 'datetime_to_timestamp',
 'date_parse',
 'get_now_13_bit_timestamp',
 'fz_timer',
 'fz_set_timeout',
 'func_time']

def get_shanghai_time(retries=10):
    """
    时区处理，得到上海时间
    :return: datetime类型
    """
    tz = timezone('Asia/Shanghai')
    now_time = datetime.now(tz)
    now_time = re.compile('\\..*').sub('', str(now_time))
    try:
        now_time = datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        try:
            if retries > 0:
                return get_shanghai_time(retries=(retries - 1))
            raise e
        finally:
            e = None
            del e

    return now_time


def timestamp_to_regulartime(timestamp):
    """
    将时间戳转换成时间
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestamp)))


def string_to_datetime(string):
    """
    将字符串转换成datetime
    :param string:
    :return:
    """
    return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')


def datetime_to_timestamp(_dateTime):
    """
    把datetime类型转外时间戳形式
    :param _dateTime:
    :return: int
    """
    return int(time.mktime(_dateTime.timetuple()))


class fz_timer(object):
    __doc__ = '\n    A timer can time how long does calling take as 上下文管理器 or 装饰器.\n    If assign ``print_func`` with ``sys.stdout.write``, ``logger.info`` and so on,\n    timer will print the spent time.\n        用法: eg:\n            import sys\n\n            @fz_timer(print_func=sys.stdout.write)\n            def tmp():\n                get_shanghai_time()\n\n            tmp()\n    '

    def __init__(self, print_func=None):
        """
        :param print_func: sys.stdout.write | logger.info
        """
        self.elapsed = None
        self.print_func = print_func

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *_):
        self.elapsed = time.time() - self.start
        if self.print_func:
            self.print_func(self.__str__())

    def __call__(self, fun):

        def wrapper(*args, **kwargs):
            with self:
                return fun(*args, **kwargs)

        return wrapper

    def __str__(self):
        return 'Spent time: {}s'.format(self.elapsed)


class TimeoutError(Exception):
    pass


def fz_set_timeout(seconds, error_message='函数执行超时!'):
    """
    可以给任意可能会hang住的函数添加超时功能[这个功能在编写外部API调用, 爬虫, 数据库查询的时候特别有用]
        用法: eg:
            from time import sleep

            @fz_set_timeout(seconds=2)
            def tmp():
                sleep(3)

            tmp()
    :param seconds: 设置超时时间
    :param error_message: 显示的错误信息
    :return: None | Exception: 自定义的超时异常TimeoutError
    """

    def decorated(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            share = [TimeoutError(error_message)]

            def func_with_except():
                try:
                    share[0] = func(*args, **kwargs)
                except Exception as e:
                    try:
                        share[0] = e
                    finally:
                        e = None
                        del e

            t = Thread(target=func_with_except)
            t.daemon = True
            try:
                t.start()
                t.join(seconds)
            except Exception as e:
                try:
                    raise e
                finally:
                    e = None
                    del e

            result = share[0]
            if isinstance(result, BaseException):
                raise result
            return result

        return wrapper

    return decorated


def date_parse(target_date_str) -> datetime:
    """
    不规范日期解析为datetime类型
        eg:
            In [5]: parse('2018-10-11T07:46:19Z')
            Out[5]: datetime.datetime(2018, 10, 11, 7, 46, 19, tzinfo=tzutc())

            In [6]: parse('Sun, 25 Nov 2018 14:46:19 +0800')
            Out[6]: datetime.datetime(2018, 11, 25, 14, 46, 19, tzinfo=tzoffset(None, 28800))
    :param target_date_str:
    :return:
    """
    from dateutil.parser import parse
    return parse(target_date_str)


def func_time(func):
    """
    计算函数耗时
    :param func:
    :return:
    """

    def _wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        print('func_name: {}, spent time: {}s'.format(func.__name__, time.time() - start_time))

    return _wrapper


def get_now_13_bit_timestamp() -> str:
    """
    得到当前的13位时间戳
    :return: eg: '1556963497711'
    """
    return str(datetime_to_timestamp(get_shanghai_time())) + str(get_random_int_number(100, 999))