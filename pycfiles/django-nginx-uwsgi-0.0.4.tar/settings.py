# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\GITHUB\django-nginx-uwsgi\dnuconfig\settings.py
# Compiled at: 2016-02-14 21:46:15
import os
NGINX_DIR = os.path.dirname('/srv/nginx/')
VASSALS_DIR = os.path.dirname('/srv/vassals/')
SOCKS_DIR = os.path.dirname('/srv/socks/')
DJANGO_SETTINGS_MODULE = 'settings'
LOGS_DIR = os.path.dirname('/srv/logs/')
MODULE_TO_RUN = 'wsgi'