# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/035_modify_cluster.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import and_, String, Column, MetaData, select, Table, Integer

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    clusters = Table('clusters', meta, autoload=True)
    osd_heartbeat_interval = Column('osd_heartbeat_interval', Integer, nullable=True)
    osd_heartbeat_grace = Column('osd_heartbeat_grace', Integer, nullable=True)
    clusters.create_column(osd_heartbeat_interval)
    clusters.create_column(osd_heartbeat_grace)


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    clusters = Table('clusters', meta, autoload=True)
    clusters.drop_column('osd_heartbeat_interval')
    clusters.drop_column('osd_heartbeat_grace')