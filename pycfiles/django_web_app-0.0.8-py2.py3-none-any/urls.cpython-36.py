# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\work\work\PycharmProjects\UpcwangyingWebApp\web_app\urls.py
# Compiled at: 2018-08-01 08:28:52
# Size of source mod 2**32: 252 bytes
__author__ = 'WANGY'
__date__ = '2018/8/1 19:03'
from django.conf.urls import url, include
from .views.index import IndexView
urlpatterns = [
 url('^web/app/index/$', (IndexView.as_view()), name='web_app_index')]