# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/005_test.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy import Integer, MetaData, String, Table
from sqlalchemy import Table, Text, Float

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    tests = Table('tests', meta, Column('id', Integer, primary_key=True, nullable=False), Column('device_id', Integer, unique=True, nullable=False), Column('service_id', Integer, nullable=False), Column('cluster_id', Integer), Column('state', String(length=255), unique=True, nullable=False), Column('created_at', DateTime(timezone=False)), Column('updated_at', DateTime(timezone=False)), Column('deleted_at', DateTime(timezone=False)), Column('deleted', Boolean(create_constraint=True, name=None)))
    try:
        tests.create()
    except Exception:
        meta.drop_all(tables=[tests])
        raise

    return


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    tests = Table('tests', meta, autoload=True)
    tests.drop()