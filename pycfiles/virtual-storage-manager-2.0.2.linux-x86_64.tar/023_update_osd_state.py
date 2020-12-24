# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/023_update_osd_state.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Integer, MetaData, String
from sqlalchemy import Table, Index

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    osd_state = Table('osd_states', meta, autoload=True)
    column_status = Column('zone_id', Integer, nullable=False)
    try:
        osd_state.create_column(column_status)
    except Exception:
        raise


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    storage_group = Table('osd_states', meta, autoload=True)
    column_status = Column('zone_id', Integer, nullable=False)
    try:
        storage_group.drop_column(column_status)
    except Exception:
        raise