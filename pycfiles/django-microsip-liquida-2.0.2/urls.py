# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\django-microsip-liquida\django-microsip-liquida\urls.py
# Compiled at: 2019-09-10 13:06:39
from django.conf.urls import patterns, url
from .views import index, actualiza_nombes_de_carpetas_sellos, UpdateConfigurationDatabase, PreferenciasManageView, DescargarFacturasDelMes, CertificarFacturas, PrepararEmpresasView, ValidarEmpresa, GetEmpresasList
urlpatterns = patterns('', (
 '^$', index), url('^certificar_factura/', CertificarFacturas), url('^validar_empresa/', ValidarEmpresa), url('^get_empresas_list/', GetEmpresasList), url('^descargar_facturas/', DescargarFacturasDelMes), url('^actualiza_nombre_carpetas_sellos/', actualiza_nombes_de_carpetas_sellos), url('^preferencias/inicializar_configuracion/$', UpdateConfigurationDatabase), url('^herramientas/preferencias/$', PreferenciasManageView), url('^transferir_datos/$', PrepararEmpresasView))