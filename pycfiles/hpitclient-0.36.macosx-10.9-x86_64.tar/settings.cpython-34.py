# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/raymond/Projects/TutorGen/python-client/env/lib/python3.4/site-packages/hpitclient/settings.py
# Compiled at: 2014-07-18 16:12:59
# Size of source mod 2**32: 527 bytes


class HpitClientSettings:
    instance = None
    HPIT_URL_ROOT = 'https://www.hpit-project.org'
    REQUESTS_LOG_LEVEL = 'debug'

    def __new__(cls, *args, **kwargs):
        if cls.instance:
            raise Exception('Settings has already been created.')
        cls.instance = object.__new__(cls)
        cls.instance.__init__(*args, **kwargs)
        return cls.instance

    @classmethod
    def settings(cls):
        if not cls.instance:
            cls.instance = HpitClientSettings()
        return cls.instance