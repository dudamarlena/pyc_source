# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/martin/amonagent/tests/settings_test.py
# Compiled at: 2014-05-20 04:17:01
from amonagent.settings import settings
from nose.tools import eq_
import sys

class TestSettings(object):

    def test_settings_dict(self):
        assert settings.HOST
        assert settings.SYSTEM_CHECK_PERIOD
        assert settings.LOGGING_MAX_BYTES
        assert settings.PIDFILE
        assert settings.SERVER_KEY
        assert settings.LOGFILE