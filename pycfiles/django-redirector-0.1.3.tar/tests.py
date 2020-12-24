# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yuji/Projects/Grove/grove_project/grove/../grove/website/redirects/tests.py
# Compiled at: 2012-05-30 17:43:58
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.core.cache import cache
from grove.website.redirects.models import Redirect, RedirectGroup, CACHE_GENERATION_KEY, generate_cache_prefix
from mock import Mock

class RedirectTest(TestCase):

    def setUp(self):
        group = RedirectGroup.objects.create(name='A Group')
        Redirect.objects.create(is_active=True, group=group, match_path='/match-this-exactly/', match_type='exact', redirect_url='/exact/')
        Redirect.objects.create(is_active=True, group=group, match_path='/match-this-exactly/', match_type='iexact', redirect_url='/iexact/')
        Redirect.objects.create(is_active=True, group=group, match_path='/match-this', match_type='startswith', redirect_url='/startswith/')
        Redirect.objects.create(is_active=True, group=group, match_path='/MATCH-THIS', match_type='istartswith', redirect_url='/istartswith/')
        Redirect.objects.create(is_active=True, group=group, match_path='/match-this-more-exactly', match_type='startswith', redirect_url='/startswith-more-exactly/')
        Redirect.objects.create(is_active=True, group=group, match_path='ends-with/', match_type='endswith', redirect_url='/endswith/')
        Redirect.objects.create(is_active=True, group=group, match_path='ENDS-WITH/', match_type='iendswith', redirect_url='/iendswith/')

    def test_redirects(self):
        pairs = [
         ('/match-this-exactly/', '/exact/'),
         ('/match-this', '/startswith/'),
         ('/match-this-more-exactly', '/startswith-more-exactly/'),
         ('/MATCH-THIS-EXACTLY/', '/iexact/'),
         ('/MATCH-THIS-INEXACTLY', '/istartswith/'),
         ('match-this-ends-with/', '/endswith/'),
         ('MATCH-THIS-ENDS-WITH/', '/iendswith/')]
        for path, target in pairs:
            result = Redirect.objects.get_redirect_for_path(path)
            self.assertEqual(result, target, msg=('Path: {0}, target: {1}, result: {2}').format(path, target, result))

    def test_redirect_startswith_more_exact(self):
        """
        Ensure the more exact startswith matches are prioritized.
        """
        redirect = Redirect.objects.get_redirect_for_path('/match-this-more-exactly')
        self.assertEqual(redirect, '/startswith-more-exactly/')

    def test_redirect_query_cache(self):
        """
        Ensure cache is used - very improtant as this is called on every view
        """
        from django.db import connection
        connection.queries = []
        Redirect.objects.get_redirect_for_path('/match-this-exactly/')
        query_count = len(connection.queries)
        self.assertEqual(0, query_count)

    def test_cache_key_invalidation(self):
        """
        Test cache invalidation on model save/delete.
        """
        original_prefix = generate_cache_prefix()
        redirect = Redirect.objects.latest('id')
        redirect.id = None
        redirect.save()
        post_save_prefix = generate_cache_prefix()
        redirect.delete()
        post_delete_prefix = generate_cache_prefix()
        prefixes = [
         original_prefix, post_save_prefix, post_delete_prefix]
        self.assertEqual(len(set(prefixes)), 3, msg=('Cache prefixes should generate 3 uniques for 3x generations. Got: {0}').format((', ').join(prefixes)))
        return