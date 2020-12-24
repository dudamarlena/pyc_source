# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/008_storage_pool.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy import Integer, MetaData, String, Table
from vsm.db.sqlalchemy import models

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_pools = Table('storage_pools', meta, Column('id', Integer, primary_key=True, nullable=False), Column('pool_id', Integer, nullable=True), Column('name', String(length=255), nullable=False), Column('status', String(length=255), default='pending'), Column('recipe_id', Integer), Column('pg_num', Integer), Column('pgp_num', Integer), Column('size', Integer), Column('min_size', Integer), Column('crush_ruleset', Integer, ForeignKey(models.StorageGroup.rule_id, onupdate='CASCADE', ondelete='CASCADE')), Column('crash_replay_interval', Integer, nullable=True), Column('cluster_id', Integer, ForeignKey(models.Cluster.id), nullable=False), Column('created_by', String(length=50), nullable=False), Column('tag', String(length=16), nullable=False), Column('num_bytes', Integer), Column('num_objects', Integer), Column('num_object_clones', Integer), Column('num_objects_degraded', Integer), Column('num_objects_unfound', Integer), Column('num_read', Integer), Column('num_read_kb', Integer), Column('num_write', Integer), Column('num_write_kb', Integer), Column('read_bytes_sec', Integer), Column('write_bytes_sec', Integer), Column('op_per_sec', Integer), Column('created_at', DateTime(timezone=False)), Column('updated_at', DateTime(timezone=False)), Column('deleted_at', DateTime(timezone=False)), Column('deleted', Boolean(create_constraint=True, name=None)))
    try:
        storage_pools.create()
    except Exception:
        meta.drop_all(tables=[storage_pools])
        raise

    return


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_pools = Table('storage_pools', meta, autoload=True)
    storage_pools.drop()