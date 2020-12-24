# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eitan/Documents/code/RITRemixerator/dorrie/settings.py
# Compiled at: 2012-01-26 12:37:48
import os, subprocess
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG
STATIC_SERVE = True
ADMINS = ()
MANAGERS = ADMINS
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(APP_ROOT, 'dorrie.sqlite3')
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = os.path.join(APP_ROOT, 'comps/media')
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = 'k1t7g+u*^80=e@^3efkmwqqtvj@6)pvoakjgagmo3*#jov^t%v'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.load_template_source', 'django.template.loaders.app_directories.load_template_source')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware')
ROOT_URLCONF = 'dorrie.urls'
TEMPLATE_DIRS = (
 '%scomps/templates/' % APP_ROOT,)
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'comps')
p = subprocess.Popen(['cat', '/etc/fedora-release'], stdout=subprocess.PIPE)
pout = p.communicate()[0]
RELEASE_VER = pout.split(' ')[2]
COMPS_URL = 'http://git.fedorahosted.org/git/?p=comps.git;a=blob_plain;f=comps-f' + RELEASE_VER + '.xml.in;hb=HEAD'
KS_DIR = '/usr/share/spin-kickstarts/'
CACHE = '/tmp/'
REPO = ''
TESTING = False