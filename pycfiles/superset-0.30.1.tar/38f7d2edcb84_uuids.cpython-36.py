# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/38f7d2edcb84_uuids.py
# Compiled at: 2019-07-11 00:43:39
# Size of source mod 2**32: 3926 bytes
"""Adds uuid columns to all classes with ImportExportMixin: dashboards, datasources, dbs, slices, tables
Revision ID: e5200a951e62
Revises: e9df189e5c7e
Create Date: 2019-05-08 13:42:48.479145
"""
import uuid
from alembic import op
from sqlalchemy import CHAR, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from superset import db
from superset.utils.sqla import get_uuid, uuid_sqla_column
revision = '38f7d2edcb84'
down_revision = 'b4a38aa87893'
Base = declarative_base()

class ImportExportMixin:
    id = Column(Integer, primary_key=True)
    uuid = uuid_sqla_column


class Dashboard(Base, ImportExportMixin):
    __tablename__ = 'dashboards'


class Datasource(Base, ImportExportMixin):
    __tablename__ = 'datasources'


class Database(Base, ImportExportMixin):
    __tablename__ = 'dbs'


class DruidCluster(Base, ImportExportMixin):
    __tablename__ = 'clusters'


class DruidMetric(Base, ImportExportMixin):
    __tablename__ = 'metrics'


class DruidColumn(Base, ImportExportMixin):
    __tablename__ = 'columns'


class Slice(Base, ImportExportMixin):
    __tablename__ = 'slices'


class SqlaTable(Base, ImportExportMixin):
    __tablename__ = 'tables'


class SqlMetric(Base, ImportExportMixin):
    __tablename__ = 'sql_metrics'


class TableColumn(Base, ImportExportMixin):
    __tablename__ = 'table_columns'


def batch_commit(iterable, mutator, session, batch_size=100):
    count = len(iterable)
    for i, obj in enumerate(iterable):
        mutator(obj)
        session.merge(obj)
        if i % 100 == 0:
            session.commit()
            print(f"uuid assigned to {i} out of {count}")

    session.commit()
    print(f"Done! Assigned {count} uuids")


def default_mutator(obj):
    obj.uuid = get_uuid()


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    db_type = session.bind.dialect.name

    def add_uuid_column(tbl_name, _type):
        print(f"Add uuid column to table '{tbl_name}'")
        with op.batch_alter_table(tbl_name) as (batch_op):
            batch_op.add_column(Column('uuid', (CHAR(36)), default=get_uuid))
        batch_commit(session.query(_type).all(), default_mutator, session)

    add_uuid_column('dashboards', Dashboard)
    add_uuid_column('datasources', Datasource)
    add_uuid_column('dbs', Database)
    add_uuid_column('clusters', DruidCluster)
    add_uuid_column('metrics', DruidMetric)
    add_uuid_column('columns', DruidColumn)
    add_uuid_column('slices', Slice)
    add_uuid_column('sql_metrics', SqlMetric)
    add_uuid_column('tables', SqlaTable)
    add_uuid_column('table_columns', TableColumn)
    session.close()


def downgrade():
    for tbl in ('dashboards', 'datasources', 'dbs', 'clusters', 'metrics', 'columns',
                'slices', 'sql_metrics', 'tables', 'table_columns'):
        try:
            with op.batch_alter_table(tbl) as (batch_op):
                batch_op.drop_column('uuid')
        except Exception:
            pass