# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/omri/code/prediction/prediction/urls.py
# Compiled at: 2017-12-26 08:34:36
# Size of source mod 2**32: 1117 bytes
__doc__ = "prediction URL Configuration\n\nThe `urlpatterns` list routes URLs to views. For more information please see:\n    https://docs.djangoproject.com/en/2.0/topics/http/urls/\nExamples:\nFunction views\n    1. Add an import:  from my_app import views\n    2. Add a URL to urlpatterns:  path('', views.home, name='home')\nClass-based views\n    1. Add an import:  from other_app.views import Home\n    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')\nIncluding another URLconf\n    1. Import the include() function: from django.urls import include, path\n    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))\n"
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