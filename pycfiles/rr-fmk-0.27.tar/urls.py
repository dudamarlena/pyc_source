# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rramos/0P/01-dajngo/PAP2/paponline/usuarios/urls.py
# Compiled at: 2018-02-01 13:51:23
from django.conf.urls import url
from django.contrib.auth.views import password_change
from .views import not_found_404, ingresar, salir, cambiarContrasena
urlpatterns = [
 url('^$', ingresar, name='login'),
 url('^logout/', salir, name='logout'),
 url('^cambiar/', cambiarContrasena.as_view(), name='change')]