# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dpl1_main/testing_app/urls.py
# Compiled at: 2014-02-28 07:48:58
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.admin import sites
from dpl1_main.testing_app import views
admin.autodiscover()

class CustomAdmin(sites.AdminSite):
    login_template = 'testing_app/admin/login.html'


urlpatterns = patterns('testing_app', url('^admin/', include(CustomAdmin().urls), name='admin'), url('^$', views.home_view, name='testing_app'), url('tests/(?P<test_id>\\d+)/results', views.show_result_view, name='results'), url('^tests/(?P<test_id>\\d+)/(?P<page_id>\\d+)', views.pages_view, name='pages'), url('^404', views.error_view, name='error'))