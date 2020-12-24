# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/939bb1e647c8_task_reschedule_fk_on_cascade_delete.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1986 bytes
"""task reschedule fk on cascade delete

Revision ID: 939bb1e647c8
Revises: 4ebbffe0a39a
Create Date: 2019-02-04 20:21:50.669751

"""
from alembic import op
revision = '939bb1e647c8'
down_revision = 'dd4ecb8fbee3'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('task_reschedule') as (batch_op):
        batch_op.drop_constraint('task_reschedule_dag_task_date_fkey',
          type_='foreignkey')
        batch_op.create_foreign_key('task_reschedule_dag_task_date_fkey',
          'task_instance',
          [
         'task_id', 'dag_id', 'execution_date'],
          [
         'task_id', 'dag_id', 'execution_date'],
          ondelete='CASCADE')


def downgrade():
    with op.batch_alter_table('task_reschedule') as (batch_op):
        batch_op.drop_constraint('task_reschedule_dag_task_date_fkey',
          type_='foreignkey')
        batch_op.create_foreign_key('task_reschedule_dag_task_date_fkey', 'task_instance', [
         'task_id', 'dag_id', 'execution_date'], [
         'task_id', 'dag_id', 'execution_date'])