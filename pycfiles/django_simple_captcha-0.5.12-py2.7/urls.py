# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/captcha/urls.py
# Compiled at: 2017-11-09 06:15:12
from django.conf.urls import url
from captcha import views
urlpatterns = [
 url('image/(?P<key>\\w+)/$', views.captcha_image, name='captcha-image', kwargs={'scale': 1}),
 url('image/(?P<key>\\w+)@2/$', views.captcha_image, name='captcha-image-2x', kwargs={'scale': 2}),
 url('audio/(?P<key>\\w+).wav$', views.captcha_audio, name='captcha-audio'),
 url('refresh/$', views.captcha_refresh, name='captcha-refresh')]