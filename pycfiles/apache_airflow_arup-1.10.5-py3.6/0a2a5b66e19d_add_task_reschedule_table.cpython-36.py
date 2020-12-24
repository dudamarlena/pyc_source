# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/0a2a5b66e19d_add_task_reschedule_table.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 3052 bytes
"""add task_reschedule table

Revision ID: 0a2a5b66e19d
Revises: 9635ae0956e7
Create Date: 2018-06-17 22:50:00.053620

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
revision = '0a2a5b66e19d'
down_revision = '9635ae0956e7'
branch_labels = None
depends_on = None
TABLE_NAME = 'task_reschedule'
INDEX_NAME = 'idx_' + TABLE_NAME + '_dag_task_date'

def mssql_timestamp():
    return sa.DateTime()


def mysql_timestamp():
    return mysql.TIMESTAMP(fsp=6)


def sa_timestamp():
    return sa.TIMESTAMP(timezone=True)


def upgrade():
    conn = op.get_bind()
    if conn.dialect.name == 'mysql':
        timestamp = mysql_timestamp
    else:
        if conn.dialect.name == 'mssql':
            timestamp = mssql_timestamp
        else:
            timestamp = sa_timestamp
    op.create_table(TABLE_NAME, sa.Column('id', (sa.Integer()), nullable=False), sa.Column('task_id', sa.String(length=250), nullable=False), sa.Column('dag_id', sa.String(length=250), nullable=False), sa.Column('execution_date', (timestamp()), nullable=False, server_default=None), sa.Column('try_number', (sa.Integer()), nullable=False), sa.Column('start_date', (timestamp()), nullable=False), sa.Column('end_date', (timestamp()), nullable=False), sa.Column('duration', (sa.Integer()), nullable=False), sa.Column('reschedule_date', (timestamp()), nullable=False), sa.PrimaryKeyConstraint('id'), sa.ForeignKeyConstraint([
     'task_id', 'dag_id', 'execution_date'],
      [
     'task_instance.task_id', 'task_instance.dag_id', 'task_instance.execution_date'],
      name='task_reschedule_dag_task_date_fkey'))
    op.create_index(INDEX_NAME,
      TABLE_NAME,
      [
     'dag_id', 'task_id', 'execution_date'],
      unique=False)


def downgrade():
    op.drop_index(INDEX_NAME, table_name=TABLE_NAME)
    op.drop_table(TABLE_NAME)