# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tinycms/tests.py
# Compiled at: 2014-11-14 09:25:00
from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from models import *
from views import *
import datetime

class ModellTest(TestCase):

    def setUp(self):
        Dispatcher.clear()
        self.c512 = ''
        for i in range(0, 511):
            self.c512 += 'a'

    def test_model_normal(self):
        testDispatch = {}
        page = Page(slug='test', template='tinycms/shelltest.html', is_active=True)
        page.save()
        page2 = Page(slug='test2', template='tinycms/shelltest.html', parent=page, is_active=True)
        page2.save()
        testDispatch['test/'] = page
        testDispatch['test/test2/'] = page2
        with self.assertRaises(Exception):
            page = Page(slug='test', template='tinycms/shelltest.html', is_active=True)
            page.save()
        page = Page(slug=self.c512, template='tinycms/shelltest.html', is_active=True)
        page.save()
        testDispatch[unicode(self.c512 + '/')] = page
        cont = Content(page=page, value_name='main', language='ja', content='test')
        cont.save()
        Dispatcher.register()
        self.assertEqual(Dispatcher.dispatchURLs, testDispatch)

    def test_slash(self):
        page = Page(slug='/test/', template='tinycms/shelltest.html', is_active=True)
        page.save()
        page2 = Page(slug='/test2/', template='tinycms/shelltest.html', parent=page, is_active=True)
        page2.save()
        page3 = Page(slug='/test3', template='tinycms/shelltest.html', parent=page, is_active=True, url_overwrite='/test3')
        page3.save()
        page4 = Page(slug='/', template='tinycms/shelltest.html', is_active=True)
        page4.save()
        testDispatch = {}
        testDispatch['test/'] = page
        testDispatch['test/test2/'] = page2
        testDispatch['test3'] = page3
        testDispatch[''] = page4
        Dispatcher.register()
        self.assertEqual(Dispatcher.dispatchURLs, testDispatch)

    def test_slash2(self):
        page4 = Page(slug='home', template='tinycms/shelltest.html', is_active=True, url_overwrite='/')
        page4.save()
        testDispatch = {}
        testDispatch[''] = page4
        Dispatcher.register()
        self.assertEqual(Dispatcher.dispatchURLs, testDispatch)


class DummyRequest:

    def __init__(self, user=None, GET={}):
        self.user = user
        self.GET = GET
        self.POST = {}
        self.method = 'GET'


class ViewTest(TestCase):

    def setUp(self):
        Dispatcher.clear()

    def test_content(self):
        page = Page(slug='test', template='tinycms/shelltest.html', is_active=True)
        page.save()
        page2 = Page(slug='test2', template='tinycms/shelltest.html', parent=page, is_active=True)
        page2.save()
        cont = Content(page=page, value_name='main', language='ja', content='test')
        cont.save()
        cont = Content(page=page, value_name='main', language='en', content='test')
        cont.save()
        req = DummyRequest()
        result = show_page(req, 'test/')
        candResult = '<html><body><p>test</p></body></html>'
        self.assertEqual(result.content, candResult)
        with self.assertRaises(Exception):
            result = show_page(req, 'test2/')

    def test_menu(self):
        page = Page(slug='test', template='tinycms/menutest.html', is_active=True)
        page.save()
        page2 = Page(slug='test2', template='tinycms/menutest.html', parent=page, is_active=True)
        page2.save()
        cont = Content(page=page, value_name='main', language='ja', content='test')
        cont.save()
        cont = Content(page=page, value_name='main', language='en', content='test')
        cont.save()
        cont = Content(page=page, value_name='menu_title', language='en', content='test')
        cont.save()
        cont = Content(page=page2, value_name='menu_title', language='en', content='test2')
        cont.save()
        req = DummyRequest()
        result = show_page(req, 'test/')
        candResult = "<html><body><ul><li><a href='/en/test/'>test</a><ul><li><a href='/en/test/test2/'>test2</a></li></ul></li></ul><p>test</p></body></html>"
        self.assertEqual(result.content, candResult)

    def test_slash(self):
        page4 = Page(slug='/', template='tinycms/shelltest.html', is_active=True)
        page4.save()
        cont = Content(page=page4, value_name='main', language='en', content='test')
        cont.save()
        cont = Content(page=page4, value_name='main', language='ja', content='test')
        cont.save()
        Dispatcher.register()
        from django.test import Client
        c = Client()
        response = c.get('/en/')
        self.assertEqual(response.status_code, 200)