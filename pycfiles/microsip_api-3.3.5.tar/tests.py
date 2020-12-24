# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\django-microsip-api\microsip_api\apps\commun\articulos\articulos\tests.py
# Compiled at: 2019-09-09 14:21:49
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase

class ArticulosViewsTestCase(TestCase):

    def test_articulos(self):
        resp = self.client.get('/punto_de_venta/articulos/')
        self.assertEqual(resp.status_code, 200)