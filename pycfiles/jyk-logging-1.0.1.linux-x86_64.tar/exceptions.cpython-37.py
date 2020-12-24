# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jiangyongkang/anaconda3/lib/python3.7/site-packages/jyk/logging/exceptions.py
# Compiled at: 2020-03-31 23:16:59
# Size of source mod 2**32: 159 bytes
"""jyk jyk exceptions"""

class jykCriticalError(Exception):
    __doc__ = 'jyk critical error'


class jykLoggingError(jykCriticalError):
    __doc__ = 'jyk scan error'