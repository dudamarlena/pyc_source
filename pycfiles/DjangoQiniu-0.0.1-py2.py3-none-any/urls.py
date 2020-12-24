# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangyong/my_development/python/django_pro/bookstore/DjangoQiniu/urls.py
# Compiled at: 2017-05-09 04:45:14
from django.conf.urls import url
from .views import qiniu_token
urlpatterns = [
 url('qiniu_token/', qiniu_token, name='qiniu_token')]