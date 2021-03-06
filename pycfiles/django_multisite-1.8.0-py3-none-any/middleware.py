# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jordi/vcs/django-multisite/multisite/middleware.py
# Compiled at: 2019-05-02 13:24:49
from __future__ import unicode_literals
from __future__ import absolute_import
import os, tempfile
try:
    from urlparse import urlsplit, urlunsplit
except ImportError:
    from urllib.parse import urlsplit, urlunsplit

import django
from django.conf import settings
from django.contrib.sites.models import Site, SITE_CACHE
from django.core.exceptions import DisallowedHost
from django.core import mail
from django.core.cache import caches
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from django.core.exceptions import ImproperlyConfigured
try:
    from django.urls import get_callable
except ImportError:
    from django.core.urlresolvers import get_callable

from django.db.models.signals import pre_save, post_delete, post_init
from django.http import Http404, HttpResponsePermanentRedirect
from hashlib import md5 as md5_constructor
from .models import Alias

class DynamicSiteMiddleware(MiddlewareMixin):

    def __init__(self, *args, **kwargs):
        super(DynamicSiteMiddleware, self).__init__(*args, **kwargs)
        if not hasattr(settings.SITE_ID, b'set'):
            raise TypeError(b'Invalid type for settings.SITE_ID: %s' % type(settings.SITE_ID).__name__)
        self.cache_alias = getattr(settings, b'CACHE_MULTISITE_ALIAS', b'default')
        self.key_prefix = getattr(settings, b'CACHE_MULTISITE_KEY_PREFIX', settings.CACHES[self.cache_alias].get(b'KEY_PREFIX', b''))
        self.cache = caches[self.cache_alias]
        post_init.connect(self.site_domain_cache_hook, sender=Site, dispatch_uid=b'multisite_post_init')
        pre_save.connect(self.site_domain_changed_hook, sender=Site)
        post_delete.connect(self.site_deleted_hook, sender=Site)

    def get_cache_key(self, netloc):
        """Returns a cache key based on ``netloc``."""
        netloc = md5_constructor(netloc.encode(b'utf-8'))
        return b'multisite.alias.%s.%s' % (self.key_prefix,
         netloc.hexdigest())

    def netloc_parse(self, netloc):
        """
        Returns ``(host, port)`` for ``netloc`` of the form ``'host:port'``.

        If netloc does not have a port number, ``port`` will be None.
        """
        if b':' in netloc:
            return netloc.rsplit(b':', 1)
        else:
            return (
             netloc, None)
            return

    def get_development_alias(self, netloc):
        """
        Returns valid Alias when in development mode. Otherwise, returns None.

        Development mode is either:
        - Running tests, i.e. manage.py test
        - Running locally in settings.DEBUG = True, where the hostname is
          a top-level name, i.e. localhost
        """
        is_testserver = hasattr(mail, b'outbox') and netloc in ('testserver', 'adminsite.com')
        is_local_debug = settings.DEBUG and len(netloc.split(b'.')) == 1
        if is_testserver or is_local_debug:
            try:
                site_id = settings.SITE_ID.get_default()
                return Alias.canonical.get(site=site_id)
            except ValueError:
                return Alias.canonical.order_by(b'site')[0]

    def get_alias(self, netloc):
        """
        Returns Alias matching ``netloc``. Otherwise, returns None.
        """
        host, port = self.netloc_parse(netloc)
        try:
            alias = Alias.objects.resolve(host=host, port=port)
        except ValueError:
            alias = None

        if alias is None:
            return self.get_development_alias(netloc)
        else:
            return alias

    def fallback_view(self, request):
        """
        Runs the fallback view function in ``settings.MULTISITE_FALLBACK``.

        If ``MULTISITE_FALLBACK`` is None, raises an Http404 error.

        If ``MULTISITE_FALLBACK`` is callable, will treat that
        callable as a view that returns an HttpResponse.

        If ``MULTISITE_FALLBACK`` is a string, will resolve it to a
        view that returns an HttpResponse.

        In order to use a generic view that takes additional
        parameters, ``settings.MULTISITE_FALLBACK_KWARGS`` may be a
        dictionary of additional keyword arguments.
        """
        fallback = getattr(settings, b'MULTISITE_FALLBACK', None)
        if fallback is None:
            raise Http404
        if callable(fallback):
            view = fallback
        else:
            try:
                view = get_callable(fallback)
                if django.VERSION < (1, 8):
                    if not callable(view):
                        raise ImportError()
            except ImportError:
                raise ImproperlyConfigured(b'settings.MULTISITE_FALLBACK is not callable: %s' % fallback)

        kwargs = getattr(settings, b'MULTISITE_FALLBACK_KWARGS', {})
        if hasattr(view, b'as_view'):
            return view.as_view(**kwargs)(request)
        else:
            return view(request, **kwargs)

    def redirect_to_canonical(self, request, alias):
        if not alias.redirect_to_canonical or alias.is_canonical:
            return
        url = urlsplit(request.build_absolute_uri(request.get_full_path()))
        url = urlunsplit((url.scheme,
         alias.site.domain,
         url.path, url.query, url.fragment))
        return HttpResponsePermanentRedirect(url)

    def process_request(self, request):
        try:
            netloc = request.get_host().lower()
        except DisallowedHost:
            settings.SITE_ID.reset()
            return self.fallback_view(request)

        cache_key = self.get_cache_key(netloc)
        alias = self.cache.get(cache_key)
        if alias is not None:
            self.cache.set(cache_key, alias)
            settings.SITE_ID.set(alias.site_id)
            return self.redirect_to_canonical(request, alias)
        else:
            alias = self.get_alias(netloc)
            if alias is None:
                settings.SITE_ID.reset()
                return self.fallback_view(request)
            self.cache.set(cache_key, alias)
            settings.SITE_ID.set(alias.site_id)
            SITE_CACHE[settings.SITE_ID] = alias.site
            return self.redirect_to_canonical(request, alias)

    @classmethod
    def site_domain_cache_hook(self, sender, instance, *args, **kwargs):
        """Caches Site.domain in the object for site_domain_changed_hook."""
        instance._domain_cache = instance.domain

    def site_domain_changed_hook(self, sender, instance, raw, *args, **kwargs):
        """Clears the cache if Site.domain has changed."""
        if raw or instance.pk is None:
            return
        original = getattr(instance, b'_domain_cache', None)
        if original != instance.domain:
            self.cache.clear()
        return

    def site_deleted_hook(self, *args, **kwargs):
        """Clears the cache if Site was deleted."""
        self.cache.clear()


class CookieDomainMiddleware(MiddlewareMixin):

    def __init__(self, *args, **kwargs):
        super(CookieDomainMiddleware, self).__init__(*args, **kwargs)
        self.depth = int(getattr(settings, b'MULTISITE_COOKIE_DOMAIN_DEPTH', 0))
        if self.depth < 0:
            raise ValueError((b'Invalid MULTISITE_COOKIE_DOMAIN_DEPTH: {depth!r}').format(depth=self.depth))
        self.psl_cache = getattr(settings, b'MULTISITE_PUBLIC_SUFFIX_LIST_CACHE', None)
        if self.psl_cache is None:
            self.psl_cache = os.path.join(tempfile.gettempdir(), b'multisite_tld.dat')
        self._tldextract = None
        return

    def tldextract(self, url):
        import tldextract
        if self._tldextract is None:
            self._tldextract = tldextract.TLDExtract(cache_file=self.psl_cache)
        return self._tldextract(url)

    def match_cookies(self, request, response):
        return [ c for c in response.cookies.values() if not c[b'domain'] ]

    def process_response(self, request, response):
        matched = self.match_cookies(request=request, response=response)
        if not matched:
            return response
        parsed = self.tldextract(request.get_host())
        if not parsed.suffix:
            return response
        if not parsed.domain:
            return response
        subdomains = parsed.subdomain.split(b'.') if parsed.subdomain else []
        if not self.depth:
            subdomains = [
             b'']
        else:
            if len(subdomains) < self.depth:
                return response
            subdomains = [b''] + subdomains[-self.depth:]
        domain = (b'.').join(subdomains + [parsed.domain, parsed.suffix])
        for morsel in matched:
            morsel[b'domain'] = domain

        return response