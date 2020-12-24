# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\django_msp_facturaglobal\django_msp_facturaglobal\test_facturas.py
# Compiled at: 2014-12-10 15:06:48
import pytest
from django.test import Client

@pytest.mark.django_db
class TestFacturas:
    urls = 'django_microsip_base.test_urls'

    def test_view(self):
        x = 200
        assert x == 200

    def test_with_client(self):
        c = Client()
        response = c.get('/')
        assert response.status_code == 200