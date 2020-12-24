# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/django-smart-proxy/lib/python3.3/site-packages/smart_proxy/views.py
# Compiled at: 2015-03-03 13:55:10
# Size of source mod 2**32: 7837 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
import logging, re
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.validators import URLValidator
from django.http import Http404, HttpResponseBadRequest
from django.utils.module_loading import import_by_path
from django.views.generic import View
from .models import SmartProxyRequest
SMART_PROXIES = getattr(settings, 'SMART_PROXIES', {})
logger = logging.getLogger(__name__)

class SmartProxyView(View):
    __doc__ = '\n    The View where all the magic happens.\n    '
    proxy_id = None
    proxy_settings = {}
    allowed_methods = SmartProxyRequest.HTTP_METHODS
    host_endpoint = ''
    timeout = 60.0
    request_decorators = ()
    validate = URLValidator()

    def dispatch(self, request, *args, **kwargs):
        """
        Determines the destination URL, validates it, records it, and
        dispatches the modified request to the appropriate handler.
        """
        self._load_proxy_settings()
        url = self._construct_destination_url(request)
        kwargs['current_request'] = self._build_request(request, url)
        try:
            response = super(SmartProxyView, self).dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.exception(e)
            response = HttpResponseBadRequest(e)

        return response

    def get(self, request, *args, **kwargs):
        """Delegates request to `requests.get`."""
        return kwargs['current_request'].send('get')

    def put(self, request, *args, **kwargs):
        """Delegates request to `requests.put`."""
        return kwargs['current_request'].send('put')

    def post(self, request, *args, **kwargs):
        """Delegates request to `requests.post`."""
        return kwargs['current_request'].send('post')

    def delete(self, request, *args, **kwargs):
        """Delegates request to `requests.delete`."""
        return kwargs['current_request'].send('delete')

    def head(self, request, *args, **kwargs):
        """Delegates request to `requests.head`."""
        return kwargs['current_request'].send('head')

    def options(self, request, *args, **kwargs):
        """Delegates request to `requests.options`."""
        return kwargs['current_request'].send('options')

    def patch(self, request, *args, **kwargs):
        """Delegates request to `requests.patch`."""
        return kwargs['current_request'].send('patch')

    def _load_proxy_settings(self):
        """Initializes the View with settings from the PROXY_SETTINGS dict."""
        if not self.proxy_settings:
            self.proxy_id = self.kwargs.get('proxy_id', None)
            if self.proxy_id and self.proxy_id in SMART_PROXIES:
                self.proxy_settings = SMART_PROXIES[self.proxy_id]
                self.host_endpoint = self._get_host_endpoint()
                if 'allowed_methods' in self.proxy_settings:
                    self.allowed_methods = self.proxy_settings['allowed_methods']
                if 'timeout' in self.proxy_settings:
                    self.timeout = self.proxy_settings['timeout']
                self.request_decorators = self._get_request_decorators()
            else:
                raise Http404('The specified Django Smart Proxy could not be found.')
        return

    def _get_headers(self, request):
        return {}

    def _build_request(self, request, url):
        """Transforms a request into a SmartProxyRequest."""
        current_request = SmartProxyRequest(url=url, data=self.request.body, headers=self._get_headers(request), settings=self.proxy_settings, timeout=self.timeout)
        for decorator in self.request_decorators:
            try:
                current_request = decorator(current_request, session=request.session)
            except Exception as e:
                logger.exception(e)

        return current_request

    def _construct_destination_url(self, request):
        """
        Transforms the request URL into the equivalent URL at the host
        endpoint.
        """
        return re.sub('.*/{0}/(.*)'.format(self.proxy_id), '{0}\\1'.format(self.host_endpoint), request.get_full_path())

    def _get_request_decorators(self):
        """
        Checks to see if request decorators have been defined.
        If so, translates fully-qualified string representations to callables and
        populates self.request_decorators with the list of callables. If a request
        decorator cannot be resolved, a warning is logged, but we will continue
        gracefully.
        """
        request_decorators = self.request_decorators
        if 'request_decorators' in self.proxy_settings:
            for request_decorator in self.proxy_settings['request_decorators']:
                if not hasattr(request_decorator, '__call__'):
                    try:
                        request_decorator = import_by_path(request_decorator)
                    except ImproperlyConfigured as e:
                        logger.warning(e)
                        continue

                request_decorators += (request_decorator,)

        return request_decorators

    def _get_host_endpoint(self):
        """
        Checks that we've identified a host for the specified proxy, and that
        it's a valid URL.
        """
        host_endpoint = self.proxy_settings.get('host_endpoint', self.host_endpoint)
        if not host_endpoint:
            raise Http404('A host has not been configured for the specified Django Smart Proxy.')
        try:
            self.validate(host_endpoint)
        except ValidationError as e:
            raise HttpResponseBadRequest(e)

        return host_endpoint