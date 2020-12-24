# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kyzima-spb/www-python/django-adminlte-full/demo/adminlte_full/urls.py
# Compiled at: 2016-06-19 11:25:45
# Size of source mod 2**32: 1306 bytes
from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
 url('', include('django.contrib.auth.urls')),
 url('^message/(?P<id>\\w+)$', views.index, name='adminlte_full_show_message'),
 url('^messages$', views.index, name='adminlte_full_all_messages'),
 url('^notification/(?P<id>\\w+)$', views.index, name='adminlte_full_show_notification'),
 url('^notifications$', views.index, name='adminlte_full_all_notifications'),
 url('^task/(?P<id>\\w+)$', views.index, name='adminlte_full_show_task'),
 url('^tasks$', views.index, name='adminlte_full_all_tasks'),
 url('^profile$', auth_views.password_change, {'template_name': 'adminlte_full/user/password_change_form.html', 
  'post_change_redirect': 'adminlte_full_profile'}, name='adminlte_full_profile'),
 url('^login$', auth_views.login, {'template_name': 'adminlte_full/user/login.html'}, name='adminlte_full_login'),
 url('^logout$', auth_views.logout_then_login, {'login_url': '/'}, name='adminlte_full_logout')]