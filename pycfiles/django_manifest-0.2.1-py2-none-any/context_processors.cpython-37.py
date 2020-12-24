# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Dropbox/Sites/django-manifest/manifest/context_processors.py
# Compiled at: 2019-10-15 15:40:16
# Size of source mod 2**32: 527 bytes
""" Manifest Context Processors
"""
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from manifest import defaults

def site(request):
    return {'site': get_current_site(request)}


def installed_apps(request):
    return {'INSTALLED_APPS': getattr(settings, 'INSTALLED_APPS', None)}


def messages(request):
    return {'MANIFEST_USE_MESSAGES': defaults.MANIFEST_USE_MESSAGES}


def user_ip(request):
    return {'user_ip': request.META['REMOTE_ADDR']}