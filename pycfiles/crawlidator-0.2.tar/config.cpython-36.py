# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/tests/dummy_site_crawler/sql_backend/config.py
# Compiled at: 2019-12-27 17:54:42
# Size of source mod 2**32: 1476 bytes
from configirl import ConfigClass, Constant, Derivable

class Config(ConfigClass):
    DB_LOCAL_HOST = Constant(default='localhost')
    DB_LOCAL_PORT = Constant(default=43347)
    DB_LOCAL_DATABASE = Constant(default='postgres')
    DB_LOCAL_USERNAME = Constant(default='postgres')
    DB_LOCAL_PASSWORD = Constant(default='password')
    DB_HOST = Derivable()

    @DB_HOST.getter
    def get_DB_HOST(self):
        if self.is_ci_runtime():
            return self.DB_LOCAL_HOST.get_value()
        else:
            return self.DB_LOCAL_HOST.get_value()

    DB_PORT = Derivable()

    @DB_PORT.getter
    def get_DB_PORT(self):
        if self.is_ci_runtime():
            return 5432
        else:
            return self.DB_LOCAL_PORT.get_value()

    DB_DATABASE = Derivable()

    @DB_DATABASE.getter
    def get_DB_DATABASE(self):
        if self.is_ci_runtime():
            return self.DB_LOCAL_DATABASE.get_value()
        else:
            return self.DB_LOCAL_DATABASE.get_value()

    DB_USERNAME = Derivable()

    @DB_USERNAME.getter
    def get_DB_USERNAME(self):
        if self.is_ci_runtime():
            return self.DB_LOCAL_USERNAME.get_value()
        else:
            return self.DB_LOCAL_USERNAME.get_value()

    DB_PASSWORD = Derivable()

    @DB_PASSWORD.getter
    def get_DB_PASSWORD(self):
        if self.is_ci_runtime():
            return
        else:
            return self.DB_LOCAL_PASSWORD.get_value()