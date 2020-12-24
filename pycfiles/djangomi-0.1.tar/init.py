# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jvai/code/djangomi/djangomi/init.py
# Compiled at: 2015-10-28 10:08:04
from __future__ import absolute_import
import os, sys
from django.conf import settings
from django.conf.global_settings import *
SECRET_KEY = os.getenv('SECRET_KEY', 'not_so_secret')
DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'
if not settings.configured:
    settings.configure(**locals())
import json
from django.http import HttpResponse
from django.conf.urls import patterns, url
from django.core import management
from django.core.wsgi import get_wsgi_application