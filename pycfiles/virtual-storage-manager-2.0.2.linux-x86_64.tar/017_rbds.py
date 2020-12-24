# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/017_rbds.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy import Integer, BigInteger, MetaData, String, Text, Table
from vsm.db.sqlalchemy import models

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    rbds = Table('rbds', meta, Column('id', Integer, primary_key=True, nullable=False), Column('pool', String(length=255), nullable=False), Column('image', String(length=255), nullable=False), Column('size', BigInteger, nullable=False), Column('format', Integer, nullable=False), Column('objects', Integer, nullable=False), Column('order', Integer, nullable=False), Column('created_at', DateTime(timezone=False)), Column('updated_at', DateTime(timezone=False)), Column('deleted_at', DateTime(timezone=False)), Column('deleted', Boolean(create_constraint=True, name=None)))
    try:
        rbds.create()
    except Exception:
        meta.drop_all(tables=[rbds])
        raise

    return


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    rbds = Table('rbds', meta, autoload=True)
    rbds.drop()