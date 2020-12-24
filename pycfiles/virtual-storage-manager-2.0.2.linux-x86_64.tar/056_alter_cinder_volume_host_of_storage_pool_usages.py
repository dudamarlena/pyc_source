# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/056_alter_cinder_volume_host_of_storage_pool_usages.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import MetaData
from sqlalchemy import Table

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_pool_usages = Table('storage_pool_usages', meta, autoload=True)
    col_cinder_volume_host = getattr(storage_pool_usages.c, 'cinder_volume_host')
    col_cinder_volume_host.alter(nullable=True)


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_pool_usages = Table('storage_pool_usages', meta, autoload=True)
    col_cinder_volume_host = getattr(storage_pool_usages.c, 'cinder_volume_host')
    col_cinder_volume_host.alter(nullable=False)