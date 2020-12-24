# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dpl1_main/DPL1/wsgi.py
# Compiled at: 2014-02-28 04:10:10
"""
WSGI config for DPL1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os
from dpl1_main.deployment_util import correct_sys_path
correct_sys_path('../..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dpl1_main.DPL1.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()