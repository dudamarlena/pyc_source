# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maupetit/projects/TailorDev/django-tailordev-biblio/sandbox/settings.py
# Compiled at: 2018-11-13 15:51:41
# Size of source mod 2**32: 3465 bytes
"""
Django settings for td_biblio sandbox.
"""
import os, dj_database_url
try:
    from django.core.urlresolvers import reverse_lazy
except:
    from django.urls import reverse_lazy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '2#jyyh#-tgk$%wdx0zgfx=-)#hr9ni(_m66a3!rmco8^a5cns!')
DEBUG = os.environ.get('IS_PUBLIC_SANDBOX') is None
ALLOWED_HOSTS = [
 'localhost', '127.0.0.1', 'tailordev-biblio.herokuapp.com']
LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('td_biblio:import')
INSTALLED_APPS = [
 'django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.messages',
 'whitenoise.runserver_nostatic',
 'django.contrib.staticfiles',
 'td_biblio']
MIDDLEWARE = ('django.middleware.security.SecurityMiddleware', 'whitenoise.middleware.WhiteNoiseMiddleware',
              'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
              'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
              'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware')
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware')
ROOT_URLCONF = 'sandbox.urls'
TEMPLATES = [
 {'BACKEND':'django.template.backends.django.DjangoTemplates', 
  'DIRS':[
   os.path.join(BASE_DIR, 'templates')], 
  'APP_DIRS':True, 
  'OPTIONS':{'context_processors': [
                          'django.template.context_processors.debug',
                          'django.template.context_processors.request',
                          'django.contrib.auth.context_processors.auth',
                          'django.contrib.messages.context_processors.messages']}}]
TEMPLATE_DIRS = [
 os.path.join(BASE_DIR, 'templates')]
WSGI_APPLICATION = 'sandbox.wsgi.application'
DATABASES = {'default': dj_database_url.config(conn_max_age=600)}
AUTH_PASSWORD_VALIDATORS = [
 {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
 {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
 {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
 {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)