# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/e9df189e5c7e_update_base_metrics.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 4730 bytes
"""update base metrics

Note that the metrics table was previously partially modifed by revision
f231d82b9b26.

Revision ID: e9df189e5c7e
Revises: 7f2635b51f5d
Create Date: 2018-07-20 15:57:48.118304

"""
revision = 'e9df189e5c7e'
down_revision = '7f2635b51f5d'
from alembic import op
from sqlalchemy import Column, engine, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from superset import db
from superset.utils.core import generic_find_uq_constraint_name
Base = declarative_base()
conv = {'uq': 'uq_%(table_name)s_%(column_0_name)s'}

class BaseMetricMixin:
    id = Column(Integer, primary_key=True)


class DruidMetric(BaseMetricMixin, Base):
    __tablename__ = 'metrics'
    datasource_id = Column(Integer)


class SqlMetric(BaseMetricMixin, Base):
    __tablename__ = 'sql_metrics'
    table_id = Column(Integer)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for record in session.query(DruidMetric).all():
        if record.datasource_id is None:
            session.delete(record)

    session.commit()
    with op.batch_alter_table('metrics') as (batch_op):
        batch_op.alter_column('metric_name', existing_type=(String(255)), nullable=False)
    with op.batch_alter_table('metrics') as (batch_op):
        batch_op.alter_column('json', existing_type=Text, nullable=False)
    for record in session.query(SqlMetric).all():
        if record.table_id is None:
            session.delete(record)

    session.commit()
    with op.batch_alter_table('sql_metrics') as (batch_op):
        batch_op.alter_column('metric_name',
          existing_type=(String(512)), nullable=False, type_=(String(255)))
    with op.batch_alter_table('sql_metrics') as (batch_op):
        batch_op.alter_column('expression', existing_type=Text, nullable=False)
    with op.batch_alter_table('sql_metrics', naming_convention=conv) as (batch_op):
        batch_op.create_unique_constraint('uq_sql_metrics_metric_name', ['metric_name', 'table_id'])


def downgrade():
    bind = op.get_bind()
    insp = engine.reflection.Inspector.from_engine(bind)
    with op.batch_alter_table('sql_metrics', naming_convention=conv) as (batch_op):
        batch_op.drop_constraint((generic_find_uq_constraint_name('sql_metrics', {'metric_name', 'table_id'}, insp) or 'uq_sql_metrics_table_id'),
          type_='unique')
    with op.batch_alter_table('sql_metrics') as (batch_op):
        batch_op.alter_column('metric_name',
          existing_type=(String(255)), nullable=True, type_=(String(512)))
    with op.batch_alter_table('sql_metrics') as (batch_op):
        batch_op.alter_column('expression', existing_type=Text, nullable=True)
    with op.batch_alter_table('metrics') as (batch_op):
        batch_op.alter_column('metric_name', existing_type=(String(255)), nullable=True)
    with op.batch_alter_table('metrics') as (batch_op):
        batch_op.alter_column('json', existing_type=Text, nullable=True)