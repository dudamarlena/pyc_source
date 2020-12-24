# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-ultracache/ultracache/tests/test_base.py
# Compiled at: 2019-05-31 04:25:16
from django import template
from django.conf import settings
from django.core.cache import cache
from django.http.cookie import SimpleCookie
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.test.utils import override_settings
from django.urls import reverse
from ultracache import _thread_locals
from ultracache.tests.models import DummyModel, DummyForeignModel, DummyOtherModel
from ultracache.tests import views
from ultracache.tests.utils import dummy_proxy

class TemplateTagsTestCase(TestCase):
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        fixtures = [
         'sites.json']

    @classmethod
    def setUpClass(cls):
        super(TemplateTagsTestCase, cls).setUpClass()
        cls.factory = RequestFactory()
        cls.request = cls.factory.get('/')
        cache.clear()
        dummy_proxy.clear()

    if 'django.contrib.sites' in settings.INSTALLED_APPS:

        def test_sites(self):
            from django.contrib.sites.models import Site
            first_site = Site.objects.all().first()
            second_site = Site.objects.all().last()
            t = template.Template("{% load ultracache_tags %}                {% ultracache 1200 'test_ultracache' %}1{% endultracache %}")
            context = template.Context({'request': self.request})
            result1 = t.render(context)
            t = template.Template("{% load ultracache_tags %}                {% ultracache 1200 'test_ultracache' %}2{% endultracache %}")
            context = template.Context({'request': self.request})
            result2 = t.render(context)
            self.failUnlessEqual(result1, result2)
            t = template.Template("{% load ultracache_tags %}                {% ultracache 1200 'test_ultracache' %}1{% endultracache %}")
            context = template.Context({'request': self.request})
            result1 = t.render(context)
            with override_settings(SITE_ID=second_site.id):
                t = template.Template("{%% load ultracache_tags %%}                    {%% ultracache 1200 'test_ultracache' %%}%s{%% endultracache %%}" % second_site.id)
                context = template.Context({'request': self.request})
                result2 = t.render(context)
                self.failIfEqual(result1, result2)

    def test_variables(self):
        t = template.Template("{% load ultracache_tags %}            {% ultracache 1200 'test_ultracache_undefined' aaa %}1{% endultracache %}")
        context = template.Context({'request': self.request})
        result1 = t.render(context)
        t = template.Template("{% load ultracache_tags %}            {% ultracache 1200 'test_ultracache_undefined' bbb %}2{% endultracache %}")
        context = template.Context({'request': self.request})
        result2 = t.render(context)
        self.failUnlessEqual(result1, result2)
        t = template.Template("{% load ultracache_tags %}            {% ultracache 1200 'test_ultracache_xlt' _('aaa') %}1{% endultracache %}")
        context = template.Context({'request': self.request})
        result1 = t.render(context)
        t = template.Template("{% load ultracache_tags %}            {% ultracache 1200 'test_ultracache_xlt' _('aaa') %}2{% endultracache %}")
        context = template.Context({'request': self.request})
        result2 = t.render(context)
        self.failUnlessEqual(result1, result2)
        t = template.Template("{% load ultracache_tags %}            {% ultracache 1200 'test_ultracache_large' 565417614189797377 %}abcde{% endultracache %}")
        context = template.Context({'request': self.request})
        result1 = t.render(context)
        t = template.Template("{% load ultracache_tags %}            {% ultracache 1200 'test_ultracache_large' 565417614189797377 %}abcde{% endultracache %}")
        context = template.Context({'request': self.request})
        result2 = t.render(context)
        self.failUnlessEqual(result1, result2)

    def test_context_without_request(self):
        t = template.Template("{% load ultracache_tags %}            {% ultracache 1200 'test_ultracache_undefined' aaa %}abcde{% endultracache %}")
        context = template.Context()
        self.assertRaises(KeyError, t.render, context)

    def test_invalidation(self):
        """Directly render template
        """
        one = DummyModel.objects.create(title='One', code='one')
        two = DummyModel.objects.create(title='Two', code='two')
        three = DummyForeignModel.objects.create(title='Three', points_to=one, code='three')
        four = DummyOtherModel.objects.create(title='Four', code='four')
        t = template.Template('{% load ultracache_tags ultracache_test_tags %}\n            {% ultracache 1200 \'test_ultracache_invalidate_outer\' %}\n                    counter outer = {{ counter }}\n                {% ultracache 1200 \'test_ultracache_invalidate_one\' %}\n                    title = {{ one.title }}\n                    counter one = {{ counter }}\n                {% endultracache %}\n                {% ultracache 1200 \'test_ultracache_invalidate_two\' %}\n                    title = {{ two.title }}\n                    counter two = {{ counter }}\n                {% endultracache %}\n                {% ultracache 1200 \'test_ultracache_invalidate_three\' %}\n                    title = {{ three.title }}\n                    {{ three.points_to.title }}\n                    counter three = {{ counter }}\n                {% endultracache %}\n                {% ultracache 1200 \'test_ultracache_invalidate_render_view\' %}\n                    {% render_view \'render-view\' %}\n                {% endultracache %}\n                {% ultracache 1200 \'test_ultracache_invalidate_include %}\n                    {% include "ultracache/include_me.html" %}\n                {% endultracache %}\n            {% endultracache %}')
        request = self.factory.get('/aaa/')
        context = template.Context({'request': request, 
           'one': one, 
           'two': two, 
           'three': three, 
           'counter': 1})
        result = t.render(context)
        dummy_proxy.cache(request, result)
        self.failUnless('title = One' in result)
        self.failUnless('title = Two' in result)
        self.failUnless('counter outer = 1' in result)
        self.failUnless('counter one = 1' in result)
        self.failUnless('counter two = 1' in result)
        self.failUnless('counter three = 1' in result)
        self.failUnless('render_view = One' in result)
        self.failUnless('include = One' in result)
        self.failUnless(dummy_proxy.is_cached('/aaa/'))
        one.title = 'Onxe'
        one.save()
        request = self.factory.get('/bbb/')
        context = template.Context({'request': request, 
           'one': one, 
           'two': two, 
           'three': three, 
           'counter': 2})
        result = t.render(context)
        dummy_proxy.cache(request, result)
        self.failUnless('title = Onxe' in result)
        self.failIf('title = One' in result)
        self.failUnless('title = Two' in result)
        self.failUnless('counter outer = 2' in result)
        self.failUnless('counter one = 2' in result)
        self.failUnless('counter two = 1' in result)
        self.failUnless('counter three = 2' in result)
        self.failUnless('render_view = Onxe' in result)
        self.failUnless('include = Onxe' in result)
        self.failIf(dummy_proxy.is_cached('/aaa/'))
        two.title = 'Twxo'
        two.save()
        request = self.factory.get('/ccc/')
        context = template.Context({'request': request, 
           'one': one, 
           'two': two, 
           'three': three, 
           'counter': 3})
        result = t.render(context)
        dummy_proxy.cache(request, result)
        self.failUnless('title = Onxe' in result)
        self.failIf('title = One' in result)
        self.failUnless('title = Twxo' in result)
        self.failIf('title = Two' in result)
        self.failUnless('counter outer = 3' in result)
        self.failUnless('counter one = 2' in result)
        self.failUnless('counter two = 3' in result)
        self.failUnless('counter three = 2' in result)
        self.failUnless('render_view = Onxe' in result)
        self.failUnless('include = Onxe' in result)
        self.failIf(dummy_proxy.is_cached('/bbb/'))
        three.title = 'Threxe'
        three.save()
        request = self.factory.get('/ddd/')
        context = template.Context({'request': request, 
           'one': one, 
           'two': two, 
           'three': three, 
           'counter': 4})
        result = t.render(context)
        dummy_proxy.cache(request, result)
        self.failUnless('title = Onxe' in result)
        self.failIf('title = One' in result)
        self.failUnless('title = Twxo' in result)
        self.failIf('title = Two' in result)
        self.failUnless('title = Threxe' in result)
        self.failIf('title = Three' in result)
        self.failUnless('counter outer = 4' in result)
        self.failUnless('counter one = 2' in result)
        self.failUnless('counter two = 3' in result)
        self.failUnless('counter three = 4' in result)
        self.failUnless('render_view = Onxe' in result)
        self.failUnless('include = Onxe' in result)
        self.failIf(dummy_proxy.is_cached('/ccc/'))
        five = DummyOtherModel.objects.create(title='Five', code='five')
        request = self.factory.get('/eee/')
        context = template.Context({'request': request, 
           'one': one, 
           'two': two, 
           'three': three, 
           'counter': 5})
        result = t.render(context)
        dummy_proxy.cache(request, result)
        self.failUnless('render_view = Five' in result)
        self.failUnless('counter outer = 5' in result)
        self.failUnless('counter one = 2' in result)
        self.failUnless('counter two = 3' in result)
        self.failUnless('counter three = 4' in result)
        self.failIf(dummy_proxy.is_cached('/ddd/'))
        two.delete()
        request = self.factory.get('/fff/')
        context = template.Context({'request': request, 
           'one': one, 
           'two': None, 
           'three': three, 
           'counter': 6})
        result = t.render(context)
        dummy_proxy.cache(request, result)
        self.failUnless('title = Onxe' in result)
        self.failIf('title = Twxo' in result)
        self.failIf('title = Two' in result)
        self.failUnless('counter outer = 6' in result)
        self.failUnless('counter one = 2' in result)
        self.failUnless('counter two = 6' in result)
        self.failUnless('counter three = 4' in result)
        self.failIf(dummy_proxy.is_cached('/eee/'))
        return


class DecoratorTestCase(TestCase):
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        fixtures = [
         'sites.json']

    def setUp(self):
        super(DecoratorTestCase, self).setUp()
        cache.clear()
        dummy_proxy.clear()
        if hasattr(_thread_locals, 'ultracache_recorder'):
            delattr(_thread_locals, 'ultracache_recorder')

    def test_method(self):
        """Render template through a view with get method decorated with
        cached_get."""
        one = DummyModel.objects.create(title='One', code='one')
        two = DummyModel.objects.create(title='Two', code='two')
        three = DummyForeignModel.objects.create(title='Three', points_to=one, code='three')
        four = DummyModel.objects.create(title='Four', code='four')
        five = DummyModel.objects.create(title='Five', code='five')
        url = reverse('method-cached-view')
        cache.set('counter', 1)
        response = self.client.get(url)
        result = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.failUnless('title = One' in result)
        self.failUnless('title = Two' in result)
        self.failUnless('title = Three' in result)
        self.failUnless('render_view = One' in result)
        self.failUnless('include = One' in result)
        self.failUnless('counter one = 1' in result)
        self.failUnless('counter two = 1' in result)
        self.failUnless('counter three = 1' in result)
        self.failUnless('counter four = 1' in result)
        self.failUnless('title = Four' in result)
        cache.set('counter', 2)
        one.title = 'Onxe'
        one.save()
        response = self.client.get(url)
        result = response.content.decode('utf-8')
        self.failUnless('title = Onxe' in result)
        self.failIf('title = One' in result)
        self.failUnless('title = Two' in result)
        self.failUnless('title = Three' in result)
        self.failUnless('render_view = Onxe' in result)
        self.failUnless('include = Onxe' in result)
        self.failUnless('counter one = 2' in result)
        self.failUnless('counter two = 1' in result)
        self.failUnless('counter three = 2' in result)
        self.failUnless('counter four = 2' in result)
        self.failUnless('title = Four' in result)
        cache.set('counter', 3)
        two.title = 'Twxo'
        two.save()
        response = self.client.get(url)
        result = response.content.decode('utf-8')
        self.failUnless('title = Onxe' in result)
        self.failIf('title = One' in result)
        self.failUnless('title = Twxo' in result)
        self.failIf('title = Two' in result)
        self.failUnless('title = Three' in result)
        self.failUnless('render_view = Onxe' in result)
        self.failUnless('include = Onxe' in result)
        self.failUnless('counter one = 2' in result)
        self.failUnless('counter two = 3' in result)
        self.failUnless('counter three = 2' in result)
        self.failUnless('counter four = 3' in result)
        self.failUnless('title = Four' in result)
        cache.set('counter', 4)
        three.title = 'Threxe'
        three.save()
        response = self.client.get(url)
        result = response.content.decode('utf-8')
        self.failUnless('title = Onxe' in result)
        self.failIf('title = One' in result)
        self.failUnless('title = Twxo' in result)
        self.failIf('title = Two' in result)
        self.failUnless('title = Threxe' in result)
        self.failIf('title = Three' in result)
        self.failUnless('render_view = Onxe' in result)
        self.failUnless('include = Onxe' in result)
        self.failUnless('counter one = 2' in result)
        self.failUnless('counter two = 3' in result)
        self.failUnless('counter three = 4' in result)
        self.failUnless('counter four = 4' in result)
        self.failUnless('title = Four' in result)
        cache.set('counter', 5)
        four.title = 'Fouxr'
        four.save()
        response = self.client.get(url)
        result = response.content.decode('utf-8')
        self.failUnless('title = Onxe' in result)
        self.failIf('title = One' in result)
        self.failUnless('title = Twxo' in result)
        self.failIf('title = Two' in result)
        self.failUnless('title = Threxe' in result)
        self.failIf('title = Three' in result)
        self.failUnless('counter one = 2' in result)
        self.failUnless('counter two = 3' in result)
        self.failUnless('counter three = 4' in result)
        self.failUnless('counter four = 5' in result)
        self.failUnless('render_view = Onxe' in result)
        self.failUnless('include = Onxe' in result)
        self.failUnless('title = Fouxr' in result)
        self.failIf('title = Four' in result)
        cache.set('counter', 6)
        five.title = 'Fivxe'
        five.save()
        response = self.client.get(url)
        result = response.content.decode('utf-8')
        self.failUnless('title = Onxe' in result)
        self.failIf('title = One' in result)
        self.failUnless('title = Twxo' in result)
        self.failIf('title = Two' in result)
        self.failUnless('title = Threxe' in result)
        self.failIf('title = Three' in result)
        self.failUnless('counter one = 2' in result)
        self.failUnless('counter two = 3' in result)
        self.failUnless('counter three = 4' in result)
        self.failUnless('counter four = 6' in result)
        self.failUnless('counter five = 6' in result)
        self.failUnless('render_view = Onxe' in result)
        self.failUnless('include = Onxe' in result)
        self.failUnless('title = Fouxr' in result)
        self.failIf('title = Four' in result)

    def test_class(self):
        """Render template through a view decorated with ultracache
        """
        one = DummyModel.objects.create(title='One', code='one')
        two = DummyModel.objects.create(title='Two', code='two')
        three = DummyForeignModel.objects.create(title='Three', points_to=one, code='three')
        four = DummyModel.objects.create(title='Four', code='four')
        five = DummyModel.objects.create(title='Five', code='five')
        url = reverse('class-cached-view')
        cache.set('counter', 1)
        response = self.client.get(url)
        result = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.failUnless('title = One' in result)
        self.failUnless('title = Two' in result)
        self.failUnless('title = Three' in result)
        self.failUnless('render_view = One' in result)
        self.failUnless('include = One' in result)
        self.failUnless('counter one = 1' in result)
        self.failUnless('counter two = 1' in result)
        self.failUnless('counter three = 1' in result)
        self.failUnless('counter four = 1' in result)
        self.failUnless('title = Four' in result)
        cache.set('counter', 2)
        one.title = 'Onxe'
        one.save()
        response = self.client.get(url)
        result = response.content.decode('utf-8')
        self.failUnless('title = Onxe' in result)
        self.failIf('title = One' in result)
        self.failUnless('title = Two' in result)
        self.failUnless('title = Three' in result)
        self.failUnless('render_view = Onxe' in result)
        self.failUnless('include = Onxe' in result)
        self.failUnless('counter one = 2' in result)
        self.failUnless('counter two = 1' in result)
        self.failUnless('counter three = 2' in result)
        self.failUnless('counter four = 2' in result)
        self.failUnless('title = Four' in result)
        cache.set('counter', 3)
        two.title = 'Twxo'
        two.save()
        response = self.client.get(url)
        result = response.content.decode('utf-8')
        self.failUnless('title = Onxe' in result)
        self.failIf('title = One' in result)
        self.failUnless('title = Twxo' in result)
        self.failIf('title = Two' in result)
        self.failUnless('title = Three' in result)
        self.failUnless('render_view = Onxe' in result)
        self.failUnless('include = Onxe' in result)
        self.failUnless('counter one = 2' in result)
        self.failUnless('counter two = 3' in result)
        self.failUnless('counter three = 2' in result)
        self.failUnless('counter four = 3' in result)
        self.failUnless('title = Four' in result)
        cache.set('counter', 4)
        three.title = 'Threxe'
        three.save()
        response = self.client.get(url)
        result = response.content.decode('utf-8')
        self.failUnless('title = Onxe' in result)
        self.failIf('title = One' in result)
        self.failUnless('title = Twxo' in result)
        self.failIf('title = Two' in result)
        self.failUnless('title = Threxe' in result)
        self.failIf('title = Three' in result)
        self.failUnless('render_view = Onxe' in result)
        self.failUnless('include = Onxe' in result)
        self.failUnless('counter one = 2' in result)
        self.failUnless('counter two = 3' in result)
        self.failUnless('counter three = 4' in result)
        self.failUnless('counter four = 4' in result)
        self.failUnless('title = Four' in result)
        cache.set('counter', 5)
        four.title = 'Fouxr'
        four.save()
        response = self.client.get(url)
        result = response.content.decode('utf-8')
        self.failUnless('title = Onxe' in result)
        self.failIf('title = One' in result)
        self.failUnless('title = Twxo' in result)
        self.failIf('title = Two' in result)
        self.failUnless('title = Threxe' in result)
        self.failIf('title = Three' in result)
        self.failUnless('counter one = 2' in result)
        self.failUnless('counter two = 3' in result)
        self.failUnless('counter three = 4' in result)
        self.failUnless('counter four = 5' in result)
        self.failUnless('render_view = Onxe' in result)
        self.failUnless('include = Onxe' in result)
        self.failUnless('title = Fouxr' in result)
        self.failIf('title = Four' in result)
        cache.set('counter', 6)
        five.title = 'Fivxe'
        five.save()
        response = self.client.get(url)
        result = response.content.decode('utf-8')
        self.failUnless('title = Onxe' in result)
        self.failIf('title = One' in result)
        self.failUnless('title = Twxo' in result)
        self.failIf('title = Two' in result)
        self.failUnless('title = Threxe' in result)
        self.failIf('title = Three' in result)
        self.failUnless('counter one = 2' in result)
        self.failUnless('counter two = 3' in result)
        self.failUnless('counter three = 4' in result)
        self.failUnless('counter four = 6' in result)
        self.failUnless('counter five = 6' in result)
        self.failUnless('render_view = Onxe' in result)
        self.failUnless('include = Onxe' in result)
        self.failUnless('title = Fouxr' in result)
        self.failIf('title = Four' in result)

    def test_header(self):
        """Test that decorator preserves headers
        """
        url = reverse('cached-header-view')
        response = self.client.get(url)
        self.assertEqual(response._headers['content-type'], ('Content-Type', 'application/json'))
        self.assertEqual(response._headers['foo'], ('foo', 'bar'))
        response = self.client.get(url)
        self.assertEqual(response._headers['content-type'], ('Content-Type', 'application/json'))
        self.assertEqual(response._headers['foo'], ('foo', 'bar'))

    def test_cache_busting(self):
        """Test cache busting with and without random querystring param
        """
        url = reverse('bustable-cached-view')
        response = self.client.get(url + '?aaa=1')
        self.failUnless('aaa=1' in response.content.decode('utf-8'))
        response = self.client.get(url + '?aaa=2')
        self.failUnless('aaa=2' in response.content.decode('utf-8'))
        url = reverse('non-bustable-cached-view')
        response = self.client.get(url + '?aaa=1')
        self.failUnless('aaa=1' in response.content.decode('utf-8'))
        response = self.client.get(url + '?aaa=2')
        self.failIf('aaa=2' in response.content.decode('utf-8'))