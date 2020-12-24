# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/geoip/middleware.py
# Compiled at: 2011-02-15 07:06:13
from django.template.loader import render_to_string
from geoip.models import GeoIPRecord, IPRedirectEntry, IgnoreURL
from geoip.conf import geo_setting
from geoip.exceptions import NoGeoRedirectFound
from django.conf import settings
from django.utils.encoding import smart_str

class GeoIPMiddleware(object):

    def __init__(self):
        if geo_setting('DEBUG_IP'):
            self.DEBUG_IP = geo_setting('DEBUG_IP')
        else:
            self.DEBUG_IP = False
        if geo_setting('REDIRECT_DOMAIN'):
            self.REDIRECT_DOMAIN = geo_setting('REDIRECT_DOMAIN')
        else:
            self.REDIRECT_DOMAIN = None
        if geo_setting('PROCESS_IGNORES'):
            self.ignore_paths = IgnoreURL.objects.all().values_list('url', flat=True)
        else:
            self.ignore_paths = None
        self.homepage_only = geo_setting('HOMEPAGE_ONLY')
        self.ignore_cookie = geo_setting('SET_IGNORE_COOKIE')
        self.user_code = None
        return

    def process_response(self, request, response):
        """ Read in the users IP address from the request object. If we
        find a matching GeoIPRecord for it and that country code has an
        active redirect then inject the HTML into the template to show
        a lightbox to the user """
        if 'redirect_ignore' in request.COOKIES and self.ignore_cookie:
            return response
        if self.homepage_only and request.path != '/':
            return response
        if settings.DEBUG and self.DEBUG_IP:
            inbound_ip = self.DEBUG_IP
        else:
            inbound_ip = request.META['REMOTE_ADDR']
        self.user_code = GeoIPRecord.get_code(inbound_ip)
        if geo_setting('REDIRECT_ALL') and self.user_code in geo_setting('REDIRECT_CODES'):
            context = dict(incoming_country_code=self.user_code, target_domain=self.REDIRECT_DOMAIN)
            inject_data = render_to_string('geoip/base_redirect.html', context)
        else:
            inject_data = self.redirect_from_admin()
        if '/admin' not in request.path and inject_data:
            if not self.ignore_paths or self.ignore_paths and request.path not in self.ignore_paths:
                response.content = smart_str(response.content) + smart_str(inject_data)
        return response

    def redirect_from_admin(self):
        redirect_list = IPRedirectEntry.objects.all()
        ccodes = redirect_list.values_list('incoming_country_code', flat=True)
        if self.user_code in ccodes:
            code_index = list(ccodes).index(self.user_code)
            redirect_data = redirect_list[code_index]
            context = dict(redirect_data.__dict__)
            inject_data = render_to_string('geoip/custom_redirect.html', context)
            return inject_data
        else:
            if geo_setting('FAIL_ON_MISSING'):
                raise NoGeoRedirectFound('Could not find a geo-redirect for this county in admin')
            else:
                return
            return