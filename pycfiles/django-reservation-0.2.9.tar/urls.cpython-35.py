# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luisza/Escritorio/desarrollo/djreservation/djreservation/urls.py
# Compiled at: 2019-02-19 22:11:26
# Size of source mod 2**32: 885 bytes
"""
Created on 1/8/2016

@author: luisza
"""
from __future__ import unicode_literals
try:
    from django.conf.urls import url
except:
    from django.urls import re_path as url

from . import views
from .settings import TOKENIZE
urlpatterns = [
 url('^reservation/create$', views.CreateReservation.as_view(), name='add_user_reservation'),
 url('^reservation/finish$', views.finish_reservation, name='finish_reservation'),
 url('^reservation/delete_product_reservation/(?P<pk>\\d+)$', views.deleteProduct, name='delete_product_reservation'),
 url('reservation/list', views.ReservationList.as_view(), name='reservation_list')]
if TOKENIZE:
    urlpatterns += [
     url('reservation/token/(?P<pk>\\d+)/(?P<token>[0-9a-f-]+)/(?P<status>\\d)$', views.update_reservation_by_token, name='reservation_token')]