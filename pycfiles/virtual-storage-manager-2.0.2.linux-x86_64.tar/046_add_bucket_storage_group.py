# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/046_add_bucket_storage_group.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Integer, MetaData, String
from sqlalchemy import Table, Index

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_group = Table('storage_groups', meta, autoload=True)
    take_id = Column('take_id', Integer, nullable=True)
    storage_group.create_column(take_id)
    take_order = Column('take_order', Integer, nullable=True)
    storage_group.create_column(take_order)


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_group = Table('storage_groups', meta, autoload=True)
    take_id = Column('take_id', Integer, nullable=True)
    take_order = Column('take_order', Integer, nullable=True)
    try:
        storage_group.drop_column(take_id)
        storage_group.drop_column(take_order)
    except Exception:
        raise