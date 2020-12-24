# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\django-microsip-api\microsip_api\apps\config\urls.py
# Compiled at: 2019-09-09 14:21:49
from django.conf.urls import patterns, url
urlpatterns = patterns('', url('^conexiones/$', 'microsip_api.apps.config.views.conexiones_View'), ('^conexion/(?P<id>\\d+)/',
                                                                                                    'microsip_api.apps.config.views.conexion_manageView'), ('^conexion/delete/(?P<id>\\d+)/',
                                                                                                                                                            'microsip_api.apps.config.views.delete_conexion'), ('^conexion/',
                                                                                                                                                                                                                'microsip_api.apps.config.views.conexion_manageView'), url('^login/$', 'microsip_api.apps.config.views.ingresar'), url('^logout/$', 'microsip_api.apps.config.views.logoutUser'), url('^select_db/$', 'microsip_api.apps.config.views.select_db'))