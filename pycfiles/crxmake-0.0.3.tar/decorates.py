# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/decorates.py
# Compiled at: 2020-02-03 23:11:43
__doc__ = '\n@author: wuyue\n@contact: wuyue92tree@163.com\n@software: PyCharm\n@file: decorates.py\n@create at: 2017-12-07 09:47\n\n这一行开始写关于本文件的说明与解释\n'
import functools
from crwy.exceptions import CrwyCookieValidException

def cls2singleton(cls, *args, **kwargs):
    u"""
    将类转换为单例模式
    :param cls: 
    :param args: 
    :param kwargs: 
    :return: 
    """
    instances = {}

    def _singleton(*args, **kwargs):
        if kwargs.pop('cls_singleton', True) is False:
            return cls(*args, **kwargs)
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


def cls_catch_exception(func):
    u"""
    该装饰器用于捕捉类方法异常
    1. 未出现异常，直接return方法执行结果
    2. 出现异常，则先将异常记入日志，再抛出异常
    :param func:
    :return:
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            self.logger.exception(e)
            raise e

    return wrapper


def cls_refresh_cookie(func):
    u"""
    该装饰器用于捕捉类方法异常 CrwyCookieValidException
    1. 未出现异常，直接return方法执行结果
    2. 出现异常，则先调用self.get_cookie()进行cookie刷新，若cookie刷新成功，
    直接return返回
    :param func:
    :return:
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except CrwyCookieValidException as e:
            if not self.get_cookie():
                self.logger.warning('Func[%s]: cookie更新失败.' % func.__name__)
                raise e
            self.logger.info('Func[%s]: cookie更新成功.' % func.__name__)
            return func(self, *args, **kwargs)

    return wrapper