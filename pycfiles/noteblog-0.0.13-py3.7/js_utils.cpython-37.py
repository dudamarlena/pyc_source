# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/js_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 629 bytes
"""
@author = super_fazai
@File    : js_utils.py
@connect : superonesfazai@gmail.com
"""
from execjs import compile
__all__ = [
 'get_js_parser_res']

def get_js_parser_res(js_path, func_name, *args):
    """
    python调用js, 并返回结果
    :param js_path: js文件路径
    :param func_name: 待调用的函数名
    :param args: 该函数待传递的参数
    :return: res
    """
    with open(js_path, 'r') as (f):
        js_code = f.read()
    js_parser = compile(js_code)
    res = (js_parser.call)(func_name, *args)
    return res