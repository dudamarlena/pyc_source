# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/025_primary_storage_group_id_to_storage_pools.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import and_, String, Column, MetaData, select, Table, Integer

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_pools = Table('storage_pools', meta, autoload=True)
    primary_storage_group_id = Column('primary_storage_group_id', Integer)
    storage_pools.create_column(primary_storage_group_id)
    storage_groups = Table('storage_groups', meta, autoload=True)
    q = select([
     storage_pools.c.id, storage_groups.c.id], whereclause=and_(storage_pools.c.deleted != True, storage_groups.c.deleted != True), from_obj=storage_pools.join(storage_groups, storage_pools.c.crush_ruleset == storage_groups.c.rule_id))
    for storage_pool_id, storage_group_id in q.execute():
        storage_pools.update().where(storage_pools.c.id == storage_pool_id).values(primary_storage_group_id=storage_group_id).execute()


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_pools = Table('storage_pools', meta, autoload=True)
    storage_pools.drop_column('primary_storage_group_id')