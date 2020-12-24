# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/044_add_uuid_appnode.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Integer, MetaData, String
from sqlalchemy import Table, Index

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    appnodes = Table('appnodes', meta, autoload=True)
    uuid = Column('uuid', String(length=255), nullable=False)
    try:
        appnodes.create_column(uuid)
    except Exception:
        raise


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    appnodes = Table('appnodes', meta, autoload=True)
    uuid = Column('uuid', String(length=50), nullable=False)
    try:
        appnodes.drop_column(uuid)
    except Exception:
        raise