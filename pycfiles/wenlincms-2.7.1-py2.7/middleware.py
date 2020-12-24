# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/core/middleware.py
# Compiled at: 2016-05-20 23:41:38
from __future__ import unicode_literals
from django.contrib.messages import error
from django.contrib.redirects.models import Redirect
from django.core.exceptions import MiddlewareNotUsed
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from django.middleware.csrf import CsrfViewMiddleware, get_token
from django.template import Template, RequestContext
from django.utils.cache import get_max_age
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from future.utils import native_str
from wenlincms.conf import settings
from wenlincms.core.management import DEFAULT_USERNAME, DEFAULT_PASSWORD
from wenlincms.utils.cache import cache_key_prefix, nevercache_token, cache_get, cache_set, cache_installed
from wenlincms.utils.device import templates_for_device, templates_for_host
from wenlincms.utils.urls import next_url
_deprecated = {b'AdminLoginInterfaceSelector': b'AdminLoginInterfaceSelectorMiddleware', 
   b'DeviceAwareUpdateCacheMiddleware': b'UpdateCacheMiddleware', 
   b'DeviceAwareFetchFromCacheMiddleware': b'FetchFromCacheMiddleware'}

class _Deprecated(object):

    def __init__(self, *args, **kwargs):
        from warnings import warn
        msg = b'wenlincms.core.middleware.%s is deprecated.' % self.old
        if self.new:
            msg += b' Please change the MIDDLEWARE_CLASSES setting to use wenlincms.core.middleware.%s' % self.new
        warn(msg)


for old, new in _deprecated.items():
    globals()[old] = type(native_str(old), (
     _Deprecated,), {b'old': old, b'new': new})

class AdminLoginInterfaceSelectorMiddleware(object):
    """
    Checks for a POST from the admin login view and if authentication is
    successful and the "site" interface is selected, redirect to the site.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        login_type = request.POST.get(b'wenlincms_login_interface')
        if login_type and not request.user.is_authenticated():
            response = view_func(request, *view_args, **view_kwargs)
            if request.user.is_authenticated():
                if login_type == b'admin':
                    next = request.get_full_path()
                    try:
                        username = request.user.get_username()
                    except AttributeError:
                        username = request.user.username

                    if username == DEFAULT_USERNAME and request.user.check_password(DEFAULT_PASSWORD):
                        error(request, mark_safe(_(b"Your account is using the default password, please <a href='%s'>change it</a> immediately.") % reverse(b'user_change_password', args=(
                         request.user.id,))))
                else:
                    next = next_url(request) or b'/'
                return HttpResponseRedirect(next)
            return response
        return


class TemplateForDeviceMiddleware(object):
    """
    Inserts device-specific templates to the template list.
    """

    def process_template_response(self, request, response):
        if hasattr(response, b'template_name'):
            if not isinstance(response.template_name, Template):
                templates = templates_for_device(request, response.template_name)
                response.template_name = templates
        return response


class TemplateForHostMiddleware(object):
    """
    Inserts host-specific templates to the template list.
    """

    def process_template_response(self, request, response):
        if hasattr(response, b'template_name'):
            if not isinstance(response.template_name, Template):
                templates = templates_for_host(request, response.template_name)
                response.template_name = templates
        return response


class UpdateCacheMiddleware(object):
    """
    Response phase for wenlincms's cache middleware. Handles caching
    the response, and then performing the second phase of rendering,
    for content enclosed by the ``nevercache`` tag.
    """

    def process_response(self, request, response):
        is_text = response.get(b'content-type', b'').startswith(b'text')
        valid_status = response.status_code == 200
        streaming = getattr(response, b'streaming', False)
        if not is_text or streaming or settings.DEBUG and not valid_status:
            return response
        marked_for_update = getattr(request, b'_update_cache', False)
        anon = hasattr(request, b'user')
        timeout = get_max_age(response)
        if timeout is None:
            timeout = settings.CACHE_MIDDLEWARE_SECONDS
        if anon and valid_status and marked_for_update and timeout:
            cache_key = cache_key_prefix(request) + request.get_full_path()
            _cache_set = lambda r: cache_set(cache_key, r.content, timeout)
            if callable(getattr(response, b'render', None)):
                response.add_post_render_callback(_cache_set)
            else:
                _cache_set(response)
        token = nevercache_token()
        try:
            token = token.encode(b'utf-8')
        except AttributeError:
            pass

        parts = response.content.split(token)
        csrf_token = None
        try:
            csrf_token = response.cookies[settings.CSRF_COOKIE_NAME].value
        except KeyError:
            try:
                csrf_token = request.COOKIES[settings.CSRF_COOKIE_NAME]
            except KeyError:
                pass

        if csrf_token:
            request.META[b'CSRF_COOKIE'] = csrf_token
        context = RequestContext(request)
        for i, part in enumerate(parts):
            if i % 2:
                part = Template(part).render(context).encode(b'utf-8')
            parts[i] = part

        response.content = (b'').join(parts)
        response[b'Content-Length'] = len(response.content)
        if hasattr(request, b'_messages'):
            request._messages.update(response)
        return response


class FetchFromCacheMiddleware(object):
    """
    Request phase for wenlincms cache middleware. Return a response
    from cache if found, othwerwise mark the request for updating
    the cache in ``UpdateCacheMiddleware``.
    """

    def process_request(self, request):
        if cache_installed() and request.method == b'GET':
            cache_key = cache_key_prefix(request) + request.get_full_path()
            response = cache_get(cache_key)
            csrf_mw_name = b'django.middleware.csrf.CsrfViewMiddleware'
            if csrf_mw_name in settings.MIDDLEWARE_CLASSES:
                csrf_mw = CsrfViewMiddleware()
                csrf_mw.process_view(request, lambda x: None, None, None)
                get_token(request)
            if response is None:
                request._update_cache = True
            else:
                return HttpResponse(response)
        return


class SSLRedirectMiddleware(object):
    """
    Handles redirections required for SSL when ``SSL_ENABLED`` is ``True``.

    If ``SSL_FORCE_HOST`` is ``True``, and is not the current host,
    redirect to it.

    Also ensure URLs defined by ``SSL_FORCE_URL_PREFIXES`` are redirect
    to HTTPS, and redirect all other URLs to HTTP if on HTTPS.
    """

    def process_request(self, request):
        settings.use_editable()
        force_host = settings.SSL_FORCE_HOST
        response = None
        if force_host and request.get_host().split(b':')[0] != force_host:
            url = b'http://%s%s' % (force_host, request.get_full_path())
            response = HttpResponsePermanentRedirect(url)
        elif settings.SSL_ENABLED and not settings.DEV_SERVER:
            url = b'%s%s' % (request.get_host(), request.get_full_path())
            if request.path.startswith(settings.SSL_FORCE_URL_PREFIXES):
                if not request.is_secure():
                    response = HttpResponseRedirect(b'https://%s' % url)
            elif request.is_secure() and settings.SSL_FORCED_PREFIXES_ONLY:
                response = HttpResponseRedirect(b'http://%s' % url)
        if response and request.method == b'POST':
            if resolve(request.get_full_path()).url_name == b'fb_do_upload':
                return
            response.status_code = 307
        return response


class RedirectFallbackMiddleware(object):
    """
    Port of Django's ``RedirectFallbackMiddleware`` that uses
    wenlincms's approach for determining the current site.
    """

    def __init__(self):
        if b'django.contrib.redirects' not in settings.INSTALLED_APPS:
            raise MiddlewareNotUsed

    def process_response(self, request, response):
        if response.status_code == 404:
            lookup = {b'old_path': request.get_full_path()}
            try:
                redirect = Redirect.objects.get(**lookup)
            except Redirect.DoesNotExist:
                pass
            else:
                if not redirect.new_path:
                    response = HttpResponseGone()
                else:
                    response = HttpResponseRedirect(redirect.new_path)
        return response