# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_connection.py
# Compiled at: 2019-10-23 08:36:50
# Size of source mod 2**32: 1090 bytes
import pytest
from influxable import InfluxDBApi, exceptions
from influxable.connection import Connection

class TestConnection:

    def check_if_connection_reached(self, connection):
        query = 'SHOW DATABASES'
        InfluxDBApi.execute_query(connection.request, query)

    def test_create_instance_with_no_args_success(self):
        connection = Connection()
        self.check_if_connection_reached(connection)
        assert connection is not None

    def test_create_instance_with_args_success(self):
        connection = Connection(user='admin',
          password='changeme')
        self.check_if_connection_reached(connection)
        assert connection is not None

    def test_create_instance_with_bad_url_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidURLError):
            Connection(base_url='incorrect_url')

    def test_create_instance_with_bad_database_name_fail(self):
        pytest.skip()
        with pytest.raises(exceptions.InfluxDBInvalidURLError):
            Connection(database_name='invalid_database_name')