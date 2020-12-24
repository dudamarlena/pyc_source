# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Moneta/moneta/iniconf.py
# Compiled at: 2017-11-04 07:55:26
# Size of source mod 2**32: 734 bytes
from djangofloor.conf.fields import bool_setting, CharConfigField
from djangofloor.conf.mapping import BASE_MAPPING, REDIS_MAPPING, AUTH_MAPPING, SENDFILE_MAPPING, ALLAUTH_MAPPING
__author__ = 'flanker'

def x_accel_converter(value):
    if bool_setting(value):
        return [('{MEDIA_ROOT}/', '/p/get/'),
         ('{MEDIA_ROOT}/', '/a/get/')]
    else:
        return []


INI_MAPPING = BASE_MAPPING + AUTH_MAPPING + ALLAUTH_MAPPING + REDIS_MAPPING + SENDFILE_MAPPING + [
 CharConfigField('gnupg.home', 'GNUPG_HOME', help_str='Path of the GnuPG secret data'),
 CharConfigField('gnupg.keyid', 'GNUPG_KEYID', help_str='ID of the GnuPG key'),
 CharConfigField('gnupg.path', 'GNUPG_PATH', help_str='Path of the gpg binary')]