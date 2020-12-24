# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/4addfa1236f1_add_fractional_seconds_to_mysql_tables.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 7940 bytes
"""Add fractional seconds to mysql tables

Revision ID: 4addfa1236f1
Revises: f2ca10b85618
Create Date: 2016-09-11 13:39:18.592072

"""
from alembic import op
from sqlalchemy.dialects import mysql
from alembic import context
revision = '4addfa1236f1'
down_revision = 'f2ca10b85618'
branch_labels = None
depends_on = None

def upgrade():
    if context.config.get_main_option('sqlalchemy.url').startswith('mysql'):
        op.alter_column(table_name='dag', column_name='last_scheduler_run', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='dag', column_name='last_pickled', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='dag', column_name='last_expired', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='dag_pickle', column_name='created_dttm', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='dag_run', column_name='execution_date', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='dag_run', column_name='start_date', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='dag_run', column_name='end_date', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='import_error', column_name='timestamp', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='job', column_name='start_date', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='job', column_name='end_date', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='job', column_name='latest_heartbeat', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='known_event', column_name='start_date', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='known_event', column_name='end_date', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='log', column_name='dttm', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='log', column_name='execution_date', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='sla_miss', column_name='execution_date', type_=mysql.DATETIME(fsp=6),
          nullable=False)
        op.alter_column(table_name='sla_miss', column_name='timestamp', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='task_fail', column_name='execution_date', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='task_fail', column_name='start_date', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='task_fail', column_name='end_date', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='task_instance', column_name='execution_date', type_=mysql.DATETIME(fsp=6),
          nullable=False)
        op.alter_column(table_name='task_instance', column_name='start_date', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='task_instance', column_name='end_date', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='task_instance', column_name='queued_dttm', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='xcom', column_name='timestamp', type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='xcom', column_name='execution_date', type_=mysql.DATETIME(fsp=6))


def downgrade():
    if context.config.get_main_option('sqlalchemy.url').startswith('mysql'):
        op.alter_column(table_name='dag', column_name='last_scheduler_run', type_=(mysql.DATETIME()))
        op.alter_column(table_name='dag', column_name='last_pickled', type_=(mysql.DATETIME()))
        op.alter_column(table_name='dag', column_name='last_expired', type_=(mysql.DATETIME()))
        op.alter_column(table_name='dag_pickle', column_name='created_dttm', type_=(mysql.DATETIME()))
        op.alter_column(table_name='dag_run', column_name='execution_date', type_=(mysql.DATETIME()))
        op.alter_column(table_name='dag_run', column_name='start_date', type_=(mysql.DATETIME()))
        op.alter_column(table_name='dag_run', column_name='end_date', type_=(mysql.DATETIME()))
        op.alter_column(table_name='import_error', column_name='timestamp', type_=(mysql.DATETIME()))
        op.alter_column(table_name='job', column_name='start_date', type_=(mysql.DATETIME()))
        op.alter_column(table_name='job', column_name='end_date', type_=(mysql.DATETIME()))
        op.alter_column(table_name='job', column_name='latest_heartbeat', type_=(mysql.DATETIME()))
        op.alter_column(table_name='known_event', column_name='start_date', type_=(mysql.DATETIME()))
        op.alter_column(table_name='known_event', column_name='end_date', type_=(mysql.DATETIME()))
        op.alter_column(table_name='log', column_name='dttm', type_=(mysql.DATETIME()))
        op.alter_column(table_name='log', column_name='execution_date', type_=(mysql.DATETIME()))
        op.alter_column(table_name='sla_miss', column_name='execution_date', type_=(mysql.DATETIME()),
          nullable=False)
        op.alter_column(table_name='sla_miss', column_name='timestamp', type_=(mysql.DATETIME()))
        op.alter_column(table_name='task_fail', column_name='execution_date', type_=(mysql.DATETIME()))
        op.alter_column(table_name='task_fail', column_name='start_date', type_=(mysql.DATETIME()))
        op.alter_column(table_name='task_fail', column_name='end_date', type_=(mysql.DATETIME()))
        op.alter_column(table_name='task_instance', column_name='execution_date', type_=(mysql.DATETIME()),
          nullable=False)
        op.alter_column(table_name='task_instance', column_name='start_date', type_=(mysql.DATETIME()))
        op.alter_column(table_name='task_instance', column_name='end_date', type_=(mysql.DATETIME()))
        op.alter_column(table_name='task_instance', column_name='queued_dttm', type_=(mysql.DATETIME()))
        op.alter_column(table_name='xcom', column_name='timestamp', type_=(mysql.DATETIME()))
        op.alter_column(table_name='xcom', column_name='execution_date', type_=(mysql.DATETIME()))