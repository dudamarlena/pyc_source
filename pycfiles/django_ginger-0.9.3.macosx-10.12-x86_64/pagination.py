# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/tests/pagination.py
# Compiled at: 2014-10-29 05:36:29
import mock, random
from django import test
from django.utils import six
from ginger import utils
from ginger.paginator import GingerPaginator

def parse_url(url):
    parts = six.moves.urllib.parse.urlparse(url)
    return six.moves.urllib.parse.parse_qs(parts.query)


class TestGingerPaginator(test.SimpleTestCase):

    def setUp(self):
        self.factory = test.RequestFactory()

    def request(self, **kwargs):
        return self.factory.get('/', data=kwargs)

    def test_missing_page(self):
        pass

    def test_invalid_page(self):
        pass

    def test_valid_page(self):
        request = self.request()

    def test_constructor(self):
        param = 'pg'
        limit = random.randint(10, 100)
        paginator = GingerPaginator([], per_page=10, page_limit=limit, parameter_name=param)
        self.assertEqual(paginator.page_limit, limit)
        self.assertEqual(paginator.parameter_name, param)

    def test_page(self):
        param = 'pg'
        paginator = GingerPaginator([ i for i in range(100) ], per_page=10, parameter_name=param)
        page_num = random.randint(1, 9)
        req = self.request(**{param: page_num})
        page = paginator.page(req)
        self.assertEqual(page.paginator.parameter_name, param)
        self.assertEqual(page.number, page.number)
        page_links = page.build_links(req)
        self.assertTrue(page_links)