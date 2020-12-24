# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/spider/fz_driver.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 310 bytes
"""
@author = super_fazai
@File    : fz_driver.py
@connect : superonesfazai@gmail.com
"""
from .fz_phantomjs import MyPhantomjs, CHROME, PHANTOMJS, FIREFOX, PC, PHONE
__all__ = [
 'BaseDriver']

class BaseDriver(MyPhantomjs):
    pass