# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/051_metrics_add_index_on_timestamp.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy import Integer, MetaData, String, Table
from sqlalchemy import Table, Text, Float, Index

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    metrics = Table('metrics', meta, autoload=True)
    metrics_timestamp_index = Index('metrics_timestamp_index', metrics.columns.timestamp)
    metrics_timestamp_index.create(bind=migrate_engine)


def downgrade(migrate_engine):
    pass