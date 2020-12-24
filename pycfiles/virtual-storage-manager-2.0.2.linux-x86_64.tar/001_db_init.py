# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/001_db_init.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy import Integer, MetaData, String, Table
from sqlalchemy import Table, Text, Float

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    services = Table('services', meta, Column('created_at', DateTime), Column('updated_at', DateTime), Column('deleted_at', DateTime), Column('deleted', Boolean), Column('id', Integer, primary_key=True, nullable=False), Column('host', String(length=255)), Column('binary', String(length=255)), Column('topic', String(length=255)), Column('report_count', Integer, nullable=False), Column('disabled', Boolean), Column('availability_zone', String(length=255)))
    try:
        services.create()
    except Exception:
        meta.drop_all(tables=[services])
        raise


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    services = Table('services', meta, autoload=True)
    services.drop()