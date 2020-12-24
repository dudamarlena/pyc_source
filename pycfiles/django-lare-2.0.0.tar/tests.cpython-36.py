# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonasbraun/Coding/iekadou/django-lare/django_lare/tests.py
# Compiled at: 2018-05-26 09:00:15
# Size of source mod 2**32: 12320 bytes
from __future__ import unicode_literals
from django import VERSION as DJANGO_VERSION
from django.test import TestCase, Client
from django_lare.models import Lare
from django_lare.test_views import *
if DJANGO_VERSION < (1, 10):
    from django.conf.urls import patterns, url
    urlpatterns = patterns('', url('^page1/$', (Page1View.as_view()), name='page_1'), url('^page1/content1/$', (Page1Content1View.as_view()), name='content_1'), url('^page1/content1/inner_content1/$', (Page1Content1InnerContent1View.as_view()), name='inner_content_1'), url('^page1/content1/inner_content2/$', (Page1Content1InnerContent2View.as_view()), name='inner_content_2'), url('^page1/content2/$', (Page1Content2View.as_view()), name='content_2'), url('^page2/$', (Page2View.as_view()), name='page_2'), url('^no-lare-page/$', (NoLareView.as_view()), name='no_lare_page'))
    from django.core.urlresolvers import reverse
else:
    if DJANGO_VERSION <= (2, 0):
        from django.conf.urls import include, url
        urlpatterns = [url('^page1/$', (Page1View.as_view()), name='page_1'),
         url('^page1/content1/$', (Page1Content1View.as_view()), name='content_1'),
         url('^page1/content1/inner_content1/$', (Page1Content1InnerContent1View.as_view()), name='inner_content_1'),
         url('^page1/content1/inner_content2/$', (Page1Content1InnerContent2View.as_view()), name='inner_content_2'),
         url('^page1/content2/$', (Page1Content2View.as_view()), name='content_2'),
         url('^page2/$', (Page2View.as_view()), name='page_2'),
         url('^no-lare-page/$', (NoLareView.as_view()), name='no_lare_page')]
        from django.urls import reverse
    else:
        from django.urls import include, path
        urlpatterns = [
         path('^page1/$', (Page1View.as_view()), name='page_1'),
         path('^page1/content1/$', (Page1Content1View.as_view()), name='content_1'),
         path('^page1/content1/inner_content1/$', (Page1Content1InnerContent1View.as_view()), name='inner_content_1'),
         path('^page1/content1/inner_content2/$', (Page1Content1InnerContent2View.as_view()), name='inner_content_2'),
         path('^page1/content2/$', (Page1Content2View.as_view()), name='content_2'),
         path('^page2/$', (Page2View.as_view()), name='page_2'),
         path('^no-lare-page/$', (NoLareView.as_view()), name='no_lare_page')]
        from django.urls import reverse

class TestLareRequests(TestCase):
    urls = 'django_lare.tests'
    page_1_string = 'page_1'
    content_1_string = 'content_1'
    content_2_string = 'content_2'
    inner_content_1_string = 'inner_con_tent_1'
    inner_content_2_string = 'inner_con_tent_2'
    page_2_string = 'page_2'
    no_lare_page_string = 'no-lare-page'

    def test_page_1_no_lare(self):
        client = Client()
        response = client.get(reverse('page_1'))
        self.assertContains(response, self.page_1_string)
        self.assertContains(response, '<html>')
        self.assertNotContains(response, '<lare-body>')
        self.assertContains(response, 'Site1.Page1')

    def test_page_1_lare_with_namespace(self):
        client = Client()
        response = (client.get)((reverse('page_1')), **{'HTTP_X_LARE': 'Site1.Page2'})
        self.assertContains(response, self.page_1_string)
        self.assertContains(response, '<lare-body>')
        self.assertNotContains(response, '<html>')
        self.assertContains(response, 'Site1.Page1')

    def test_page_1_lare_different_namespace(self):
        client = Client()
        response = (client.get)((reverse('page_1')), **{'HTTP_X_LARE': 'Site2'})
        self.assertContains(response, self.page_1_string)
        self.assertNotContains(response, '<lare-body>')
        self.assertContains(response, '<html>')
        self.assertContains(response, 'Site1.Page1')

    def test_content_1_no_lare(self):
        client = Client()
        response = client.get(reverse('content_1'))
        self.assertContains(response, self.page_1_string)
        self.assertContains(response, self.content_1_string)
        self.assertContains(response, '<html>')
        self.assertNotContains(response, '<lare-body>')
        self.assertContains(response, 'Site1.Page1.Content1')

    def test_content_1_lare_current_namespace(self):
        client = Client()
        response = (client.get)((reverse('content_1')), **{'HTTP_X_LARE': 'Site1.Page1.Content1'})
        self.assertNotContains(response, self.page_1_string)
        self.assertNotContains(response, self.content_1_string)
        self.assertContains(response, '<lare-body>')
        self.assertNotContains(response, '<html>')
        self.assertContains(response, 'Site1.Page1.Content1')

    def test_content_1_lare_page_namespace(self):
        client = Client()
        response = (client.get)((reverse('content_1')), **{'HTTP_X_LARE': 'Site1.Page1'})
        self.assertNotContains(response, self.page_1_string)
        self.assertContains(response, self.content_1_string)
        self.assertContains(response, '<lare-body>')
        self.assertNotContains(response, '<html>')
        self.assertContains(response, 'Site1.Page1.Content1')

    def test_content_1_lare_content_namespace(self):
        client = Client()
        response = (client.get)((reverse('content_1')), **{'HTTP_X_LARE': 'Site1.Page1.Content2'})
        self.assertNotContains(response, self.page_1_string)
        self.assertContains(response, self.content_1_string)
        self.assertContains(response, '<lare-body>')
        self.assertNotContains(response, '<html>')
        self.assertContains(response, 'Site1.Page1.Content1')

    def test_content_1_lare_different_page_namespace(self):
        client = Client()
        response = (client.get)((reverse('content_1')), **{'HTTP_X_LARE': 'Site1.Page2'})
        self.assertContains(response, self.page_1_string)
        self.assertContains(response, self.content_1_string)
        self.assertContains(response, '<lare-body>')
        self.assertNotContains(response, '<html>')
        self.assertContains(response, 'Site1.Page1.Content1')

    def test_content_1_lare_different_site_namespace(self):
        client = Client()
        response = (client.get)((reverse('content_1')), **{'HTTP_X_LARE': 'Site2.Page1'})
        self.assertContains(response, self.page_1_string)
        self.assertContains(response, self.content_1_string)
        self.assertNotContains(response, '<lare-body>')
        self.assertContains(response, '<html>')
        self.assertContains(response, 'Site1.Page1.Content1')

    def test_inner_content_1_no_lare(self):
        client = Client()
        response = client.get(reverse('inner_content_1'))
        self.assertContains(response, self.inner_content_1_string)
        self.assertContains(response, self.content_1_string)
        self.assertContains(response, self.page_1_string)
        self.assertContains(response, '<html>')
        self.assertNotContains(response, '<lare-body>')
        self.assertContains(response, 'Site1.Page1.Content1.InnerContent1')

    def test_inner_content_1_lare_with_namespace(self):
        client = Client()
        response = (client.get)((reverse('inner_content_1')), **{'HTTP_X_LARE': 'Site1.Page1.Content1.InnerContent2'})
        self.assertContains(response, self.inner_content_1_string)
        self.assertNotContains(response, self.content_1_string)
        self.assertNotContains(response, self.page_1_string)
        self.assertContains(response, '<lare-body>')
        self.assertNotContains(response, '<html>')
        self.assertContains(response, 'Site1.Page1.Content1.InnerContent1')

    def test_inner_content_1_lare_different_content_namespace(self):
        client = Client()
        response = (client.get)((reverse('inner_content_1')), **{'HTTP_X_LARE': 'Site1.Page1.Content2'})
        self.assertContains(response, self.inner_content_1_string)
        self.assertContains(response, self.content_1_string)
        self.assertNotContains(response, self.page_1_string)
        self.assertContains(response, '<lare-body>')
        self.assertNotContains(response, '<html>')
        self.assertContains(response, 'Site1.Page1.Content1.InnerContent1')

    def test_inner_content_1_lare_different_page_namespace(self):
        client = Client()
        response = (client.get)((reverse('inner_content_1')), **{'HTTP_X_LARE': 'Site1.Page2'})
        self.assertContains(response, self.inner_content_1_string)
        self.assertContains(response, self.content_1_string)
        self.assertContains(response, self.page_1_string)
        self.assertContains(response, '<lare-body>')
        self.assertNotContains(response, '<html>')
        self.assertContains(response, 'Site1.Page1.Content1.InnerContent1')

    def test_inner_content_1_lare_different_site_namespace(self):
        client = Client()
        response = (client.get)((reverse('inner_content_1')), **{'HTTP_X_LARE': 'Site2.Page1.Content1'})
        self.assertContains(response, self.inner_content_1_string)
        self.assertContains(response, self.content_1_string)
        self.assertContains(response, self.page_1_string)
        self.assertNotContains(response, '<lare-body>')
        self.assertContains(response, '<html>')
        self.assertContains(response, 'Site1.Page1.Content1.InnerContent1')

    def test_old_version(self):
        versions = Lare.supported_version.split('.')
        versions[len(versions) - 1] = '{0}'.format(int(versions[(len(versions) - 1)]) - 1)
        version = '.'.join(versions)
        client = Client()
        response = (client.get)((reverse('inner_content_1')), HTTP_X_LARE_VERSION=version, HTTP_X_LARE='Site1.Page1.Content2')
        self.assertContains(response, self.inner_content_1_string)
        self.assertContains(response, self.content_1_string)
        self.assertContains(response, self.page_1_string)
        self.assertNotContains(response, '<lare-body>')
        self.assertContains(response, '<html>')
        self.assertContains(response, 'Site1.Page1.Content1.InnerContent1')

    def test_future_version(self):
        versions = Lare.supported_version.split('.')
        versions[len(versions) - 1] = '{0}'.format(int(versions[(len(versions) - 1)]) + 1)
        version = '.'.join(versions)
        client = Client()
        response = (client.get)((reverse('inner_content_1')), HTTP_X_LARE_VERSION=version, HTTP_X_LARE='Site1.Page1.Content2')
        self.assertContains(response, self.inner_content_1_string)
        self.assertContains(response, self.content_1_string)
        self.assertNotContains(response, self.page_1_string)
        self.assertContains(response, '<lare-body>')
        self.assertNotContains(response, '<html>')
        self.assertContains(response, 'Site1.Page1.Content1.InnerContent1')

    def test_non_lare_page(self):
        client = Client()
        response = client.get(reverse('no_lare_page'))
        self.assertContains(response, self.no_lare_page_string)
        self.assertContains(response, '<html>')
        self.assertNotContains(response, '<lare-body>')

    def test_non_lare_page_with_namespace(self):
        client = Client()
        response = (client.get)((reverse('no_lare_page')), **{'HTTP_X_LARE': 'Site2.Page1.Content1'})
        self.assertContains(response, self.no_lare_page_string)
        self.assertContains(response, '<html>')
        self.assertNotContains(response, '<lare-body>')