# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djlimiter/errors.py
# Compiled at: 2015-01-08 11:09:27
from django.http import HttpResponse

class RateLimitExceeded(HttpResponse):
    """
    exception raised when a rate limit is hit (status code: 429).
    """
    status_code = 429

    def __init__(self, limit):
        super(RateLimitExceeded, self).__init__(str(limit))