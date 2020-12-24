# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jordi/vcs/django-multisite/multisite/middleware.py
# Compiled at: 2019-05-02 13:24:49
# Size of source mod 2**32: 10088 bytes
from __future__ import unicode_literals
from __future__ import absolute_import
import os, tempfile
try:
    from urlparse import urlsplit, urlunsplit
except ImportError:
    from urllib.parse import urlsplit, urlunsplit
else:
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
else:
    from django.core.exceptions import ImproperlyConfigured
    try:
        from django.urls import get_callable
    except ImportError:
        from django.core.urlresolvers import get_callable
    else:
        from django.db.models.signals import pre_save, post_delete, post_init
        from django.http import Http404, HttpResponsePermanentRedirect
        from hashlib import md5 as md5_constructor
        from .models import Alias

        class DynamicSiteMiddleware(MiddlewareMixin):

            def __init__(self, *args, **kwargs):
                (super(DynamicSiteMiddleware, self).__init__)(*args, **kwargs)
                if not hasattr(settings.SITE_ID, 'set'):
                    raise TypeError('Invalid type for settings.SITE_ID: %s' % type(settings.SITE_ID).__name__)
                self.cache_alias = getattr(settings, 'CACHE_MULTISITE_ALIAS', 'default')
                self.key_prefix = getattr(settings, 'CACHE_MULTISITE_KEY_PREFIX', settings.CACHES[self.cache_alias].get('KEY_PREFIX', ''))
                self.cache = caches[self.cache_alias]
                post_init.connect((self.site_domain_cache_hook), sender=Site, dispatch_uid='multisite_post_init')
                pre_save.connect((self.site_domain_changed_hook), sender=Site)
                post_delete.connect((self.site_deleted_hook), sender=Site)

            def get_cache_key(self, netloc):
                """Returns a cache key based on ``netloc``."""
                netloc = md5_constructor(netloc.encode('utf-8'))
                return 'multisite.alias.%s.%s' % (self.key_prefix,
                 netloc.hexdigest())

            def netloc_parse(self, netloc):
                """
        Returns ``(host, port)`` for ``netloc`` of the form ``'host:port'``.

        If netloc does not have a port number, ``port`` will be None.
        """
                if ':' in netloc:
                    return netloc.rsplit(':', 1)
                return (netloc, None)

            def get_development_alias--- This code section failed: ---

 L.  91         0  LOAD_GLOBAL              hasattr
                2  LOAD_GLOBAL              mail
                4  LOAD_STR                 'outbox'
                6  CALL_FUNCTION_2       2  ''
                8  JUMP_IF_FALSE_OR_POP    16  'to 16'

 L.  92        10  LOAD_FAST                'netloc'
               12  LOAD_CONST               ('testserver', 'adminsite.com')
               14  COMPARE_OP               in
             16_0  COME_FROM             8  '8'

 L.  91        16  STORE_FAST               'is_testserver'

 L.  95        18  LOAD_GLOBAL              settings
               20  LOAD_ATTR                DEBUG
               22  JUMP_IF_FALSE_OR_POP    40  'to 40'
               24  LOAD_GLOBAL              len
               26  LOAD_FAST                'netloc'
               28  LOAD_METHOD              split
               30  LOAD_STR                 '.'
               32  CALL_METHOD_1         1  ''
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_CONST               1
               38  COMPARE_OP               ==
             40_0  COME_FROM            22  '22'
               40  STORE_FAST               'is_local_debug'

 L.  96        42  LOAD_FAST                'is_testserver'
               44  POP_JUMP_IF_TRUE     50  'to 50'
               46  LOAD_FAST                'is_local_debug'
               48  POP_JUMP_IF_FALSE   114  'to 114'
             50_0  COME_FROM            44  '44'

 L.  97        50  SETUP_FINALLY        78  'to 78'

 L.  99        52  LOAD_GLOBAL              settings
               54  LOAD_ATTR                SITE_ID
               56  LOAD_METHOD              get_default
               58  CALL_METHOD_0         0  ''
               60  STORE_FAST               'site_id'

 L. 100        62  LOAD_GLOBAL              Alias
               64  LOAD_ATTR                canonical
               66  LOAD_ATTR                get
               68  LOAD_FAST                'site_id'
               70  LOAD_CONST               ('site',)
               72  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               74  POP_BLOCK        
               76  RETURN_VALUE     
             78_0  COME_FROM_FINALLY    50  '50'

 L. 101        78  DUP_TOP          
               80  LOAD_GLOBAL              ValueError
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE   112  'to 112'
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L. 103        92  LOAD_GLOBAL              Alias
               94  LOAD_ATTR                canonical
               96  LOAD_METHOD              order_by
               98  LOAD_STR                 'site'
              100  CALL_METHOD_1         1  ''
              102  LOAD_CONST               0
              104  BINARY_SUBSCR    
              106  ROT_FOUR         
              108  POP_EXCEPT       
              110  RETURN_VALUE     
            112_0  COME_FROM            84  '84'
              112  END_FINALLY      
            114_0  COME_FROM            48  '48'

Parse error at or near `POP_TOP' instruction at offset 88

            def get_alias(self, netloc):
                """
        Returns Alias matching ``netloc``. Otherwise, returns None.
        """
                host, port = self.netloc_parse(netloc)
                try:
                    alias = Alias.objects.resolve(host=host, port=port)
                except ValueError:
                    alias = None
                else:
                    if alias is None:
                        return self.get_development_alias(netloc)
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
                fallback = getattr(settings, 'MULTISITE_FALLBACK', None)
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
                        raise ImproperlyConfigured('settings.MULTISITE_FALLBACK is not callable: %s' % fallback)
                    else:
                        kwargs = getattr(settings, 'MULTISITE_FALLBACK_KWARGS', {})
                        if hasattr(view, 'as_view'):
                            return (view.as_view)(**kwargs)(request)
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
                else:
                    cache_key = self.get_cache_key(netloc)
                    alias = self.cache.get(cache_key)
                    if alias is not None:
                        self.cache.set(cache_key, alias)
                        settings.SITE_ID.set(alias.site_id)
                        return self.redirect_to_canonical(request, alias)
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
                original = getattr(instance, '_domain_cache', None)
                if original != instance.domain:
                    self.cache.clear()

            def site_deleted_hook(self, *args, **kwargs):
                """Clears the cache if Site was deleted."""
                self.cache.clear()


        class CookieDomainMiddleware(MiddlewareMixin):

            def __init__(self, *args, **kwargs):
                (super(CookieDomainMiddleware, self).__init__)(*args, **kwargs)
                self.depth = int(getattr(settings, 'MULTISITE_COOKIE_DOMAIN_DEPTH', 0))
                if self.depth < 0:
                    raise ValueError('Invalid MULTISITE_COOKIE_DOMAIN_DEPTH: {depth!r}'.format(depth=(self.depth)))
                self.psl_cache = getattr(settings, 'MULTISITE_PUBLIC_SUFFIX_LIST_CACHE', None)
                if self.psl_cache is None:
                    self.psl_cache = os.path.join(tempfile.gettempdir(), 'multisite_tld.dat')
                self._tldextract = None

            def tldextract(self, url):
                import tldextract
                if self._tldextract is None:
                    self._tldextract = tldextract.TLDExtract(cache_file=(self.psl_cache))
                return self._tldextract(url)

            def match_cookies(self, request, response):
                return [c for c in response.cookies.values() if not c['domain']]

            def process_response(self, request, response):
                matched = self.match_cookies(request=request, response=response)
                if not matched:
                    return response
                    parsed = self.tldextract(request.get_host())
                    if not parsed.suffix:
                        return response
                    if not parsed.domain:
                        return response
                else:
                    subdomains = parsed.subdomain.split('.') if parsed.subdomain else []
                    if not self.depth:
                        subdomains = [
                         '']
                    else:
                        if len(subdomains) < self.depth:
                            return response
                    subdomains = [
                     ''] + subdomains[-self.depth:]
                domain = '.'.join(subdomains + [parsed.domain, parsed.suffix])
                for morsel in matched:
                    morsel['domain'] = domain
                else:
                    return response