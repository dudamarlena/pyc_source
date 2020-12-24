# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scaler/tests.py
# Compiled at: 2012-05-31 03:57:34
import time
from django.test import TestCase
from django.test.client import Client
from django.core.files import File as DjangoFile
from django.core.urlresolvers import reverse
from django.conf import settings

class ScalerTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def reset_settings(self):
        settings.DJANGO_SCALER['redirect_n_slowest_function'] = lambda : 0
        settings.DJANGO_SCALER['redirect_percentage_slowest_function'] = lambda : 0
        settings.DJANGO_SCALER['redirect_regexes_function'] = lambda : []

    def test_auto_scaler(self):
        """Middleware redirects requests by itself"""
        self.reset_settings()
        for i in range(0, 20):
            response = self.client.get('/?delay=0.1')
            self.assertEqual(response.status_code, 200)

        for i in range(0, 10):
            response = self.client.get('/?delay=1.0')
            if response.status_code == 302:
                stamp = time.time()

        self.assertEqual(response.status_code, 302)
        now = time.time()
        while now - settings.DJANGO_SCALER['redirect_for'] < stamp:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 302)
            time.sleep(2)
            now = time.time()

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_excplicit_scaler_n_slowest(self):
        """Middleware is instructed to redirect X slowest URLs"""
        self.reset_settings()
        for i in range(0, 20):
            response = self.client.get('/?delay=0.1')
            self.assertEqual(response.status_code, 200)
            response = self.client.get('/scaler-test-one/?delay=0.3')
            self.assertEqual(response.status_code, 200)
            response = self.client.get('/scaler-test-two/?delay=0.5')
            self.assertEqual(response.status_code, 200)

        settings.DJANGO_SCALER['redirect_n_slowest_function'] = lambda : 2
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/scaler-test-one/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/scaler-test-two/')
        self.assertEqual(response.status_code, 302)

    def test_excplicit_scaler_percentage_slowest(self):
        """Middleware is instructed to redirect % slowest URLs"""
        self.reset_settings()
        for i in range(0, 20):
            response = self.client.get('/?delay=0.1')
            self.assertEqual(response.status_code, 200)
            response = self.client.get('/scaler-test-one/?delay=0.3')
            self.assertEqual(response.status_code, 200)
            response = self.client.get('/scaler-test-two/?delay=0.5')
            self.assertEqual(response.status_code, 200)

        settings.DJANGO_SCALER['redirect_percentage_slowest_function'] = lambda : 67
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/scaler-test-one/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/scaler-test-two/')
        self.assertEqual(response.status_code, 302)

    def test_excplicit_scaler_regexes(self):
        """Middleware is instructed to redirect if URL matches a regex in
        list."""
        self.reset_settings()
        settings.DJANGO_SCALER['redirect_regexes_function'] = lambda : [
         '/scaler-test-o', '/scaler-test-t']
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/scaler-test-one/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/scaler-test-two/')
        self.assertEqual(response.status_code, 302)