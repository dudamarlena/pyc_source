# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/003_osd_state.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy import Integer, MetaData, String, Table
from sqlalchemy import Table, Float
from vsm.db.sqlalchemy import models

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    osd_states = Table('osd_states', meta, Column('id', Integer, primary_key=True, nullable=False), Column('osd_name', String(length=255), nullable=False), Column('device_id', Integer, ForeignKey(models.Device.id), nullable=False), Column('storage_group_id', Integer, nullable=False), Column('service_id', Integer, nullable=False), Column('cluster_id', Integer), Column('state', String(length=255), nullable=False), Column('operation_status', String(length=255), nullable=False), Column('weight', Float, default=1.0, nullable=False), Column('public_ip', String(length=255)), Column('cluster_ip', String(length=255)), Column('created_at', DateTime(timezone=False)), Column('updated_at', DateTime(timezone=False)), Column('deleted_at', DateTime(timezone=False)), Column('deleted', Boolean(create_constraint=True, name=None)))
    try:
        osd_states.create()
    except Exception:
        meta.drop_all(tables=[osd_states])
        raise

    return


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    osd_states = Table('osd_states', meta, autoload=True)
    osd_states.drop()