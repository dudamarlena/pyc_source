# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/django-markdownx/markdownx/tests/tests.py
# Compiled at: 2019-12-26 17:56:56
# Size of source mod 2**32: 1059 bytes
import os, re
from django.test import TestCase
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

class SimpleTest(TestCase):

    def test_me(self):
        response = self.client.get('/testview/')
        self.assertEqual(response.status_code, 200)

    def test_upload(self):
        url = reverse('markdownx_upload')
        with open('markdownx/tests/static/django-markdownx-preview.png', 'rb') as (fp):
            response = self.client.post(url, {'image': fp}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        try:
            json = response.json()
        except AttributeError:
            import json
            json = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('image_code', json)
        match = re.findall('(markdownx/[\\w\\-]+\\.png)', json['image_code'])
        try:
            if match:
                os.remove(match[0])
        except OSError:
            pass