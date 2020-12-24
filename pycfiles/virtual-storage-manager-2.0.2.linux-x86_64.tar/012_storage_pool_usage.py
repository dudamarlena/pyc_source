# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/012_storage_pool_usage.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy import Integer, MetaData, String, Table
from vsm.db.sqlalchemy import models

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_pool_usages = Table('storage_pool_usages', meta, Column('id', Integer, primary_key=True, nullable=False), Column('pool_id', Integer, ForeignKey(models.StoragePool.id), nullable=False), Column('vsmapp_id', Integer, ForeignKey(models.Vsmapp.id), nullable=False), Column('attach_status', String(length=255), nullable=False), Column('attach_at', DateTime(timezone=False)), Column('terminate_at', DateTime(timezone=False)), Column('created_at', DateTime(timezone=False)), Column('updated_at', DateTime(timezone=False)), Column('deleted_at', DateTime(timezone=False)), Column('deleted', Boolean(create_constraint=True, name=None), default=False))
    try:
        storage_pool_usages.create()
    except Exception:
        meta.drop_all(tables=[storage_pool_usages])
        raise

    return


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    table = Table('storage_pool_usages', meta, autoload=True)
    table.drop()