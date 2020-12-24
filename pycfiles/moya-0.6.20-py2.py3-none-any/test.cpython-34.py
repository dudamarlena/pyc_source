# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/testproject/blog/py/test.py
# Compiled at: 2015-09-01 07:17:44
# Size of source mod 2**32: 130 bytes
from __future__ import print_function
import moya

@moya.expose.macro('test')
def test():
    print('Success! :-)')
    return 10