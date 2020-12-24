# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/013_appnode.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy import Integer, MetaData, String, Text, Table
from vsm.db.sqlalchemy import models

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    appnodes = Table('appnodes', meta, Column('id', Integer, primary_key=True, nullable=False), Column('ip', String(length=50), nullable=False), Column('vsmapp_id', Integer, ForeignKey(models.Vsmapp.id), nullable=False), Column('ssh_status', String(length=50), nullable=True), Column('log_info', Text, nullable=True), Column('created_at', DateTime(timezone=False)), Column('updated_at', DateTime(timezone=False)), Column('deleted_at', DateTime(timezone=False)), Column('deleted', Boolean(create_constraint=True, name=None), default=False))
    try:
        appnodes.create()
    except Exception:
        meta.drop_all(tables=[appnodes])
        raise

    return


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    table = Table('appnodes', meta, autoload=True)
    table.drop()