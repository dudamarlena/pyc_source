# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/thread_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 517 bytes
"""
@author = super_fazai
@File    : thread_utils.py
@connect : superonesfazai@gmail.com
"""
from functools import wraps
__all__ = [
 'thread_safe']

def thread_safe(lock):
    """
    线程安全装饰器
    :param lock: 锁
    :return:
    """

    def decorate(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)

        return wrapper

    return decorate