# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/est/src/django-trumbowyg/trumbowyg/urls.py
# Compiled at: 2017-03-07 08:28:38
from django.conf.urls import url
from trumbowyg.views import upload_image
urlpatterns = [
 url('^upload_image/$', upload_image, name='trumbowyg_upload_image')]