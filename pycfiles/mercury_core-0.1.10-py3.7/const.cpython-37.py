# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/behave/common/const.py
# Compiled at: 2018-07-31 13:26:37
# Size of source mod 2**32: 607 bytes


class ConfigVars(object):
    __doc__ = 'Configuration environment variables'
    VERBOSE = 'VERBOSE'
    MERCURY_API_ENDPOINT = 'MERCURY_API_ENDPOINT'
    INTERNAL_IDENTITY_URL = 'INTERNAL_IDENTITY_URL'
    INTERNAL_IDENTITY_USERNAME = 'INTERNAL_IDENTITY_USERNAME'
    INTERNAL_IDENTITY_PASSWORD = 'INTERNAL_IDENTITY_PASSWORD'
    DOMAIN = 'DOMAIN'
    DOMAIN_NAME = 'DOMAIN_NAME'
    JSON_API_DATA_LOCATION = 'JSON_API_DATA_LOCATION'


class Sources(object):
    __doc__ = 'Sources to get the configuration variables from'
    ENVIRON = 'environ'