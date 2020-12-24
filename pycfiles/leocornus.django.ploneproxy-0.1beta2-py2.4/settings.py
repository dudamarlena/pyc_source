# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/leocornus/django/ploneproxy/settings.py
# Compiled at: 2010-06-02 17:39:15
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/usr/local/rd/django/test-db/simple1.db'
TEST_DATABASE_NAME = '/usr/local/rd/django/test-db/simple-test.db'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''
TIME_ZONE = 'America/Toronto Canada/Eastern'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = '@!+pn=pph&o30zaz)u$pq&kx5zy_y_v%-25+#es@91#h0%zgql'
SESSION_COOKIE_NAME = 'ctssessionid'
SESSION_COOKIE_AGE = 300
AUTHENTICATION_BACKENDS = ('leocornus.django.ploneproxy.authen.backends.PloneModelBackend', )
PLONEPROXY_COOKIE_NAME = '__ac'
PLONEPROXY_LANG_FIELD_NAME = 'ldp_lang'
PLONEPROXY_PLONE_VIEW_BYPASS = ('/view/', '/presentation_view/', '/folder_contents/',
                                '/vcs_view/', '/ics_view/', '/manage_main/', 'plone_control_panel')
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.load_template_source', 'django.template.loaders.app_directories.load_template_source')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'leocornus.django.ploneproxy.authen.middleware.PloneCookieMiddleware',
                      'django.contrib.sessions.middleware.SessionMiddleware', 'leocornus.django.ploneproxy.middleware.LocaleMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware')
ROOT_URLCONF = 'leocornus.django.ploneproxy.urls'
TEMPLATE_DIRS = ()
INSTALLED_APPS = ('leocornus.django.ploneproxy', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.sites', 'django.contrib.admin',
                  'leocornus.django.ploneproxy.authen')