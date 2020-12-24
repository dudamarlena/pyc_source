# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Archivos\Proyectos\Developer.pe\proyectos\base_django\base_django\urls.py
# Compiled at: 2019-07-11 01:39:44
# Size of source mod 2**32: 1090 bytes
"""base_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from aplicaciones.base.views import Login, logoutUsuario
urlpatterns = [
 path('admin/', admin.site.urls),
 path('', include(('aplicaciones.base.urls', 'base'))),
 path('usuarios/', include(('aplicaciones.usuarios.urls', 'usuarios'))),
 path('accounts/login/', (Login.as_view()), name='login'),
 path('logout/', logoutUsuario, name='logout')]