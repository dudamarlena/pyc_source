# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/002_device.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy import Integer, MetaData, String, Table
from sqlalchemy import Table, Text, Float

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    devices = Table('devices', meta, Column('id', Integer, primary_key=True, nullable=False), Column('name', String(length=255), nullable=False), Column('journal', String(length=255), nullable=True), Column('service_id', Integer, nullable=False), Column('total_capacity_kb', Integer, nullable=False, default=0), Column('used_capacity_kb', Integer, nullable=False, default=0), Column('avail_capacity_kb', Integer, nullable=False, default=0), Column('device_type', String(length=255), nullable=True), Column('interface_type', String(length=255)), Column('fs_type', String(length=255)), Column('mount_point', String(length=255)), Column('created_at', DateTime(timezone=False)), Column('updated_at', DateTime(timezone=False)), Column('deleted_at', DateTime(timezone=False)), Column('deleted', Boolean(create_constraint=True, name=None)), Column('state', String(length=255), default='MISSING'), Column('journal_state', String(length=255), default='MISSING'), Column('path', String(length=255), nullable=False))
    try:
        devices.create()
    except Exception:
        meta.drop_all(tables=[devices])
        raise

    return


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    devices = Table('devices', meta, autoload=True)
    devices.drop()