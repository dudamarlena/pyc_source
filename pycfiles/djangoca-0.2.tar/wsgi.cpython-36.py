# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Archivos\Proyectos\Python\Django\DjangoProjects\base_django\base_django\wsgi.py
# Compiled at: 2019-05-23 00:59:34
# Size of source mod 2**32: 426 bytes
"""
WSGI config for base_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base_django.configuracion.local')
application = get_wsgi_application()