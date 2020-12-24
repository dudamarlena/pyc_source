# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/projects/django-init/django_init/db/mysql.py
# Compiled at: 2020-01-15 01:17:43
# Size of source mod 2**32: 207 bytes
import MySQLdb
from django_init.db.base import DatabaseBase

class DatabaseMySQL(DatabaseBase):
    client = MySQLdb