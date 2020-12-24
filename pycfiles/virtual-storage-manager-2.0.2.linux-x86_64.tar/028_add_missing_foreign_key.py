# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/028_add_missing_foreign_key.py
# Compiled at: 2016-06-13 14:11:03
from migrate import ForeignKeyConstraint
from sqlalchemy import MetaData, Table
from sqlalchemy.sql.expression import select
from vsm.db.sqlalchemy import utils

def upgrade(migrate_engine):
    if migrate_engine.name == 'sqlite':
        return
    meta = MetaData(bind=migrate_engine)
    storage_pools = Table('storage_pools', meta, autoload=True)
    storage_groups = Table('storage_groups', meta, autoload=True)
    params = {'columns': [storage_pools.c.primary_storage_group_id], 'refcolumns': [
                    storage_groups.c.id]}
    if migrate_engine.name == 'mysql':
        params['name'] = ('_').join(('storage_pool', 'primary_storage_group_id', 'fkey'))
    fkey = ForeignKeyConstraint(**params)
    fkey.create()


def downgrade(migrate_engine):
    if migrate_engine.name == 'sqlite':
        return
    meta = MetaData(bind=migrate_engine)
    storage_pools = Table('storage_pools', meta, autoload=True)
    storage_groups = Table('storage_groups', meta, autolaod=True)
    params = {'columns': [storage_pools.c.primary_storage_group_id], 'refcolumns': [
                    storage_groups.c.id]}
    fkey = ForeignKeyConstraint(**params)
    fkey.drop()