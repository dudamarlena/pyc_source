# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/djangohttpdigest/http.py
# Compiled at: 2011-04-16 15:59:35
"""
Fixes around django.http
"""
from django.http import HttpResponse

class HttpResponseNotAuthorized(HttpResponse):
    status_code = 401