# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/flask_limiter/util.py
# Compiled at: 2019-09-23 12:31:26
# Size of source mod 2**32: 495 bytes
"""

"""
from flask import request

def get_ipaddr():
    """
    :return: the ip address for the current request (or 127.0.0.1 if none found)
     based on the X-Forwarded-For headers.
    """
    if request.access_route:
        return request.access_route[0]
    return request.remote_addr or '127.0.0.1'


def get_remote_address():
    """
    :return: the ip address for the current request (or 127.0.0.1 if none found)
    """
    return request.remote_addr or '127.0.0.1'