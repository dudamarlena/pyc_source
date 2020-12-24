# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/single_file_module-project/sfm/decorator.py
# Compiled at: 2019-04-21 23:26:54
"""
collection of useful decorator.
"""
from __future__ import print_function
import time

def _text_of_func_args_and_kwargs(func, args, kwargs):
    u"""

    **中文文档**

    返回一个函数的调用以及其参数的文本形式。
    """
    text_args = (', ').join([ '%r' % arg for arg in args ])
    text_kwargs = (', ').join([ '%s=%r' % (key, value) for key, value in kwargs.items()
                              ])
    if text_args and text_kwargs:
        return '%s(%s, %s)' % (func.__name__, text_args, text_kwargs)
    if not text_args and not text_kwargs:
        return '%s()' % func.__name__
    if text_args:
        return '%s(%s)' % (func.__name__, text_args)
    if text_kwargs:
        return '%s(%s)' % (func.__name__, text_kwargs)
    raise Exception


def elapsed_printer(func):
    u"""

    **中文文档**

    此包装器可以打印函数的输入参数, 以及运行时间。
    """

    def _wrapper(*args, **kwargs):
        print('>>> %s # Running ...' % _text_of_func_args_and_kwargs(func, args, kwargs))
        st = time.clock()
        res = func(*args, **kwargs)
        elapsed = time.clock() - st
        print('    Complete! Elapsed %.6f seconds.' % elapsed)
        return res

    return _wrapper


def run_if_is_main(__name__):
    u"""

    **中文文档**

    此装饰器能够让函数自动只在自己是以主脚本进行时才运行, 否则直接返回None。
    此装饰器在pytest下无效。
    """

    def _run_if_is_main(func):

        def _wrapper(*args, **kwargs):
            if __name__ == '__main__':
                return func(*args, **kwargs)

        return _wrapper

    return _run_if_is_main


@run_if_is_main(__name__)
def test_run_if_is_main():
    return 'HelloWorld'