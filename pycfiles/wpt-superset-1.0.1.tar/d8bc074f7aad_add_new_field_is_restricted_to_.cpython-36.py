# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leonardo/proyectos/dashboard/incubator-superset/superset/migrations/versions/d8bc074f7aad_add_new_field_is_restricted_to_.py
# Compiled at: 2019-01-19 16:19:59
# Size of source mod 2**32: 2513 bytes
"""Add new field 'is_restricted' to SqlMetric and DruidMetric

Revision ID: d8bc074f7aad
Revises: 1226819ee0e3
Create Date: 2016-06-07 12:33:25.756640

"""
revision = 'd8bc074f7aad'
down_revision = '1226819ee0e3'
from alembic import op
import sqlalchemy as sa
from superset import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Boolean
Base = declarative_base()

class DruidMetric(Base):
    __doc__ = 'Declarative class used to do query in upgrade'
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True)
    is_restricted = Column(Boolean, default=False, nullable=True)


class SqlMetric(Base):
    __doc__ = 'Declarative class used to do query in upgrade'
    __tablename__ = 'sql_metrics'
    id = Column(Integer, primary_key=True)
    is_restricted = Column(Boolean, default=False, nullable=True)


def upgrade():
    op.add_column('metrics', sa.Column('is_restricted', (sa.Boolean()), nullable=True))
    op.add_column('sql_metrics', sa.Column('is_restricted', (sa.Boolean()), nullable=True))
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for obj in session.query(DruidMetric).all():
        obj.is_restricted = False

    for obj in session.query(SqlMetric).all():
        obj.is_restricted = False

    session.commit()
    session.close()


def downgrade():
    with op.batch_alter_table('sql_metrics', schema=None) as (batch_op):
        batch_op.drop_column('is_restricted')
    with op.batch_alter_table('metrics', schema=None) as (batch_op):
        batch_op.drop_column('is_restricted')