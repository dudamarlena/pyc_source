# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/dispatch/resource/exc.py
# Compiled at: 2019-06-10 13:47:23
# Size of source mod 2**32: 177 bytes
try:
    from webob.exc import HTTPMethodNotAllowed
except ImportError:
    HTTPMethodNotAllowed = RuntimeError

class InvalidMethod(HTTPMethodNotAllowed):
    pass