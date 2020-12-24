# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/settings.py
# Compiled at: 2018-07-21 08:49:30
# Size of source mod 2**32: 4307 bytes
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_NAME = 'ambition_validators'
ETC_DIR = os.path.join(BASE_DIR, 'etc')
SITE_ID = 40
REVIEWER_SITE_ID = 0
SECRET_KEY = '6_sw)a7sn3tt%tbx$aps62a90dp&yfdri+a#=udt6g_4h--$q9'
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
 'django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.messages',
 'django.contrib.staticfiles',
 'django.contrib.sites',
 'django_crypto_fields.apps.AppConfig',
 'django_revision.apps.AppConfig',
 'edc_appointment.apps.AppConfig',
 'edc_base.apps.AppConfig',
 'edc_device.apps.AppConfig',
 'edc_metadata.apps.AppConfig',
 'edc_identifier.apps.AppConfig',
 'edc_protocol.apps.AppConfig',
 'edc_registration.apps.AppConfig',
 'edc_timepoint.apps.AppConfig',
 'edc_form_validators.apps.AppConfig',
 'edc_visit_schedule.apps.AppConfig',
 'ambition_screening.apps.AppConfig',
 'ambition_labs.apps.AppConfig',
 'ambition_validators.apps.AppConfig']
MIDDLEWARE_CLASSES = [
 'django.middleware.security.SecurityMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
 'django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF = 'ambition_validators.urls'
TEMPLATES = [
 {'BACKEND':'django.template.backends.django.DjangoTemplates', 
  'DIRS':[],  'APP_DIRS':True, 
  'OPTIONS':{'context_processors': [
                          'django.template.context_processors.debug',
                          'django.template.context_processors.request',
                          'django.contrib.auth.context_processors.auth',
                          'django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'ambition_validators.wsgi.application'
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
             'NAME':os.path.join(BASE_DIR, 'db.sqlite3')}}
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
DASHBOARD_URL_NAMES = {'subject_models_url':'subject_models_url', 
 'subject_listboard_url':'ambition_dashboard:subject_listboard_url', 
 'screening_listboard_url':'ambition_dashboard:screening_listboard_url', 
 'subject_dashboard_url':'ambition_dashboard:subject_dashboard_url'}
if 'test' in sys.argv:
    COUNTRY = 'botswana'

    class DisableMigrations:

        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            pass


    MIGRATION_MODULES = DisableMigrations()
    PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher', )
    DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'