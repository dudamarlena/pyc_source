# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nemesis/Code/django-owm-legacy/owm_legacy/__init__.py
# Compiled at: 2018-02-19 07:38:08
# Size of source mod 2**32: 452 bytes
VERSION = (0, 4, 1, 'final')
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


default_app_config = 'owm_legacy.apps.OwmLegacyConfig'