# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/quantmind/pulsar-odm/tests/__init__.py
# Compiled at: 2017-11-24 06:00:10
# Size of source mod 2**32: 263 bytes
from pulsar.apps.test import TestPlugin

class PostgreSql(TestPlugin):
    name = 'postgresql'
    meta = 'CONNECTION_STRING'
    default = 'postgresql+green://odm:odmtest@127.0.0.1:5432/odmtests'
    desc = 'Default connection string for the PostgreSql server'