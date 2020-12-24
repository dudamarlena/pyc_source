# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/mote/mote/tests/test_views.py
# Compiled at: 2017-04-24 04:30:52
# Size of source mod 2**32: 1007 bytes
from django.core.urlresolvers import reverse
from django.test import TestCase
from mote import models

class ViewsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(ViewsTestCase, cls).setUpTestData()
        cls.project = models.Project('myproject')
        cls.aspect = models.Aspect('website', cls.project)
        cls.pattern = models.Pattern('atoms', cls.aspect)
        cls.element = models.Element('button', cls.pattern)

    def test_element_partial(self):
        url = reverse('mote:element-partial', args=('myproject', 'website', 'atoms',
                                                    'button'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_element_partial_post_request(self):
        response = self.client.post(reverse('mote:element-partial', args=('myproject',
                                                                          'website',
                                                                          'atoms',
                                                                          'button')))
        self.assertEqual(response.status_code, 200)