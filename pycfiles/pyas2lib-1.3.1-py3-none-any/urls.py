# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./pyas2/tests/urls.py
# Compiled at: 2017-03-07 00:07:29
__doc__ = "pyas2_dev URL Configuration\n\nThe `urlpatterns` list routes URLs to views. For more information please see:\n    https://docs.djangoproject.com/en/1.9/topics/http/urls/\nExamples:\nFunction views\n    1. Add an import:  from my_app import views\n    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')\nClass-based views\n    1. Add an import:  from other_app.views import Home\n    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')\nIncluding another URLconf\n    1. Import the include() function: from django.conf.urls import url, include\n    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))\n"
from django.conf.urls import url, include
from django.contrib import admin
urlpatterns = [
 url('^admin/', admin.site.urls),
 url('^pyas2/', include('pyas2.urls'))]