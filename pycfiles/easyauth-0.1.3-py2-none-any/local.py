# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\mine\PycharmProjects\easyauth\test\settings\local.py
# Compiled at: 2018-12-22 08:45:48
"""Development settings."""
import os
os.environ['EASYAUTH_LOG_LEVEL'] = 'DEBUG'
from os.path import join, normpath
from .production import *
DEBUG = True
TEMPLATE_DEBUG = DEBUG
CORS_ORIGIN_ALLOW_ALL = DEBUG
CORS_ALLOW_CREDENTIALS = DEBUG
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': normpath(join(WK_DIR, 'db.sqlite3')), 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
REST_FRAMEWORK = {'DEFAULT_PERMISSION_CLASSES': ('easyauth.permissions.IsAuthenticated', ), 
   'DEFAULT_AUTHENTICATION_CLASSES': ('easyauth.authentication.CsrfExemptSessionAuthentication', 'rest_framework.authentication.BasicAuthentication'), 
   'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer', 'rest_framework.renderers.BrowsableAPIRenderer'), 
   'DEFAULT_PARSER_CLASSES': ('rest_framework.parsers.JSONParser', 'rest_framework.parsers.FormParser', 'rest_framework.parsers.MultiPartParser'), 
   'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend', 'rest_framework.filters.SearchFilter',
 'rest_framework.filters.OrderingFilter'), 
   'EXCEPTION_HANDLER': 'easyauth.views.exception_handler', 
   'DEFAULT_PAGINATION_CLASS': 'easyauth.pagination.CustomizedPageNumberPagination', 
   'PAGE_SIZE': 500}