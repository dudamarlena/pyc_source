# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/e9df189e5c7e_update_base_metrics.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 4730 bytes
__doc__ = 'update base metrics\n\nNote that the metrics table was previously partially modifed by revision\nf231d82b9b26.\n\nRevision ID: e9df189e5c7e\nRevises: 7f2635b51f5d\nCreate Date: 2018-07-20 15:57:48.118304\n\n'
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
        batch_op.drop_constraint((generic_find_uq_constraint_name('sql_metrics', {'metric_name', 'table_id'}, insp) or ),
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