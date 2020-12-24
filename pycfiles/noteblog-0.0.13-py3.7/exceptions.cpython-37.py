# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/exceptions.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 589 bytes
"""
@author = super_fazai
@File    : my_exceptions.py
@connect : superonesfazai@gmail.com
"""
__all__ = [
 'ResponseBodyIsNullStrException',
 'NoNextPageException']

class ResponseBodyIsNullStrException(Exception):
    __doc__ = '请求的应答返回的body为空str异常, 多用于处理proxy异常中, 避免数据误删'


class NoNextPageException(Exception):
    __doc__ = '没有后续页面的异常'