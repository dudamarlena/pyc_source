# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tagbase\settings.py
# Compiled at: 2009-08-06 01:20:53
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'C:\\Documents and Settings\\emilyw\\My Documents\\test\\gutentag1.0\\tagbase\\example_gutentagdb'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''
TIME_ZONE = 'Australia/Sydney'
BLASTDB = 'C:\\blastspace'
FORMATDB = 'C:\\PROGRA~1\\blast\\bin\\formatdb'
BLASTALL = 'C:\\PROGRA~1\\blast\\bin\\blastall'
BLASTCL3 = 'C:\\PROGRA~1\\blastcl3\\blastcl3'
EVALUE = 0.001
DBNAME = ''
STATIC_DOC_ROOT = 'C:\\Documents and Settings\\emilyw\\My Documents\\test\\gutentag1.0\\tagbase\\media'
LOG_FILE = 'C:\\Documents and Settings\\emilyw\\My Documents\\test\\gutentag1.0\\tagbase\\log.txt'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = 'z7)y=52_n0*ylc87^g)kl3cu&no($whkduz9kl$d)9e_co7gvq'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.load_template_source', 'django.template.loaders.app_directories.load_template_source')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware')
ROOT_URLCONF = 'tagbase.urls'
TEMPLATE_DIRS = ('C:/Documents and Settings/emilyw/My Documents/test/gutentag1.0/tagbase/templates', )
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'tagbase.gutentag', 'django.contrib.admin',
                  'django.contrib.sessions')