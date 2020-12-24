# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/life-website-env/life-website/website/website/apps/djangocms_background_media/tests/test_settings.py
# Compiled at: 2016-06-23 11:00:12
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': ':memory:'}}
INSTALLED_APPS = [
 'django.contrib.contenttypes',
 'django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.messages',
 'django.contrib.sites',
 'djangocms_flexslider',
 'cms',
 'filer',
 'menus',
 'sekizai',
 'treebeard']
LANGUAGE_CODE = 'en'
MIDDLEWARE_CLASSES = []
SECRET_KEY = 'cms123'
SITE_ID = 1
TEMPLATES = [
 {'BACKEND': 'django.template.backends.django.DjangoTemplates', 
    'OPTIONS': {'context_processors': [
                                     'django.contrib.auth.context_processors.auth',
                                     'django.contrib.messages.context_processors.messages',
                                     'django.core.context_processors.i18n',
                                     'django.core.context_processors.debug',
                                     'django.core.context_processors.request',
                                     'django.core.context_processors.media',
                                     'django.core.context_processors.csrf',
                                     'django.core.context_processors.tz',
                                     'sekizai.context_processors.sekizai',
                                     'django.core.context_processors.static',
                                     'cms.context_processors.cms_settings'], 
                'loaders': [
                          'django.template.loaders.filesystem.Loader',
                          'django.template.loaders.app_directories.Loader',
                          'django.template.loaders.eggs.Loader']}}]