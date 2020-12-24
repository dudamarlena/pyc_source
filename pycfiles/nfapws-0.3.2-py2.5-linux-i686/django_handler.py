# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fapws/contrib/django_handler.py
# Compiled at: 2009-08-20 03:05:56
from django.core.handlers import wsgi
import django
djhand = wsgi.WSGIHandler()

def handler(environ, start_response):
    res = djhand(environ, start_response)
    if django.VERSION[0] == 0:
        for (key, val) in res.headers.items():
            start_response.response_headers[key] = val

    for (key, val) in res._headers.values():
        start_response.response_headers[key] = val

    start_response.cookies = res.cookies
    return res.content