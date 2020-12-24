# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/settings/base.py
# Compiled at: 2015-02-23 22:44:57
# Size of source mod 2**32: 9340 bytes
from __future__ import absolute_import, division
import os, sys
gettext = lambda s: s
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, 'extensions'))
sys.path.append(os.path.join(BASE_DIR, 'plugins'))
sys.path.append(os.path.join(BASE_DIR, 'apps'))
SECRET_KEY = 'h%v89*ik-=#+$nn+#%^(n(r+6bhs=r+q)a2o%n&k&doup&tce('
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = [
 '*']
ROOT_URLCONF = 'pegasus.urls'
WSGI_APPLICATION = 'pegasus.wsgi.application'
LANGUAGE_CODE = 'en'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATIC_FILES_LOADER = 'django.contrib.staticfiles.templatetags.staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
SITE_ID = 2
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader',
                    'django.template.loaders.eggs.Loader')
MIDDLEWARE_CLASSES = ('django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.locale.LocaleMiddleware',
                      'django.middleware.doc.XViewMiddleware', 'django.middleware.common.CommonMiddleware',
                      'django.middleware.clickjacking.XFrameOptionsMiddleware', 'cms.middleware.user.CurrentUserMiddleware',
                      'cms.middleware.page.CurrentPageMiddleware', 'cms.middleware.toolbar.ToolbarMiddleware',
                      'cms.middleware.language.LanguageCookieMiddleware')
TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages',
                               'django.core.context_processors.i18n', 'django.core.context_processors.debug',
                               'django.core.context_processors.request', 'django.core.context_processors.media',
                               'django.core.context_processors.csrf', 'django.core.context_processors.tz',
                               'sekizai.context_processors.sekizai', 'django.core.context_processors.static',
                               'cms.context_processors.cms_settings')
TEMPLATE_DIRS = (
 os.path.join(BASE_DIR, 'pegasus', 'templates'),)
INSTALLED_APPS = ('precompressed', 'djangocms_admin_style', 'djangocms_text_ckeditor',
                  'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.admin', 'django.contrib.sites', 'django.contrib.sitemaps',
                  'django.contrib.staticfiles', 'django.contrib.messages', 'cms',
                  'mptt', 'menus', 'sekizai', 'djangocms_style', 'djangocms_column',
                  'djangocms_file', 'djangocms_flash', 'djangocms_googlemap', 'djangocms_inherit',
                  'djangocms_link', 'djangocms_picture', 'djangocms_teaser', 'djangocms_video',
                  'reversion', 'content', 'authors', 'search', 'files', 'content_list',
                  'tombstones', 'left_nav', 'page_extras', 'utils', 'tombstone',
                  'four_up', 'masthead', 'carousel', 'django_extensions', 'taggit',
                  'haystack', 'sorl.thumbnail', 'genericadmin')
SOUTH_MIGRATION_MODULES = {'taggit': 'taggit.south_migrations'}
MIGRATION_MODULES = {'cms': 'cms.migrations_django', 
 'menus': 'menus.migrations_django', 
 'djangocms_column': 'djangocms_column.migrations_django', 
 'djangocms_file': 'djangocms_file.migrations_django', 
 'djangocms_flash': 'djangocms_flash.migrations_django', 
 'djangocms_googlemap': 'djangocms_googlemap.migrations_django', 
 'djangocms_inherit': 'djangocms_inherit.migrations_django', 
 'djangocms_link': 'djangocms_link.migrations_django', 
 'djangocms_picture': 'djangocms_picture.migrations_django', 
 'djangocms_snippet': 'djangocms_snippet.migrations_django', 
 'djangocms_style': 'djangocms_style.migrations_django', 
 'djangocms_teaser': 'djangocms_teaser.migrations_django', 
 'djangocms_video': 'djangocms_video.migrations_django', 
 'djangocms_text_ckeditor': 'djangocms_text_ckeditor.migrations_django', 
 'carousel': 'carousel.migrations', 
 'four_up': 'four_up.migrations_django', 
 'masthead': 'masthead.migrations', 
 'tombstone': 'tombstone.migrations'}
LANGUAGES = (
 (
  'en', gettext('en')),)
CMS_LANGUAGES = {'default': {'public': True, 
             'hide_untranslated': False, 
             'redirect_on_fallback': True}, 
 1: [
     {'public': True, 
      'code': 'en', 
      'hide_untranslated': False, 
      'name': gettext('en'), 
      'redirect_on_fallback': True}]}
CMS_TEMPLATES = (('pegasus/page.html', 'Page'), ('pegasus/pages/home.html', 'Home'),
                 ('pegasus/pages/work.html', 'Work'), ('pegasus/pages/news.html', 'News'),
                 ('pegasus/pages/connect.html', 'Connect'), ('pegasus/pages/contact.html', 'Contact'),
                 ('pegasus/pages/about.html', 'About'), ('pegasus/pages/search.html', 'Search'),
                 ('pegasus/pages/team.html', 'People'), ('pegasus/pages/donate.html', 'Donate'),
                 ('pegasus/pages/email.html', 'Keep Me Informed'))
CMS_PERMISSION = True
CMS_PLACEHOLDER_CONF = {'4up': {'plugins': [
                     'CMSFourUpPlugin']}, 
 'carousel': {'plugins': [
                          'CMSCarouselPlugin']}, 
 'masthead': {'plugins': [
                          'CMSMastheadPlugin']}}
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
             'NAME': 'project.db', 
             'HOST': 'localhost', 
             'USER': '', 
             'PASSWORD': '', 
             'PORT': ''}}
HAYSTACK_CONNECTIONS = {'default': {'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine', 
             'PATH': os.path.join(BASE_DIR, 'whoosh_index')}}
HAYSTACK_ROUTERS = [
 'haystack.routers.DefaultRouter']
ALDRYN_SEARCH_LANGUAGE_FROM_ALIAS = lambda alias: alias.split('-')[(-1)]
ALDRYN_SEARCH_REGISTER_APPHOOK = False
ALDRYN_SEARCH_PAGINATION = 10
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 
             'LOCATION': 'pegasus-default'}, 
 'decorated': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
LOGGING = {'version': 1, 
 'disable_existing_loggers': False, 
 'formatters': {},  'filters': {},  'handlers': {'null': {'level': 'DEBUG', 
                       'class': 'logging.NullHandler'}, 
              'console': {'level': 'DEBUG', 
                          'class': 'logging.StreamHandler'}, 
              'mail_admins': {'level': 'ERROR', 
                              'class': 'django.utils.log.AdminEmailHandler'}}, 
 'loggers': {'django': {'handlers': [
                                     'null'], 
                        'propagate': True, 
                        'level': 'INFO'}, 
             'django.db': {'handlers': [
                                        'console'], 
                           'level': 'DEBUG', 
                           'propagate': False}, 
             'django.request': {'handlers': [
                                             'mail_admins'], 
                                'level': 'ERROR', 
                                'propagate': False}, 
             'elasticsearch': {'handlers': [
                                            'console', 'mail_admins'], 
                               'level': 'INFO'}, 
             'elasticsearch.trace': {'handlers': [
                                                  'console'], 
                                     'level': 'INFO', 
                                     'propagate': False}, 
             'search': {'handlers': [
                                     'console'], 
                        'level': 'INFO'}, 
             'pegasus': {'handlers': [
                                      'console', 'mail_admins'], 
                         'level': 'INFO'}}}
TEXT_ADDITIONAL_TAGS = ('iframe', 'script')
TEXT_HTML_SANITIZE = True
CKEDITOR_SETTINGS = {'basicEntities': False, 
 'entities': False}