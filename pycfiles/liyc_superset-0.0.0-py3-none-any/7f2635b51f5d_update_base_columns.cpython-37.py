# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pythonfile\hand_superset\superset\migrations\versions\7f2635b51f5d_update_base_columns.py
# Compiled at: 2019-08-01 07:27:28
# Size of source mod 2**32: 3967 bytes
"""update base columns

Note that the columns table was previously partially modifed by revision
f231d82b9b26.

Revision ID: 7f2635b51f5d
Revises: 937d04c16b64
Create Date: 2018-07-20 15:31:05.058050

"""
revision = '7f2635b51f5d'
down_revision = '937d04c16b64'
from alembic import op
from sqlalchemy import Column, engine, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from superset import db
from superset.utils.core import generic_find_uq_constraint_name
Base = declarative_base()
conv = {'uq': 'uq_%(table_name)s_%(column_0_name)s'}

class BaseColumnMixin:
    id = Column(Integer, primary_key=True)


class DruidColumn(BaseColumnMixin, Base):
    __tablename__ = 'columns'
    datasource_id = Column(Integer)


class TableColumn(BaseColumnMixin, Base):
    __tablename__ = 'table_columns'
    table_id = Column(Integer)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for record in session.query(DruidColumn).all():
        if record.datasource_id is None:
            session.delete(record)

    session.commit()
    with op.batch_alter_table('columns') as (batch_op):
        batch_op.alter_column('column_name', existing_type=(String(255)), nullable=False)
    for record in session.query(TableColumn).all():
        if record.table_id is None:
            session.delete(record)

    session.commit()
    with op.batch_alter_table('table_columns') as (batch_op):
        batch_op.alter_column('column_name',
          existing_type=(String(256)), nullable=False, type_=(String(255)))
    with op.batch_alter_table('table_columns', naming_convention=conv) as (batch_op):
        batch_op.create_unique_constraint('uq_table_columns_column_name', ['column_name', 'table_id'])


def downgrade():
    bind = op.get_bind()
    insp = engine.reflection.Inspector.from_engine(bind)
    with op.batch_alter_table('table_columns', naming_convention=conv) as (batch_op):
        batch_op.drop_constraint((generic_find_uq_constraint_name('table_columns', {'column_name', 'table_id'}, insp) or 'uq_table_columns_column_name'),
          type_='unique')
    with op.batch_alter_table('table_columns') as (batch_op):
        batch_op.alter_column('column_name',
          existing_type=(String(255)), nullable=True, type_=(String(256)))
    with op.batch_alter_table('columns') as (batch_op):
        batch_op.alter_column('column_name', existing_type=(String(255)), nullable=True)