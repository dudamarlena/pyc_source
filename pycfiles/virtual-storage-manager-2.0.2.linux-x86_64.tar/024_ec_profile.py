# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/024_ec_profile.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime, Text
from sqlalchemy import Integer, MetaData, String, Table

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    ec_profiles = Table('ec_profiles', meta, Column('id', Integer, primary_key=True, nullable=False), Column('name', String(length=255), nullable=False), Column('plugin', String(length=255), nullable=False), Column('plugin_path', String(length=255), nullable=False), Column('pg_num', Integer, nullable=False), Column('plugin_kv_pair', Text, nullable=False), Column('created_at', DateTime(timezone=False)), Column('updated_at', DateTime(timezone=False)), Column('deleted_at', DateTime(timezone=False)), Column('deleted', Boolean(create_constraint=True, name=None)))
    try:
        ec_profiles.create()
    except Exception:
        meta.drop_all(tables=[ec_profiles])
        raise

    return


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    ec_profiles = Table('ec_profiles', meta, autoload=True)
    ec_profiles.drop()