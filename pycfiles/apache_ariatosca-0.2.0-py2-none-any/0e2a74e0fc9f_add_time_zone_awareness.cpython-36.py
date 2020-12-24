# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/0e2a74e0fc9f_add_time_zone_awareness.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 16167 bytes
__doc__ = 'Add time zone awareness\n\nRevision ID: 0e2a74e0fc9f\nRevises: d2ae31099d61\nCreate Date: 2017-11-10 22:22:31.326152\n\n'
from alembic import op
from sqlalchemy.dialects import mysql
import sqlalchemy as sa
revision = '0e2a74e0fc9f'
down_revision = 'd2ae31099d61'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    if conn.dialect.name == 'mysql':
        conn.execute("SET time_zone = '+00:00'")
        cur = conn.execute('SELECT @@explicit_defaults_for_timestamp')
        res = cur.fetchall()
        if res[0][0] == 0:
            raise Exception('Global variable explicit_defaults_for_timestamp needs to be on (1) for mysql')
        op.alter_column(table_name='chart',
          column_name='last_modified',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='dag',
          column_name='last_scheduler_run',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='dag',
          column_name='last_pickled',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='dag',
          column_name='last_expired',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='dag_pickle',
          column_name='created_dttm',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='dag_run',
          column_name='execution_date',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='dag_run',
          column_name='start_date',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='dag_run',
          column_name='end_date',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='import_error',
          column_name='timestamp',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='job',
          column_name='start_date',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='job',
          column_name='end_date',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='job',
          column_name='latest_heartbeat',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='log',
          column_name='dttm',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='log',
          column_name='execution_date',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='sla_miss',
          column_name='execution_date',
          type_=mysql.TIMESTAMP(fsp=6),
          nullable=False)
        op.alter_column(table_name='sla_miss',
          column_name='timestamp',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='task_fail',
          column_name='execution_date',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='task_fail',
          column_name='start_date',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='task_fail',
          column_name='end_date',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='task_instance',
          column_name='execution_date',
          type_=mysql.TIMESTAMP(fsp=6),
          nullable=False)
        op.alter_column(table_name='task_instance',
          column_name='start_date',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='task_instance',
          column_name='end_date',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='task_instance',
          column_name='queued_dttm',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='xcom',
          column_name='timestamp',
          type_=mysql.TIMESTAMP(fsp=6))
        op.alter_column(table_name='xcom',
          column_name='execution_date',
          type_=mysql.TIMESTAMP(fsp=6))
    else:
        if conn.dialect.name in ('sqlite', 'mssql'):
            return
        if conn.dialect.name == 'postgresql':
            conn.execute('set timezone=UTC')
        op.alter_column(table_name='chart',
          column_name='last_modified',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='dag',
          column_name='last_scheduler_run',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='dag',
          column_name='last_pickled',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='dag',
          column_name='last_expired',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='dag_pickle',
          column_name='created_dttm',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='dag_run',
          column_name='execution_date',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='dag_run',
          column_name='start_date',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='dag_run',
          column_name='end_date',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='import_error',
          column_name='timestamp',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='job',
          column_name='start_date',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='job',
          column_name='end_date',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='job',
          column_name='latest_heartbeat',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='log',
          column_name='dttm',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='log',
          column_name='execution_date',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='sla_miss',
          column_name='execution_date',
          type_=sa.TIMESTAMP(timezone=True),
          nullable=False)
        op.alter_column(table_name='sla_miss',
          column_name='timestamp',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='task_fail',
          column_name='execution_date',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='task_fail',
          column_name='start_date',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='task_fail',
          column_name='end_date',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='task_instance',
          column_name='execution_date',
          type_=sa.TIMESTAMP(timezone=True),
          nullable=False)
        op.alter_column(table_name='task_instance',
          column_name='start_date',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='task_instance',
          column_name='end_date',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='task_instance',
          column_name='queued_dttm',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='xcom',
          column_name='timestamp',
          type_=sa.TIMESTAMP(timezone=True))
        op.alter_column(table_name='xcom',
          column_name='execution_date',
          type_=sa.TIMESTAMP(timezone=True))


def downgrade():
    conn = op.get_bind()
    if conn.dialect.name == 'mysql':
        conn.execute("SET time_zone = '+00:00'")
        op.alter_column(table_name='chart',
          column_name='last_modified',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='dag',
          column_name='last_scheduler_run',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='dag',
          column_name='last_pickled',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='dag',
          column_name='last_expired',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='dag_pickle',
          column_name='created_dttm',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='dag_run',
          column_name='execution_date',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='dag_run',
          column_name='start_date',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='dag_run',
          column_name='end_date',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='import_error',
          column_name='DATETIME',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='job',
          column_name='start_date',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='job',
          column_name='end_date',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='job',
          column_name='latest_heartbeat',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='log',
          column_name='dttm',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='log',
          column_name='execution_date',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='sla_miss',
          column_name='execution_date',
          type_=mysql.DATETIME(fsp=6),
          nullable=False)
        op.alter_column(table_name='sla_miss',
          column_name='DATETIME',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='task_fail',
          column_name='execution_date',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='task_fail',
          column_name='start_date',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='task_fail',
          column_name='end_date',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='task_instance',
          column_name='execution_date',
          type_=mysql.DATETIME(fsp=6),
          nullable=False)
        op.alter_column(table_name='task_instance',
          column_name='start_date',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='task_instance',
          column_name='end_date',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='task_instance',
          column_name='queued_dttm',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='xcom',
          column_name='DATETIME',
          type_=mysql.DATETIME(fsp=6))
        op.alter_column(table_name='xcom',
          column_name='execution_date',
          type_=mysql.DATETIME(fsp=6))
    else:
        if conn.dialect.name in ('sqlite', 'mssql'):
            return
        if conn.dialect.name == 'postgresql':
            conn.execute('set timezone=UTC')
        op.alter_column(table_name='chart',
          column_name='last_modified',
          type_=(sa.DateTime()))
        op.alter_column(table_name='dag',
          column_name='last_scheduler_run',
          type_=(sa.DateTime()))
        op.alter_column(table_name='dag',
          column_name='last_pickled',
          type_=(sa.DateTime()))
        op.alter_column(table_name='dag',
          column_name='last_expired',
          type_=(sa.DateTime()))
        op.alter_column(table_name='dag_pickle',
          column_name='created_dttm',
          type_=(sa.DateTime()))
        op.alter_column(table_name='dag_run',
          column_name='execution_date',
          type_=(sa.DateTime()))
        op.alter_column(table_name='dag_run',
          column_name='start_date',
          type_=(sa.DateTime()))
        op.alter_column(table_name='dag_run',
          column_name='end_date',
          type_=(sa.DateTime()))
        op.alter_column(table_name='import_error',
          column_name='timestamp',
          type_=(sa.DateTime()))
        op.alter_column(table_name='job', column_name='start_date', type_=(sa.DateTime()))
        op.alter_column(table_name='job', column_name='end_date', type_=(sa.DateTime()))
        op.alter_column(table_name='job',
          column_name='latest_heartbeat',
          type_=(sa.DateTime()))
        op.alter_column(table_name='log', column_name='dttm', type_=(sa.DateTime()))
        op.alter_column(table_name='log',
          column_name='execution_date',
          type_=(sa.DateTime()))
        op.alter_column(table_name='sla_miss',
          column_name='execution_date',
          type_=(sa.DateTime()),
          nullable=False)
        op.alter_column(table_name='sla_miss',
          column_name='timestamp',
          type_=(sa.DateTime()))
        op.alter_column(table_name='task_fail',
          column_name='execution_date',
          type_=(sa.DateTime()))
        op.alter_column(table_name='task_fail',
          column_name='start_date',
          type_=(sa.DateTime()))
        op.alter_column(table_name='task_fail',
          column_name='end_date',
          type_=(sa.DateTime()))
        op.alter_column(table_name='task_instance',
          column_name='execution_date',
          type_=(sa.DateTime()),
          nullable=False)
        op.alter_column(table_name='task_instance',
          column_name='start_date',
          type_=(sa.DateTime()))
        op.alter_column(table_name='task_instance',
          column_name='end_date',
          type_=(sa.DateTime()))
        op.alter_column(table_name='task_instance',
          column_name='queued_dttm',
          type_=(sa.DateTime()))
        op.alter_column(table_name='xcom', column_name='timestamp', type_=(sa.DateTime()))
        op.alter_column(table_name='xcom',
          column_name='execution_date',
          type_=(sa.DateTime()))