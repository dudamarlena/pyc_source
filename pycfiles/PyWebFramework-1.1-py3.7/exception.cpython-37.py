# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyWebFramework\core\exception.py
# Compiled at: 2019-09-03 03:19:20
# Size of source mod 2**32: 1534 bytes
import traceback, io
from pyWebFramework.dll.IeWebFramework import RunJsException, ErrorCode
from .module import TaskManager

class FailureException(BaseException):

    def __init__(self, desc, code=ErrorCode.ExcuteFailed):
        self.desc = desc
        self.code = code


class SuccessException(BaseException):

    def __init__(self, desc='', code=ErrorCode.ExcuteSuccess):
        self.desc = desc
        self.code = code


def dispatch_task_func(task, func, *args):
    try:
        return func(*args)
    except RunJsException as e:
        try:
            traceback.print_exc()
            sio = io.StringIO()
            traceback.print_exc(file=sio)
            tb = sio.getvalue()
            task.Failure('执行js异常: \n' + tb, ErrorCode.RunJScriptFailed)
        finally:
            e = None
            del e

    except FailureException as e:
        try:
            task.Failure(e.desc, e.code)
        finally:
            e = None
            del e

    except SuccessException as e:
        try:
            task.Success(e.desc, e.code)
        finally:
            e = None
            del e

    except BaseException as e:
        try:
            traceback.print_exc()
            sio = io.StringIO()
            traceback.print_exc(file=sio)
            tb = sio.getvalue()
            task.Failure('未知python异常: \n' + tb)
        finally:
            e = None
            del e


def dispatch_page_func(func, *args):
    task = TaskManager.current_task
    if task:
        return dispatch_task_func(task, func, *args)


def wrap_callback(func):

    def wrapper(*args):
        task = TaskManager.current_task
        if task:
            dispatch_task_func(task, func, *args)

    if not func:
        return
    return wrapper