# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/018_license_status.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Integer, MetaData, Table

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    license_status = Table('license_status', meta, Column('id', Integer, primary_key=True), Column('license_accept', Boolean, default=False), Column('created_at', DateTime(timezone=False)), Column('updated_at', DateTime(timezone=False)), Column('deleted_at', DateTime(timezone=False)), Column('deleted', Boolean(create_constraint=True, name=None)))
    try:
        license_status.create()
    except Exception:
        meta.drop_all(tables=[license_status])
        raise

    return


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    license_status = Table('license_status', meta, autoload=True)
    license_status.drop()