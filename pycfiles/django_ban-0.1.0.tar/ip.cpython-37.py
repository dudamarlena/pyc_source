# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ABRA\Desktop\programlarim\djangoapps\django_ban\django_ban\middleware\ip.py
# Compiled at: 2019-07-26 10:29:21
# Size of source mod 2**32: 988 bytes
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from ..models import IPBan, Url
message = '<html>\n    <head>\n        <title>403 Forbidden</title>\n    </head>\n    <body>\n        <h1 style="color:red"><center>403 Forbidden</center></h1>\n        <p><center>You are banned</center></p>\n        <p><center>Your ip address is {address}, Contact us if there is anything wrong.</center></p>\n    </body>\n    </html>'

class IPBanMiddleware(MiddlewareMixin):

    def process_request(self, request):
        url = Url.objects.get(url_name=(resolve(request.path_info).url_name))
        query, created = IPBan.objects.get_or_create(ip=(request.ip_model), url=url)
        query.update()
        if query.ban:
            return HttpResponseForbidden(message.format(address=(request.ip_model.ip)))