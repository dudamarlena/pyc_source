# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/michal/workspace/code/django-mips/mips/settings.py
# Compiled at: 2015-11-13 09:30:49
"""Settings file """
import dbsettings_default as dbsettings
try:
    import dbsettings_production as dbsettings
except ImportError as ie:
    print 'No production setting, load defaults'

SECRET_KEY = dbsettings.SECRET_KEY
ALLOWED_HOSTS = dbsettings.ALLOWED_HOSTS
INSTALLED_APPS = [
 'mips',
 'django_nose',
 'coverage']
MIDDLEWARE_CLASSES = ()
DATABASES = dbsettings.DATABASES
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
 '--with-coverage',
 '--cover-package=mips',
 '--cover-inclusive',
 '--verbosity=2']