# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/052_add_auto_growth_pg_storage_pool.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import and_, String, Column, MetaData, select, Table, Integer

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_pools = Table('storage_pools', meta, autoload=True)
    auto_growth_pg = Column('auto_growth_pg', Integer, nullable=False, default=0)
    storage_pools.create_column(auto_growth_pg)


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_pools = Table('storage_pools', meta, autoload=True)
    storage_pools.drop_column('auto_growth_pg')