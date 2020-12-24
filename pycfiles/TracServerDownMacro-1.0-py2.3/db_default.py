# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.11.1-i386/egg/serverdownmacro/db_default.py
# Compiled at: 2007-12-15 05:07:57
from trac.db import Table, Column
name = 'serverdown'
version = 1
tables = [Table('serverdown', key=('host', 'port'))[(Column('host'), Column('port'), Column('ts'), Column('value'))]]