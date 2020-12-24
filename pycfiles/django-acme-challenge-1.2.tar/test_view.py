# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ec2-user/environment/django-acme-challenge/acme_challenge/tests/test_view.py
# Compiled at: 2018-04-02 16:16:06
"""
    Simple test to confirm that the view shows what it should when it should
"""
from django.test import TestCase, Client
from django.conf import settings
__all__ = ('ViewTest', )
SLUG = 'test'
CONTENT = 'test content'

class ViewTest(TestCase):

    def setUp(self):
        """
            Set the settings variables
        """
        settings.ACME_CHALLENGE_URL_SLUG = SLUG
        settings.ACME_CHALLENGE_TEMPLATE_CONTENT = CONTENT

    def testView(self):
        c = Client()
        response = c.get('/%s' % SLUG)
        self.assertEqual(response.content.decode(), CONTENT)
        response = c.get('/test2')
        self.assertEqual(response.status_code, 404)