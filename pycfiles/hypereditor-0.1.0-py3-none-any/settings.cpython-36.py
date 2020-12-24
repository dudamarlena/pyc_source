# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shimul/Projects/django-hyper-editor/hypereditor/settings.py
# Compiled at: 2019-04-10 07:52:53
# Size of source mod 2**32: 782 bytes
from django.conf import settings
from django.apps import apps
from hypereditor import utils
WAGTAIL_EXISTS = apps.is_installed('wagtail.core')
HYPER_SETTINGS = {'BLOCK_CONFIG':{},  'STYLESHEETS':[],  'IMAGE_API_URL':'#', 
 'AUTHENTICATION_MIXIN':'hypereditor.views.AuthMixin'}
utils.merge_dict(HYPER_SETTINGS, getattr(settings, 'HYPER_EDITOR', {}))
AUTHENTICATION_MIXIN = HYPER_SETTINGS['AUTHENTICATION_MIXIN']
BLOCK_CONFIG = HYPER_SETTINGS['BLOCK_CONFIG']
STYLESHEETS = HYPER_SETTINGS['STYLESHEETS']
IMAGE_API_URL = HYPER_SETTINGS['IMAGE_API_URL']