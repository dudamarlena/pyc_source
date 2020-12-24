# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rest_framework_extras/tests/urls.py
# Compiled at: 2016-10-26 05:12:13
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from rest_framework_extras import discover, register
from rest_framework_extras.tests import forms
router = routers.SimpleRouter()
discover(router, override=[
 (
  'tests.withform', dict(form=forms.WithFormForm)),
 (
  'tests.withtrickyform', dict(form=forms.WithFormTrickyForm))])
register(router)
urlpatterns = [
 url('^', include(router.urls)),
 url('^api-auth/', include('rest_framework.urls', namespace='rest_framework'))]