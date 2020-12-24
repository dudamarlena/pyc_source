# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rramos/_P/02-django/PAP/pap/usuarios/urls.py
# Compiled at: 2017-12-07 13:51:44
# Size of source mod 2**32: 1055 bytes
from django.conf.urls import url
from django.contrib.auth.views import password_change
from .views import not_found_404, ingresar, salir, cambiarContrasena
urlpatterns = [
 url('^$', ingresar, name='login'),
 url('^logout/', salir, name='logout'),
 url('^cambiar/', cambiarContrasena.as_view(), name='change')]