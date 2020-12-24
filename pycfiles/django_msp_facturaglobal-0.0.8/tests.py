# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\django_msp_facturaglobal\django_msp_facturaglobal\tests.py
# Compiled at: 2014-12-10 15:06:48
import pytest

@pytest.mark.django_db
class RegistroAccesoTest:

    def test_view(self, client):
        response = client.get('/factura_global_app/generar_factura_global')
        assert response.status_code == 200