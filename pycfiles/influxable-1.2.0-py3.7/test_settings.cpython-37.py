# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_settings.py
# Compiled at: 2019-10-23 08:36:50
# Size of source mod 2**32: 576 bytes
from influxable import settings

class TestSettings:

    def check_if_variable_exist(self, variable_name):
        return hasattr(settings, variable_name)

    def test_check_url_exist(self):
        assert self.check_if_variable_exist('INFLUXDB_URL')

    def test_check_user_exist(self):
        assert self.check_if_variable_exist('INFLUXDB_USER')

    def test_check_password_exist(self):
        assert self.check_if_variable_exist('INFLUXDB_PASSWORD')

    def test_check_database_name_exist(self):
        assert self.check_if_variable_exist('INFLUXDB_DATABASE_NAME')