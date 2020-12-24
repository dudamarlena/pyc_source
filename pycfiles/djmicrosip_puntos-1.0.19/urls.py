# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_puntos\djmicrosip_puntos\urls.py
# Compiled at: 2015-06-01 14:40:26
from django.conf.urls import patterns, url
from .views import index, articulo_manageview, ArticuloListView, ClienteListView, ClienteManageView, PreferenciasManageView, GenerarTarjetasView, UpdateDatabaseTable, LineaArticulosListView, GrupoLineasListView, LineaArticulosManageView, GrupoLineasManageView, ClienteTipoListView, ClienteTipoManageView, cliente_searchView, InicializarPuntosArticulosView, TransferirDineroView
urlpatterns = patterns('', (
 '^$', index), (
 '^articulo/$', articulo_manageview), (
 '^articulo/(?P<id>\\d+)/', articulo_manageview), (
 '^articulos/$', ArticuloListView.as_view()), (
 '^tipos_cliente/$', ClienteTipoListView.as_view()), (
 '^tipo_cliente/$', ClienteTipoManageView), (
 '^tipo_cliente/(?P<id>\\d+)/', ClienteTipoManageView), (
 '^linea/$', LineaArticulosManageView), (
 '^linea/(?P<id>\\d+)/', LineaArticulosManageView), (
 '^grupo/$', GrupoLineasManageView), (
 '^grupo/(?P<id>\\d+)/', GrupoLineasManageView), (
 '^lineas/$', LineaArticulosListView.as_view()), (
 '^grupos/$', GrupoLineasListView.as_view()), (
 '^cliente/$', ClienteManageView), (
 '^cliente/(?P<id>\\d+)/', ClienteManageView), (
 '^clientes/$', ClienteListView.as_view()), (
 '^preferencias/$', PreferenciasManageView), (
 '^generar_tarjetas/$', GenerarTarjetasView), (
 '^dar_puntosdinero/$', TransferirDineroView), (
 '^preferencias/actualizar_tablas/$', UpdateDatabaseTable), (
 '^inicializar_puntos_articulos/$', InicializarPuntosArticulosView), (
 '^cliente_search/', cliente_searchView), (
 '^cliente_search/(?P<id>\\d+)/', cliente_searchView))