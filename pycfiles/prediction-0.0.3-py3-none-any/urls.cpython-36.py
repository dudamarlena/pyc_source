# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/omri/code/prediction/prediction/urls.py
# Compiled at: 2017-12-26 08:34:36
# Size of source mod 2**32: 1117 bytes
"""prediction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from scoring import api
router = routers.DefaultRouter()
class_based_views = [
 path('hello-world/', (api.HelloWorld.as_view()), name='hello-world')]
urlpatterns = [
 path('admin/', admin.site.urls),
 path('api/v1/', include(class_based_views)),
 path('api/v1/', include(router.urls))]