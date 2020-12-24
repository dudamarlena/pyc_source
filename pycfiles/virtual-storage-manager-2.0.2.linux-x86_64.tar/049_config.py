# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/049_config.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime, Text
from sqlalchemy import Integer, MetaData, String, Table

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    config = Table('config', meta, Column('id', Integer, primary_key=True, nullable=False), Column('name', String(length=255), nullable=False), Column('value', String(length=255), nullable=True), Column('default_value', String(length=255), nullable=False), Column('category', String(length=255), nullable=True), Column('section', String(length=255), nullable=False), Column('description', String(length=255), nullable=True), Column('alterable', Boolean(create_constraint=True, name=None)), Column('created_at', DateTime(timezone=False)), Column('updated_at', DateTime(timezone=False)), Column('deleted_at', DateTime(timezone=False)), Column('deleted', Boolean(create_constraint=True, name=None)))
    try:
        config.create()
    except Exception:
        meta.drop_all(tables=[config])
        raise

    return


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    configs = Table('config', meta, autoload=True)
    configs.drop()