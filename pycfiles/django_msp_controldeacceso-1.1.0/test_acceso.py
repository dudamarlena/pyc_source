# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_msp_controldeacceso\django_msp_controldeacceso\test_acceso.py
# Compiled at: 2016-02-15 12:30:53
from .models import RegistroAcceso, Cliente
import datetime, pytest

@pytest.mark.django_db
class TestAcceso:

    def test_cliente_selectfirst(self):
        cliente1 = Cliente.objects.all()[0]
        assert isinstance(cliente1, Cliente)