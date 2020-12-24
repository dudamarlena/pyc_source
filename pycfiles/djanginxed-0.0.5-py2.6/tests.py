# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/djanginxed/tests.py
# Compiled at: 2011-02-16 03:45:00
import hashlib
from django.conf import settings
from django.core.cache import cache as django_cache
from django.http import HttpResponse, HttpRequest
from django.test import TestCase
from djanginxed.decorators import cache
from snippetscream import RequestFactory

def test_key_generator(request):
    return 'foobar'


class DecoratorCacheTestCase(TestCase):

    def test_get_cache_key(self):
        request = RequestFactory().get('/')
        key = cache.get_cache_key(request, '')
        self.assertEqual(len(key), 32)
        self.assertEqual(key, hashlib.md5('/').hexdigest())
        key = cache.get_cache_key(request, 'prefix')
        self.assertEqual(key, 'prefix' + hashlib.md5('/').hexdigest())
        settings.CACHE_MIDDLEWARE_KEY_PREFIX = 'prefix'
        key = cache.get_cache_key(request, '')
        self.assertEqual(key, 'prefix' + hashlib.md5('/').hexdigest())
        settings.CACHE_MIDDLEWARE_KEY_PREFIX = ''
        request = RequestFactory().get('/?foo=bar')
        key = cache.get_cache_key(request, '')
        self.assertEqual(key, hashlib.md5('/?foo=bar').hexdigest())
        request = RequestFactory().get('/?foo=bar')
        key = cache.get_cache_key(request, '', key_generator=test_key_generator)
        self.assertEqual(key, test_key_generator(request))
        request = RequestFactory().get('/?foo=bar')
        key = cache.get_cache_key(request, 'prefix', key_generator=test_key_generator)
        self.assertEqual(key, 'prefix' + test_key_generator(request))

    def test_cache_page(self):

        def my_view(request):
            return HttpResponse('response')

        django_cache.clear()
        my_view_cached = cache.cache_page(123)(my_view)
        self.assertEqual(my_view_cached(HttpRequest()).content, 'response')
        my_view_cached = cache.cache_page(123)(my_view)
        self.assertEqual(my_view_cached(HttpRequest()), 'response')