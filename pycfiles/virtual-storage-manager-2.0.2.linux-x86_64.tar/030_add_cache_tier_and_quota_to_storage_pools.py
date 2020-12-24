# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/030_add_cache_tier_and_quota_to_storage_pools.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import and_, String, Column, MetaData, select, Table, Integer

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_pools = Table('storage_pools', meta, autoload=True)
    cache_tier_status = Column('cache_tier_status', String(length=255))
    quota = Column('quota', Integer(), default=0)
    storage_pools.create_column(cache_tier_status)
    storage_pools.create_column(quota)
    storage_groups = Table('storage_groups', meta, autoload=True)


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_pools = Table('storage_pools', meta, autoload=True)
    storage_pools.drop_column('cache_tier_status')
    storage_pools.drop_column('quota')