# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/django-hstore/django_hstore/__init__.py
# Compiled at: 2016-04-02 17:02:59
# Size of source mod 2**32: 474 bytes
VERSION = (1, 4, 2, 'final')
__version__ = VERSION

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    elif VERSION[3] != 'final':
        version = '%s %s' % (version, VERSION[3])
    return version


default_app_config = 'django_hstore.apps.HStoreConfig'