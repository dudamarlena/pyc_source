# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/url_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 570 bytes
"""
@author = super_fazai
@File    : url_utils.py
@Time    : 2016/7/28 11:59
@connect : superonesfazai@gmail.com
"""
from urllib.parse import unquote
__all__ = [
 'unquote_plus']

def unquote_plus(string, encoding='utf-8', errors='replace'):
    """
    url解码
        eg: unquote_plus('%7e/abc+def') -> '~/abc def'
    :param string:
    :param encoding:
    :param errors:
    :return:
    """
    string = string.replace('+', ' ')
    return unquote(string=string, encoding=encoding, errors=errors)