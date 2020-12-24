# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/039_update_appnode.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Integer, MetaData, String
from sqlalchemy import Table, Index

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    appnodes = Table('appnodes', meta, autoload=True)
    ip = Column('ip', String(length=50), nullable=False)
    os_tenant_name = Column('os_tenant_name', String(length=50), nullable=False)
    os_username = Column('os_username', String(length=50), nullable=False)
    os_password = Column('os_password', String(length=50), nullable=False)
    os_auth_url = Column('os_auth_url', String(length=255), nullable=False)
    os_region_name = Column('os_region_name', String(length=255), nullable=True)
    try:
        appnodes.drop_column(ip)
        appnodes.create_column(os_tenant_name)
        appnodes.create_column(os_username)
        appnodes.create_column(os_password)
        appnodes.create_column(os_auth_url)
        appnodes.create_column(os_region_name)
    except Exception:
        raise


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    appnodes = Table('appnodes', meta, autoload=True)
    ip = Column('ip', String(length=50), nullable=False)
    os_tenant_name = Column('os_tenant_name', String(length=50), nullable=False)
    os_username = Column('os_username', String(length=50), nullable=False)
    os_password = Column('os_password', String(length=50), nullable=False)
    os_auth_url = Column('os_auth_url', String(length=255), nullable=False)
    os_region_name = Column('os_region_name', String(length=255), nullable=True)
    try:
        appnodes.create_column(ip)
        appnodes.drop_column(os_tenant_name)
        appnodes.drop_column(os_username)
        appnodes.drop_column(os_password)
        appnodes.drop_column(os_auth_url)
        appnodes.drop_column(os_region_name)
    except Exception:
        raise