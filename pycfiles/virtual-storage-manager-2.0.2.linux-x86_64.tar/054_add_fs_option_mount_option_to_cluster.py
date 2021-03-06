# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/054_add_fs_option_mount_option_to_cluster.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Integer, MetaData, String
from sqlalchemy import Table, Index

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    clusters = Table('clusters', meta, autoload=True)
    mkfs_option = Column('mkfs_option', String(length=255))
    mount_option = Column('mount_option', String(length=255))
    try:
        clusters.create_column(mkfs_option)
        clusters.create_column(mount_option)
    except Exception:
        raise


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    clusters = Table('clusters', meta, autoload=True)
    mkfs_option = Column('mkfs_option', String(length=255))
    mount_option = Column('mount_option', String(length=255))
    try:
        clusters.drop_column(mkfs_option)
        clusters.drop_column(mount_option)
    except Exception:
        raise