# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/d8bc074f7aad_add_new_field_is_restricted_to_.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2526 bytes
__doc__ = "Add new field 'is_restricted' to SqlMetric and DruidMetric\n\nRevision ID: d8bc074f7aad\nRevises: 1226819ee0e3\nCreate Date: 2016-06-07 12:33:25.756640\n\n"
revision = 'd8bc074f7aad'
down_revision = '1226819ee0e3'
import sqlalchemy as sa
from alembic import op
from sqlalchemy import Boolean, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from superset import db
Base = declarative_base()

class DruidMetric(Base):
    """DruidMetric"""
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True)
    is_restricted = Column(Boolean, default=False, nullable=True)


class SqlMetric(Base):
    """SqlMetric"""
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