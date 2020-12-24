# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/build/quantmind/pulsar-odm/tests/__init__.py
# Compiled at: 2017-11-24 06:00:10
# Size of source mod 2**32: 263 bytes
from pulsar.apps.test import TestPlugin

class PostgreSql(TestPlugin):
    name = 'postgresql'
    meta = 'CONNECTION_STRING'
    default = 'postgresql+green://odm:odmtest@127.0.0.1:5432/odmtests'
    desc = 'Default connection string for the PostgreSql server'