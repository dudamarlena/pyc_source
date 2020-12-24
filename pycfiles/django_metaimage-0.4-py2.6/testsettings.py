# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/metaimage/testsettings.py
# Compiled at: 2011-05-20 19:39:06
DATABASES = {'default': {'ENGINE': 'sqlite3', 
               'NAME': '/tmp/metaimage.db'}}
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'metaimage', 'photologue', 'taggit', 'uni_form')
METAIMAGE_MAX_REMOTE_IMAGE_SIZE = 1048576
ROOT_URLCONF = 'metaimage.urls'