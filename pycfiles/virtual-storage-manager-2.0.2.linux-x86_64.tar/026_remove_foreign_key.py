# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/026_remove_foreign_key.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Integer, MetaData, String
from sqlalchemy import Table, Index, ForeignKey
from sqlalchemy.engine.base import Engine
from migrate.changeset.constraint import ForeignKeyConstraint
from sqlalchemy.engine import reflection
from sqlalchemy import create_engine

def upgrade(migrate_engine):
    if migrate_engine.name == 'sqlite':
        return
    storage_pools = 'storage_pools'
    storage_groups = 'storage_groups'
    col = ''
    insp = reflection.Inspector.from_engine(migrate_engine)
    foreign_keys = insp.get_foreign_keys(storage_pools)
    for key in foreign_keys:
        if storage_groups == key['referred_table']:
            sql_str = 'ALTER TABLE %s DROP FOREIGN KEY %s;' % (storage_pools, key['name'])
            ret = migrate_engine.execute(sql_str)


def downgrade(migrate_engine):
    if migrate_engine.name == 'sqlite':
        return
    try:
        pass
    except Exception:
        raise