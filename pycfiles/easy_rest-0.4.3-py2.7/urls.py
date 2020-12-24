# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/easyapi/tests/test_project/urls.py
# Compiled at: 2014-08-13 19:57:15
from django.conf.urls import patterns, include, url
from django.contrib import admin
from easyapi.enums import EnumRouter
from easyapi.router import AutoAppListRouter, AutoAppRouter
from easyapi.tests.test_project.api import router
from easyapi.tests.test_project.models import CompanyType, ProjectScope
from easyapi.tests.test_project.views import WelcomeView
admin.autodiscover()
auto_list_router = AutoAppListRouter('test_project', namespace='list')
auto_router = AutoAppRouter('test_project', namespace='normal')
enum_router = EnumRouter([CompanyType, ProjectScope])
urlpatterns = patterns('easyapi.tests.test_project.views', url('^admin/', include(admin.site.urls)), url('^api/', include(router.urls)), url('^enums/', include(enum_router.urls)), url('^auto-list/', include(auto_list_router.urls)), url('^auto-api/', include(auto_router.urls)), url('^custom-api/hello-func/', 'say_hello'), url('^custom-api/company-paginator/', 'company_paginator'), url('^custom-api/hello-view/', WelcomeView.as_view()))