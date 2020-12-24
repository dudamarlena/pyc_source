# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/041_add_parent_id_zone.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import and_, String, Column, MetaData, select, Table, Integer

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    zones = Table('zones', meta, autoload=True)
    parent_id = Column('parent_id', Integer, nullable=True)
    zones.create_column(parent_id)
    type = Column('type', Integer)
    zones.create_column(type)


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    zones = Table('zones', meta, autoload=True)
    zones.drop_column('parent_id')
    zones = Table('zones', meta, autoload=True)
    zones.drop_column('type')