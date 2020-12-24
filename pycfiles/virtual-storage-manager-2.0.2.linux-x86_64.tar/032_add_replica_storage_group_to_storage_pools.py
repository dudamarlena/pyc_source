# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/032_add_replica_storage_group_to_storage_pools.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import and_, String, Column, MetaData, select, Table, Integer

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_pools = Table('storage_pools', meta, autoload=True)
    replica_storage_pool = Column('replica_storage_pool', String(length=255))
    storage_pools.create_column(replica_storage_pool)


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_pools = Table('storage_pools', meta, autoload=True)
    storage_pools.drop_column('replica_storage_pool')