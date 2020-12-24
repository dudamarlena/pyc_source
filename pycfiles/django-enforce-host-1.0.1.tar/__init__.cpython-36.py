# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jamie/code/django-enforce-hostname/enforce_host/__init__.py
# Compiled at: 2017-11-24 11:20:06
# Size of source mod 2**32: 1096 bytes
__version__ = '1.0.0'
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponsePermanentRedirect
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

try:
    string_type = basestring
except NameError:
    string_type = str

class EnforceHostMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None):
        self.get_response = get_response
        setting_value = getattr(settings, 'ENFORCE_HOST', None)
        if setting_value is None:
            raise MiddlewareNotUsed()
        if isinstance(setting_value, string_type):
            setting_value = [
             setting_value]
        self.allowed_hosts = setting_value

    def process_request(self, request):
        host = request.get_host()
        if host in self.allowed_hosts:
            return
        else:
            new_url = '%s://%s%s' % (
             'https' if request.is_secure() else 'http',
             self.allowed_hosts[0], request.get_full_path())
            return HttpResponsePermanentRedirect(new_url)