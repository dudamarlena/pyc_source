# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/haplugin/auth/db_tables.py
# Compiled at: 2014-09-30 02:34:53
# Size of source mod 2**32: 285 bytes
from haplugin.sql import Base
from sqlalchemy import Column, Integer, ForeignKey, Table
users_2_permissions = Table('users_2_permissions', Base.metadata, Column('user_id', Integer, ForeignKey('users.id')), Column('permission_id', Integer, ForeignKey('permissions.id')))