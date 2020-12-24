# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/frame/httpcontext.py
# Compiled at: 2013-04-13 01:11:48
from errors import Error500

class HTTPContext(object):

    def __enter__(self):
        pass

    def __exit__(self, e_type, e_value, e_tb):
        if e_type is not None:
            raise Error500
            return True
        else:
            return