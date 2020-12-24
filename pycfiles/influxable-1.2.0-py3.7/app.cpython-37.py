# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/influxable/app.py
# Compiled at: 2019-10-23 08:36:50
# Size of source mod 2**32: 1144 bytes
from .api import InfluxDBApi
from .connection import Connection
from helpers.decorators import Singleton

@Singleton
class Influxable:

    def __init__(self, *args, **kwargs):
        self.connection = Connection(*args, **kwargs)

    def create_connection(self, *args, **kwargs):
        return (Connection.create_connection)(*args, **kwargs)

    def ping(self, *args, **kwargs):
        request = self.connection.request
        return (InfluxDBApi.ping)(request, *args, **kwargs)

    def execute_query(self, *args, **kwargs):
        request = self.connection.request
        return (InfluxDBApi.execute_query)(request, *args, **kwargs)

    def write_points(self, *args, **kwargs):
        request = self.connection.request
        return (InfluxDBApi.write_points)(request, *args, **kwargs)

    @property
    def base_url(self):
        return self.connection.base_url

    @property
    def database_name(self):
        return self.connection.database_name

    @property
    def full_database_name(self):
        return self.connection.full_database_name

    @property
    def policy_name(self):
        return self.connection.policy_name