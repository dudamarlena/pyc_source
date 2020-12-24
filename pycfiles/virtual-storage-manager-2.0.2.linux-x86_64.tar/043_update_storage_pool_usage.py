# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/043_update_storage_pool_usage.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Integer, MetaData, String
from sqlalchemy import Table, Index

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_pool_usages = Table('storage_pool_usages', meta, autoload=True)
    appnode_id = Column('appnode_id', Integer, nullable=False)
    cinder_volume_host = Column('cinder_volume_host', String(length=255), nullable=False)
    try:
        storage_pool_usages.create_column(appnode_id)
        storage_pool_usages.create_column(cinder_volume_host)
    except Exception:
        raise


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_pool_usages = Table('storage_pool_usages', meta, autoload=True)
    appnode_id = Column('appnode_id', Integer, nullable=False)
    cinder_volume_host = Column('cinder_volume_host', String(length=255), nullable=False)
    try:
        storage_pool_usages.drop_column(appnode_id)
        storage_pool_usages.drop_column(cinder_volume_host)
    except Exception:
        raise