# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbix/dbix.py
# Compiled at: 2017-10-10 20:03:37
"""Main module."""
from .schema import Schema
from .sqlschema import SQLSchema
from .sqlite import SQLITE
from .postgresql import POSTGRESQL
from .mysql import MYSQL
from .perlconv import treeconv, oneconv, schemaconv