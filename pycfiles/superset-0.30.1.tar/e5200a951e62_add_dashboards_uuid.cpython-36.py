# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/e5200a951e62_add_dashboards_uuid.py
# Compiled at: 2019-06-07 15:07:03
# Size of source mod 2**32: 5551 bytes
"""Adds uuid columns to all classes with ImportMixin: dashboards, datasources, dbs, slices, tables, dashboard_email_schedules, slice_email_schedules

Revision ID: e5200a951e62
Revises: e9df189e5c7e
Create Date: 2019-05-08 13:42:48.479145

"""
import uuid
from alembic import op
from sqlalchemy import Column, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.types.uuid import UUIDType
from superset import db
revision = 'e5200a951e62'
down_revision = 'afc69274c25a'
Base = declarative_base()
get_uuid = lambda : str(uuid.uuid4())

class Dashboard(Base):
    __tablename__ = 'dashboards'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType(binary=False), default=get_uuid)


class Datasource(Base):
    __tablename__ = 'datasources'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType(binary=False), default=get_uuid)


class Database(Base):
    __tablename__ = 'dbs'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType(binary=False), default=get_uuid)


class DruidCluster(Base):
    __tablename__ = 'clusters'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType(binary=False), default=get_uuid)


class DruidMetric(Base):
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType(binary=False), default=get_uuid)


class Slice(Base):
    __tablename__ = 'slices'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType(binary=False), default=get_uuid)


class SqlaTable(Base):
    __tablename__ = 'tables'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType(binary=False), default=get_uuid)


class SqlMetric(Base):
    __tablename__ = 'sql_metrics'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType(binary=False), default=get_uuid)


class TableColumn(Base):
    __tablename__ = 'table_columns'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType(binary=False), default=get_uuid)


class DashboardEmailSchedule(Base):
    __tablename__ = 'dashboard_email_schedules'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType(binary=False), default=get_uuid)


class SliceEmailSchedule(Base):
    __tablename__ = 'slice_email_schedules'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType(binary=False), default=get_uuid)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)

    def add_uuid_column(col_name, _type):
        with op.batch_alter_table(col_name) as (batch_op):
            batch_op.add_column(Column('uuid', UUIDType(binary=False), default=get_uuid))
        for s in session.query(_type):
            s.uuid = get_uuid()
            session.merge(s)

        with op.batch_alter_table(col_name) as (batch_op):
            batch_op.alter_column('uuid', existing_type=(CHAR(32)), new_column_name='uuid',
              nullable=False)
            batch_op.create_unique_constraint('uq_uuid', ['uuid'])
        session.commit()

    add_uuid_column('dashboards', Dashboard)
    add_uuid_column('datasources', Datasource)
    add_uuid_column('dbs', Database)
    add_uuid_column('clusters', DruidCluster)
    add_uuid_column('metrics', DruidMetric)
    add_uuid_column('slices', Slice)
    add_uuid_column('sql_metrics', SqlMetric)
    add_uuid_column('tables', SqlaTable)
    add_uuid_column('table_columns', TableColumn)
    add_uuid_column('dashboard_email_schedules', DashboardEmailSchedule)
    add_uuid_column('slice_email_schedules', SliceEmailSchedule)
    session.close()


def downgrade():
    with op.batch_alter_table('dashboards') as (batch_op):
        batch_op.drop_column('uuid')
    with op.batch_alter_table('datasources') as (batch_op):
        batch_op.drop_column('uuid')
    with op.batch_alter_table('dbs') as (batch_op):
        batch_op.drop_column('uuid')
    with op.batch_alter_table('clusters') as (batch_op):
        batch_op.drop_column('uuid')
    with op.batch_alter_table('metrics') as (batch_op):
        batch_op.drop_column('uuid')
    with op.batch_alter_table('slices') as (batch_op):
        batch_op.drop_column('uuid')
    with op.batch_alter_table('sql_metrics') as (batch_op):
        batch_op.drop_column('uuid')
    with op.batch_alter_table('tables') as (batch_op):
        batch_op.drop_column('uuid')
    with op.batch_alter_table('table_columns') as (batch_op):
        batch_op.drop_column('uuid')
    with op.batch_alter_table('dashboard_email_schedules') as (batch_op):
        batch_op.drop_column('uuid')
    with op.batch_alter_table('slice_email_schedules') as (batch_op):
        batch_op.drop_column('uuid')