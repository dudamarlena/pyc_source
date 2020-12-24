# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/composer/tests/test_middleware.py
# Compiled at: 2017-10-23 07:42:35
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase
from composer.models import Slot, Row, Column, Tile

class MiddleWareTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(MiddleWareTestCase, cls).setUpTestData()
        cls.slot = Slot.objects.create(slot_name='content', url='/not-a-four-o-four/')
        cls.slot.sites = Site.objects.all()
        cls.slot.save()
        cls.tile = Tile.objects.create(column=Column.objects.create(row=Row.objects.create(slot=cls.slot)))
        cls.tile.view_name = 'header'
        cls.tile.save()

    def test_404(self):
        response = self.client.get('/not-a-four-o-four/')
        self.assertHTMLEqual('\n        <div id="header">\n            Header slot\n        </div>\n        <div id="content">\n            <div class="composer-row None">\n                <div class="composer-column composer-column-8 None">\n                    <div class="composer-tile None" data-oid="%s">\n                        I am the header\n                    </div>\n                </div>\n            </div>\n        </div>\n        <div id="footer">\n            Footer slot\n        </div>' % self.tile.id, response.content)

    def test_404_no_slash(self):
        response = self.client.get('/not-a-four-o-four')
        self.assertRedirects(response, '/not-a-four-o-four/', status_code=301, target_status_code=200, fetch_redirect_response=True)

    def test_404_no_slash_no_redirect(self):
        with self.settings(APPEND_SLASH=False):
            response = self.client.get('/not-a-four-o-four')
            self.assertEqual(response.status_code, 404)

    def test_request_method_types(self):
        response = self.client.options('/not-a-four-o-four/')
        self.assertEqual(response.status_code, 200)
        response = self.client.options('/does-not-exist/')
        self.assertEqual(response.status_code, 404)
        response = self.client.put('/does-not-exist/')
        self.assertEqual(response.status_code, 405)
        response = self.client.put('/not-a-four-o-four/')
        self.assertEqual(response.status_code, 405)
        response = self.client.patch('/does-not-exist/')
        self.assertEqual(response.status_code, 405)
        response = self.client.patch('/not-a-four-o-four/')
        self.assertEqual(response.status_code, 405)
        response = self.client.get('/does-not-exist/')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/not-a-four-o-four/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/does-not-exist/')
        self.assertEqual(response.status_code, 405)
        response = self.client.post('/not-a-four-o-four/')
        self.assertEqual(response.status_code, 405)
        response = self.client.delete('/does-not-exist/')
        self.assertEqual(response.status_code, 405)
        response = self.client.delete('/not-a-four-o-four/')
        self.assertEqual(response.status_code, 405)
        response = self.client.head('/does-not-exist/')
        self.assertEqual(response.status_code, 404)
        response = self.client.head('/not-a-four-o-four/')
        self.assertEqual(response.status_code, 200)
        response = self.client.trace('/does-not-exist/')
        self.assertEqual(response.status_code, 405)
        response = self.client.trace('/not-a-four-o-four/')
        self.assertEqual(response.status_code, 405)