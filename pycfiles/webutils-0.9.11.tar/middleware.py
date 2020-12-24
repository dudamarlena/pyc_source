# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/pjs/python-modules/webutils/djtools/middleware.py
# Compiled at: 2016-05-17 14:52:55
from django.conf import settings

class AddIPAddress(object):

    def process_request(self, request):
        request.ip_address = self.get_real_ip(request.META)
        return

    def get_real_ip(self, meta_data):
        checks = ('HTTP_X_REAL_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR')
        ip = None
        for check in checks:
            if check in meta_data:
                ip = meta_data[check]
                break

        return ip or ''