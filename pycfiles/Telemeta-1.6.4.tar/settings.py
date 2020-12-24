# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/app/settings.py
# Compiled at: 2017-09-17 17:51:33
import os, sys
from django.core.urlresolvers import reverse_lazy, reverse
import environ
env = environ.Env(DEBUG=(bool, False), CELERY_ALWAYS_EAGER=(
 bool, False))
DEBUG = env('DEBUG')
TEMPLATE_DEBUG = DEBUG
sys.dont_write_bytecode = True
ALLOWED_HOSTS = [
 '*']
ADMINS = (('Guillaume Pellerin', 'yomguy@parisson.com'), )
MANAGERS = ADMINS
PROJECT_ROOT = '/srv/app/'
DATABASES = {'default': {'ENGINE': env('ENGINE'), 
               'USER': env('MYSQL_USER'), 
               'PASSWORD': env('MYSQL_PASSWORD'), 
               'NAME': env('MYSQL_DATABASE'), 
               'HOST': 'db', 
               'PORT': '3306'}}
TIME_ZONE = 'Europe/Paris'
LANGUAGES = [
 ('fr', 'French'),
 ('en', 'English'),
 ('de', 'German'),
 ('zh_CN', 'Simplified Chinese'),
 ('ar_TN', 'Arabic'),
 ('pt_BR', 'Portuguese'),
 ('es', 'Spanish')]
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = '/srv/media/'
MEDIA_URL = '/media/'
STATIC_ROOT = '/srv/static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
                       'djangobower.finders.BowerFinder')
SECRET_KEY = 'a8l7%06wr2k+3=%#*#@#rvop2mmzko)44%7k(zx%lls^ihm9^5'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
MIDDLEWARE_CLASSES = ('djng.middleware.AngularUrlMiddleware', 'django.middleware.common.CommonMiddleware',
                      'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.locale.LocaleMiddleware',
                      'debug_toolbar.middleware.DebugToolbarMiddleware')
ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = ()
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.messages', 'suit', 'django.contrib.admin',
                  'django.contrib.staticfiles', 'django_extensions', 'telemeta',
                  'timeside.player', 'timeside.server', 'jsonrpc', 'south', 'sorl.thumbnail',
                  'timezones', 'jqchat', 'ipauth', 'extra_views', 'debug_toolbar',
                  'bootstrap3', 'bootstrap_pagination', 'googletools', 'registration',
                  'rest_framework', 'djcelery', 'haystack', 'djangobower', 'djng',
                  'saved_searches')
TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.request', 'django.contrib.auth.context_processors.auth',
                               'django.core.context_processors.i18n', 'django.core.context_processors.media',
                               'django.core.context_processors.static', 'django.contrib.messages.context_processors.messages')
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', 'ipauth.backend.RangeBackend')
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
TELEMETA_ORGANIZATION = 'CREM-CNRS'
TELEMETA_SUBJECTS = ('Ethnomusicology', 'Research')
TELEMETA_DESCRIPTION = "Sound archives of the CNRS and the Musee de l'Homme. Research Centre of Ethnomusicology (CREM), University of Paris 10"
TELEMETA_LOGO = STATIC_URL + 'telemeta/images/logo_crem.png'
TELEMETA_GMAP_KEY = 'ABQIAAAArg7eSfnfTkBRma8glnGrlxRVbMrhnNNvToCbZQtWdaMbZTA_3RRGObu5PDoiBImgalVnnLU2yN4RMA'
TELEMETA_CACHE_DIR = os.path.join(MEDIA_ROOT, 'cache')
TELEMETA_EXPORT_CACHE_DIR = os.path.join(MEDIA_ROOT, 'export')
TELEMETA_DATA_CACHE_DIR = os.path.join(TELEMETA_CACHE_DIR, 'data')
FILE_UPLOAD_TEMP_DIR = os.path.join(MEDIA_ROOT, 'tmp')
FILE_UPLOAD_PERMISSIONS = 420
TELEMETA_DOWNLOAD_ENABLED = False
TELEMETA_STREAMING_FORMATS = ('mp3', 'ogg')
TELEMETA_DOWNLOAD_FORMATS = ('wav', 'mp3', 'ogg', 'flac')
TELEMETA_PUBLIC_ACCESS_PERIOD = 51
TELEMETA_STRICT_CODE = False
COLLECTION_PUBLISHED_CODE_REGEX = 'CNRSMH_E_[0-9]{4}(?:_[0-9]{3}){2}'
COLLECTION_UNPUBLISHED_CODE_REGEX = 'CNRSMH_I_[0-9]{4}_[0-9]{3}'
ITEM_PUBLISHED_CODE_REGEX = COLLECTION_PUBLISHED_CODE_REGEX + '(?:_[0-9]{2,3}){1,2}'
ITEM_UNPUBLISHED_CODE_REGEX = COLLECTION_UNPUBLISHED_CODE_REGEX + '_[0-9]{2,3}(?:_[0-9]{2,3}){0,2}'
AUTH_PROFILE_MODULE = 'telemeta.userprofile'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/desk/lists/'
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'webmaster@parisson.com'
TIMESIDE_DEFAULT_GRAPHER_ID = 'waveform_centroid'
TIMESIDE_DEFAULT_WAVEFORM_SIZES = ['346x130', '640x130']
TIMESIDE_AUTO_ZOOM = False
BOOTSTRAP3 = {'set_required': True, 
   'set_placeholder': False, 
   'error_css_class': 'has-error', 
   'required_css_class': 'has-warning', 
   'javascript_in_head': True}
PAGINATION_SETTINGS = {'PAGE_RANGE_DISPLAYED': 10, 
   'MARGIN_PAGES_DISPLAYED': 2}
if DEBUG:
    DEBUG_TOOLBAR_CONFIG = {'SHOW_TOOLBAR_CALLBACK': lambda x: True}
DEBUG_TOOLBAR_PATCH_SETTINGS = False
DEBUG_TOOLBAR_PANELS = [
 'debug_toolbar.panels.versions.VersionsPanel',
 'debug_toolbar.panels.timer.TimerPanel',
 'debug_toolbar.panels.settings.SettingsPanel',
 'debug_toolbar.panels.headers.HeadersPanel',
 'debug_toolbar.panels.request.RequestPanel',
 'debug_toolbar.panels.sql.SQLPanel',
 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
 'debug_toolbar.panels.templates.TemplatesPanel',
 'debug_toolbar.panels.cache.CachePanel',
 'debug_toolbar.panels.signals.SignalsPanel',
 'debug_toolbar.panels.logging.LoggingPanel',
 'debug_toolbar.panels.redirects.RedirectsPanel']
SUIT_CONFIG = {'ADMIN_NAME': 'Telemeta Admin'}
LOGGING = {'version': 1, 
   'disable_existing_loggers': False, 
   'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}}, 
   'handlers': {'mail_admins': {'level': 'ERROR', 
                                'filters': [
                                          'require_debug_false'], 
                                'class': 'django.utils.log.AdminEmailHandler'}}, 
   'loggers': {'django.request': {'handlers': [
                                             'mail_admins'], 
                                  'level': 'ERROR', 
                                  'propagate': True}}}
BROKER_URL = env('BROKER_URL')
CELERY_IMPORTS = ('timeside.server.tasks', )
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']
from worker import app
HAYSTACK_CONNECTIONS = {'default': {'ENGINE': 'telemeta.util.backend.CustomElasticEngine', 
               'URL': env('HAYSTACK_URL'), 
               'INDEX_NAME': env('HAYSTACK_INDEX_NAME'), 
               'INLUDE_SPELLING': True, 
               'EXCLUDED_INDEXES': [
                                  'telemeta.search_indexes.LocationIndex',
                                  'telemeta.search_indexes.LocationAliasIndex',
                                  'telemeta.search_indexes.InstrumentIndex',
                                  'telemeta.search_indexes.InstrumentAliasIndex']}, 
   'autocomplete': {'ENGINE': 'telemeta.util.backend.CustomElasticEngine', 
                    'URL': env('HAYSTACK_URL'), 
                    'INDEX_NAME': env('HAYSTACK_INDEX_NAME_AUTOCOMPLETE'), 
                    'INLUDE_SPELLING': True, 
                    'EXCLUDED_INDEXES': [
                                       'telemeta.search_indexes.MediaItemIndex',
                                       'telemeta.search_indexes.MediaCollectionIndex',
                                       'telemeta.search_indexes.MediaCorpusIndex',
                                       'telemeta.search_indexes.MediaFondsIndex']}}
HAYSTACK_ROUTERS = [
 'telemeta.util.search_router.AutoRouter', 'haystack.routers.DefaultRouter']
HAYSTACK_SIGNAL_PROCESSOR = 'telemeta.util.search_signals.RealTimeCustomSignal'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 50
BOWER_COMPONENTS_ROOT = '/srv/bower/'
BOWER_PATH = '/usr/local/bin/bower'
BOWER_INSTALLED_APPS = ('jquery#2.2.4', 'jquery-migrate#~1.2.1', 'underscore#1.8.3',
                        'bootstrap#3.3.6', 'bootstrap-select#1.5.4', 'font-awesome#4.4.0',
                        'angular#1.2.26', 'angular-bootstrap-select#0.0.5', 'angular-resource#1.2.26',
                        'raphael#2.2.0', 'soundmanager#V2.97a.20150601', 'https://github.com/Parisson/loaders.git',
                        'https://github.com/Parisson/ui.git', 'jquery-ui#1.11.4',
                        'tablesorter', 'video.js', 'sass-bootstrap-glyphicons')