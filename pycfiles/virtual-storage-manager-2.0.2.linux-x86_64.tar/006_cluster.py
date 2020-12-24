# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/006_cluster.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Integer, MetaData, String, Table
from sqlalchemy import Table, Text

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    ceph_cluster = Table('clusters', meta, Column('id', Integer, primary_key=True, nullable=False), Column('name', String(length=255), nullable=True), Column('file_system', String(length=255), nullable=True), Column('primary_public_network', String(length=255), nullable=True), Column('secondary_public_network', String(length=255), nullable=True), Column('cluster_network', String(length=255), nullable=True), Column('journal_size', Integer, nullable=False), Column('size', Integer, nullable=True), Column('info_dict', Text(convert_unicode=False, unicode_error=None, _warn_on_bytestring=False), nullable=True), Column('ceph_conf', String(length=10485760), nullable=True), Column('deleted_times', Integer, nullable=True), Column('created_at', DateTime(timezone=False)), Column('updated_at', DateTime(timezone=False)), Column('deleted_at', DateTime(timezone=False)), Column('deleted', Boolean(create_constraint=True, name=None)))
    try:
        ceph_cluster.create()
    except Exception:
        meta.drop_all(tables=[ceph_cluster])
        raise

    return


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    ceph_cluster = Table('clusters', meta, autoload=True)
    ceph_cluster.drop()