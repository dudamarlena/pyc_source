# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/010_init_node.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy import Integer, MetaData, String, Table
from vsm.db.sqlalchemy import models

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    init_nodes = Table('init_nodes', meta, Column('id', Integer, primary_key=True, nullable=False), Column('host', String(length=255), nullable=True), Column('service_id', Integer(), nullable=True), Column('raw_ip', String(length=255), nullable=True), Column('primary_public_ip', String(length=255), nullable=True), Column('secondary_public_ip', String(length=255), nullable=True), Column('cluster_ip', String(length=255), nullable=True), Column('zone_id', Integer(), nullable=True), Column('mds', String(length=255), nullable=True), Column('type', String(length=255), nullable=True), Column('cluster_id', Integer, ForeignKey(models.Cluster.id), nullable=True), Column('data_drives_number', String(length=255), nullable=True), Column('status', String(length=255), nullable=True), Column('pre_status', String(length=255), nullable=True), Column('id_rsa_pub', String(length=1024), nullable=True), Column('created_at', DateTime(timezone=False)), Column('updated_at', DateTime(timezone=False)), Column('deleted_at', DateTime(timezone=False)), Column('deleted', Boolean(create_constraint=True, name=None)))
    try:
        init_nodes.create()
    except Exception:
        meta.drop_all(tables=[init_nodes])
        raise

    return


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    init_nodes = Table('init_nodes', meta, autoload=True)
    init_nodes.drop()