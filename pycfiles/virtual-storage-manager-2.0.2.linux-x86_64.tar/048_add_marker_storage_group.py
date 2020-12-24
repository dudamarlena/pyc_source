# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/048_add_marker_storage_group.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Integer, MetaData, String
from sqlalchemy import Table, Index

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_group = Table('storage_groups', meta, autoload=True)
    marker = Column('marker', String(length=255), nullable=True, default='#ffff00')
    storage_group.create_column(marker)


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_group = Table('storage_groups', meta, autoload=True)
    marker = Column('marker', String(length=255), nullable=True, default='#ffff00')
    try:
        storage_group.drop_column(marker)
    except Exception:
        raise