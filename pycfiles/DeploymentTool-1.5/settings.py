# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\FilePkl\hasil_development\Deploymentnew\Deployment\Deployment\settings.py
# Compiled at: 2014-10-27 22:38:34
"""
Django settings for Deployment project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'y&79j4=@rqgu)#ab7*^xh-%a(a_ar)!%ya#c((fbx32eju@!2h'
DEBUG = True
TEMPLATE_DEBUG = True
TEMPLATE_DIRS = (
 os.path.join(BASE_DIR, 'Templates'),)
STATICFILES_DIRS = (
 os.path.join(BASE_DIR, 'Static/Assets'),)
ALLOWED_HOSTS = [
 '*']
INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'Deploymentapp')
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware')
ROOT_URLCONF = 'Deployment.urls'
WSGI_APPLICATION = 'Deployment.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql', 
               'NAME': 'deploymentdb', 
               'USER': 'root', 
               'PASSWORD': '', 
               'HOST': 'localhost'}}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'Static')
LOGIN_URL = '/login'