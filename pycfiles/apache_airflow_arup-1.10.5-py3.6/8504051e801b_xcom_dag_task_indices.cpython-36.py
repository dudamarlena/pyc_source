# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/8504051e801b_xcom_dag_task_indices.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1321 bytes
"""xcom dag task indices

Revision ID: 8504051e801b
Revises: 4addfa1236f1
Create Date: 2016-11-29 08:13:03.253312

"""
from alembic import op
revision = '8504051e801b'
down_revision = '4addfa1236f1'
branch_labels = None
depends_on = None

def upgrade():
    op.create_index('idx_xcom_dag_task_date', 'xcom', [
     'dag_id', 'task_id', 'execution_date'],
      unique=False)


def downgrade():
    op.drop_index('idx_xcom_dag_task_date', table_name='xcom')