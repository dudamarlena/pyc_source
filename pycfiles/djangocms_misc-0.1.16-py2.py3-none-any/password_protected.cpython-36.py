# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/benzkji/Development/open/djangocms-misc/djangocms_misc/basic/middleware/password_protected.py
# Compiled at: 2020-01-07 08:41:54
# Size of source mod 2**32: 1236 bytes
from django.shortcuts import redirect
import django
if django.VERSION[:2] < (1, 10):
    from django.core.urlresolvers import reverse
else:
    from django.urls import reverse

class PasswordProtectedMiddleware(object):

    def __init__(self, get_response=None):
        if get_response:
            self.get_response = get_response

    def __call__(self, request):
        a_possible_redirect = self.process_request(request)
        if a_possible_redirect:
            return a_possible_redirect
        else:
            response = self.get_response(request)
            return response

    def process_request(self, request):
        login_url = reverse('admin:login')
        logout_url = reverse('admin:logout')
        if request.path in (login_url, logout_url):
            return
        if not request.user.is_authenticated:
            redirect_url = '{}?next={}'.format(login_url, request.path)
            return redirect(redirect_url)