# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/settings/base/template.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 1572 bytes
"""
Base settings for Django templates.
"""
ALDRYN_BOILERPLATE_NAME = 'bootstrap3'
TEMPLATES = [
 {'BACKEND':'django.template.backends.django.DjangoTemplates', 
  'OPTIONS':{'context_processors':[
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.template.context_processors.i18n',
    'cms.context_processors.cms_settings',
    'sekizai.context_processors.sekizai',
    'aldryn_boilerplates.context_processors.boilerplate',
    'constance.context_processors.config'], 
   'loaders':[
    'django.template.loaders.filesystem.Loader',
    'aldryn_boilerplates.template_loaders.AppDirectoriesLoader',
    'django.template.loaders.app_directories.Loader']}}]