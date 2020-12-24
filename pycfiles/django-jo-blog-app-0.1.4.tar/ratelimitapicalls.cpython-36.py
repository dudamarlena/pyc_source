# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/maluki/blog/django_blog/blog_project/blog/api/ratelimitapicalls.py
# Compiled at: 2019-07-26 08:00:57
# Size of source mod 2**32: 202 bytes
from rest_framework.throttling import BaseThrottle
from rest_framework.exceptions import Throttled

class RandomRateThrottle(BaseThrottle):

    def allow_request(self, request, view):
        return 6