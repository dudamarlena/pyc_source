# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/db4b49eb0782_add_tables_for_sql_lab_state.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 4368 bytes
"""Add tables for SQL Lab state

Revision ID: db4b49eb0782
Revises: 78ee127d0d1d
Create Date: 2019-11-13 11:05:30.122167

"""
revision = 'db4b49eb0782'
down_revision = '78ee127d0d1d'
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

def upgrade():
    op.create_table('tab_state',
      sa.Column('created_on', (sa.DateTime()), nullable=True),
      sa.Column('changed_on', (sa.DateTime()), nullable=True),
      sa.Column('extra_json', (sa.Text()), nullable=True),
      sa.Column('id', (sa.Integer()), nullable=False, autoincrement=True),
      sa.Column('user_id', (sa.Integer()), nullable=True),
      sa.Column('label', sa.String(length=256), nullable=True),
      sa.Column('active', (sa.Boolean()), nullable=True),
      sa.Column('database_id', (sa.Integer()), nullable=True),
      sa.Column('schema', sa.String(length=256), nullable=True),
      sa.Column('sql', (sa.Text()), nullable=True),
      sa.Column('query_limit', (sa.Integer()), nullable=True),
      sa.Column('latest_query_id', (sa.String(11)), nullable=True),
      sa.Column('autorun', (sa.Boolean()), nullable=False, default=False),
      sa.Column('template_params', (sa.Text()), nullable=True),
      sa.Column('created_by_fk', (sa.Integer()), nullable=True),
      sa.Column('changed_by_fk', (sa.Integer()), nullable=True),
      (sa.ForeignKeyConstraint(['changed_by_fk'], ['ab_user.id'])),
      (sa.ForeignKeyConstraint(['created_by_fk'], ['ab_user.id'])),
      (sa.ForeignKeyConstraint(['database_id'], ['dbs.id'])),
      (sa.ForeignKeyConstraint(['latest_query_id'], ['query.client_id'])),
      (sa.ForeignKeyConstraint(['user_id'], ['ab_user.id'])),
      (sa.PrimaryKeyConstraint('id')),
      sqlite_autoincrement=True)
    op.create_index((op.f('ix_tab_state_id')), 'tab_state', ['id'], unique=True)
    op.create_table('table_schema',
      sa.Column('created_on', (sa.DateTime()), nullable=True),
      sa.Column('changed_on', (sa.DateTime()), nullable=True),
      sa.Column('extra_json', (sa.Text()), nullable=True),
      sa.Column('id', (sa.Integer()), nullable=False, autoincrement=True),
      sa.Column('tab_state_id', (sa.Integer()), nullable=True),
      sa.Column('database_id', (sa.Integer()), nullable=False),
      sa.Column('schema', sa.String(length=256), nullable=True),
      sa.Column('table', sa.String(length=256), nullable=True),
      sa.Column('description', (sa.Text()), nullable=True),
      sa.Column('expanded', (sa.Boolean()), nullable=True),
      sa.Column('created_by_fk', (sa.Integer()), nullable=True),
      sa.Column('changed_by_fk', (sa.Integer()), nullable=True),
      (sa.ForeignKeyConstraint(['changed_by_fk'], ['ab_user.id'])),
      (sa.ForeignKeyConstraint(['created_by_fk'], ['ab_user.id'])),
      (sa.ForeignKeyConstraint(['database_id'], ['dbs.id'])),
      sa.ForeignKeyConstraint(['tab_state_id'], ['tab_state.id'], ondelete='CASCADE'),
      (sa.PrimaryKeyConstraint('id')),
      sqlite_autoincrement=True)
    op.create_index((op.f('ix_table_schema_id')), 'table_schema', ['id'], unique=True)


def downgrade():
    op.drop_index((op.f('ix_table_schema_id')), table_name='table_schema')
    op.drop_table('table_schema')
    op.drop_index((op.f('ix_tab_state_id')), table_name='tab_state')
    op.drop_table('tab_state')