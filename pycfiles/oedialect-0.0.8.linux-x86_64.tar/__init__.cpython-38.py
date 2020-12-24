# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/oedialect/__init__.py
# Compiled at: 2020-04-01 07:23:01
# Size of source mod 2**32: 140 bytes
from sqlalchemy.dialects import registry
from psycopg2 import *
registry.register('postgresql.oedialect', 'oedialect.dialect', 'OEDialect')