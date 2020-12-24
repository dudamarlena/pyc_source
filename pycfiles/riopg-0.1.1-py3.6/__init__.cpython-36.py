# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/riopg/__init__.py
# Compiled at: 2018-08-16 08:33:20
# Size of source mod 2**32: 166 bytes
"""
riopg - a curio/trio library for connecting and interacting with PostgreSQL.
"""
from riopg.connection import Connection
from riopg.pool import Pool, create_pool