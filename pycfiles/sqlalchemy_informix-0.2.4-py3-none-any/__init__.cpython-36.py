# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /builds/apollo13/sqlalchemy-informix/sqlalchemy_informix/__init__.py
# Compiled at: 2018-07-26 11:33:27
# Size of source mod 2**32: 185 bytes
__version__ = '0.2.4'
import os
from sqlalchemy.dialects import registry
os.environ['DELIMIDENT'] = 'y'
registry.register('informix', 'sqlalchemy_informix.ibmdb', 'InformixDialect')