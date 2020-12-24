# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/055_add_is_glance_store_pool_to_storage_pool_usages.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column
from sqlalchemy import MetaData
from sqlalchemy import Table

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_pool_usages = Table('storage_pool_usages', meta, autoload=True)
    as_glance_store_pool = Column('as_glance_store_pool', Boolean, default=False)
    try:
        storage_pool_usages.create_column(as_glance_store_pool)
    except Exception:
        raise


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_pool_usages = Table('storage_pool_usages', meta, autoload=True)
    as_glance_store_pool = Column('as_glance_store_pool', Boolean, default=False)
    try:
        storage_pool_usages.drop_column(as_glance_store_pool)
    except Exception:
        raise