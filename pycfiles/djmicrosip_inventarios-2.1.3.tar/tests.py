# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_inventarios\djmicrosip_inventarios\tests.py
# Compiled at: 2019-09-17 20:26:23
from django.test import TestCase
from django.test.client import RequestFactory
from django_microsip_base.libs.models_base.models import Almacen, Articulo
from .models import LogInventario
import json

class CargosClientesTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client.post('/login/', {'username': 'SYSDBA', 'password': '1', 'conexion_db': '1'})
        self.almacen = Almacen.objects.get(es_predet='S')
        if self.almacen.inventariando:
            self.client.get('/inventarios/close_inventario_byalmacen_view/', {'almacen_id': self.almacen.ALMACEN_ID})
        self.almacen.inventariando = True
        LogInventario.objects.create(almacen=self.almacen)
        self.almacen.inventario_conajustes = True
        self.almacen.save(update_fields=['inventariando', 'inventario_conajustes'])

    def test_muestra_si_ya_se_conto_un_articulo(self):
        """
        mustra correctamente si ya se conto un articulo
        """
        from core.views import ajustes_get_or_create
        articulo = Articulo.objects.filter(es_almacenable='S', estatus='A', seguimiento='N')[0]
        existencia = articulo.get_existencia(almacen_nombre=self.almacen.nombre)
        entrada, salida = ajustes_get_or_create(almacen_id=self.almacen.ALMACEN_ID)
        self.client.get('/inventarios/agregar_existencia/', {'entrada_id': entrada.id, 
           'salida_id': salida.id, 
           'ubicacion': 'general', 
           'serie': '', 
           'unidades': existencia, 
           'articulo_id': articulo.id, 
           'almacen_nombre': self.almacen.nombre, 
           'tipo_seguimiento': articulo.seguimiento})
        resp = self.client.get('/inventarios/get_existencia_articulo/', {'almacen': self.almacen.nombre, 
           'articulo_id': articulo.id, 
           'serie': ''})
        resp = json.loads(resp.content)
        self.assertEqual(resp['ya_ajustado'], True, msg='Al insertar una existencia igual a la real y checar si esta contad, me dice que no esta contado.')