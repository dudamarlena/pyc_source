# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vwa13376/workspace/uploader/archer/urls.py
# Compiled at: 2013-08-12 11:06:04
from django.conf.urls import patterns, include, url
from django.contrib import admin
from archer.projects import views
admin.autodiscover()
urlpatterns = patterns('', url('^$', include('archer.projects.urls'), name='index'), url('^setup/', include('archer.appsetup.urls', namespace='appsetup')), url('^projects/', include('archer.projects.urls', namespace='projects')), url('^packages/', include('archer.packages.urls', namespace='packages')), url('^admin/', include(admin.site.urls)), url('^unauthenticated$', views.unauthenticated, name='unauthenticated'))