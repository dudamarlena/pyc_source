# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rramos/00P/01-dajngo/3d/app/rr/usuarios/urls.py
# Compiled at: 2018-04-05 10:09:45
# Size of source mod 2**32: 1360 bytes
from django.conf.urls import url
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import password_change
from .views import not_found_404, ingresar, salir, signup, account_activation_sent, activate, change_password, Reiniciar_pass, Reiniciar_pass_ConfirmView
app_name = 'usuarios'
urlpatterns = [
 url('^$', ingresar, name='login'),
 url('^logout/', salir, name='logout'),
 url('^crear/', signup, name='signup'),
 url('^password/$', change_password, name='change_password'),
 url('^account_activation_sent/$', account_activation_sent, name='account_activation_sent'),
 url('^activate/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate,
   name='activate'),
 url('^password_reset/$', (Reiniciar_pass.as_view()), name='password_reset'),
 url('^password_reset/done/$', (auth_views.password_reset_done), name='password_reset_done'),
 url('^reset/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', (Reiniciar_pass_ConfirmView.as_view()),
   name='password_reset_confirm'),
 url('^reset/done/$', (auth_views.password_reset_complete), name='password_reset_complete')]