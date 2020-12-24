# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/notifications/middleware.py
# Compiled at: 2020-02-28 16:23:31
# Size of source mod 2**32: 1593 bytes
from __future__ import unicode_literals
import datetime, operator
from django.utils.deprecation import MiddlewareMixin
from .models import Notification

class NotificationMiddleware(MiddlewareMixin):

    def is_valid_request(self, request):
        return hasattr(request, 'user') and request.user.is_authenticated

    def process_request(self, request):
        """
        Adds notification status to requests for handling in views etc.
        :param request:
        :return: None
        """
        if self.is_valid_request(request):
            request.notifications = Notification.unseen(request.user)

    def process_response(self, request, response):
        if not self.is_valid_request(request):
            return response
        else:
            notifications = Notification.unseen(request.user)
            sorted_items = sorted((notifications.items()), key=(operator.itemgetter(1)))
            if notifications:
                epoch = datetime.datetime.utcfromtimestamp(0)
                max_age = 1209600
                expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)
                coookie_string = '-'.join(('{}:{}'.format(key, (val - epoch).total_seconds() * 1000.0) for key, val in sorted_items))
                response.set_cookie('notifications',
                  coookie_string, expires=expires)
            else:
                response.delete_cookie('notifications')
        return response