# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\django_microsip_diot\django_microsip_diot\urls.py
# Compiled at: 2015-11-24 14:59:05
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required
from . import views
urlpatterns = patterns('', (
 '^$', views.index), (
 '^proveedores/$', permission_required('django_microsip_diot.proveedores', login_url='/administrador/permission_required/')(views.ProveedorListView.as_view())), (
 '^proveedor/$', views.ProveedorManageView), (
 '^proveedor/(?P<id>\\d+)/', views.ProveedorManageView), (
 '^create_file/$', views.create_file), (
 '^exporta_xml/$', views.ExportaDiotXML), (
 '^exporta_proveedores/$', views.ExportaProveedoresView), (
 '^crear_paises/$', views.CreaPaisesView), (
 '^paginacion/$', views.PaginationView), (
 '^inicializar/$', views.UpdateDatabaseTable), (
 '^change_xml_status/$', views.change_xml_status), (
 '^pago_parcial/$', views.pago_parcial), (
 '^pago_total/$', views.pago_total), (
 '^inicializar_pagos/$', views.inicializar_pagos), (
 '^captura_manual/$', views.captura_manual), (
 '^ocultar_repo/$', views.ocultar_repo), (
 '^guardar_repositorio/$', views.guardar_repositorio), (
 '^exporta_excel/$', views.exporta_excel), (
 '^genero_ext/$', views.genero_ext), (
 '^preferencias/$', views.preferencias_view), (
 '^importar_xml/$', views.importar_xml), (
 '^cargar_pago/$', views.cargar_pago), (
 '^info_poliza_xml/$', views.info_poliza_xml))