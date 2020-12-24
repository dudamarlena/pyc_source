# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/bf00311e1990_add_index_to_taskinstance.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1304 bytes
"""add index to taskinstance

Revision ID: bf00311e1990
Revises: dd25f486b8ea
Create Date: 2018-09-12 09:53:52.007433

"""
from alembic import op
revision = 'bf00311e1990'
down_revision = 'dd25f486b8ea'
branch_labels = None
depends_on = None

def upgrade():
    op.create_index('ti_dag_date',
      'task_instance',
      [
     'dag_id', 'execution_date'],
      unique=False)


def downgrade():
    op.drop_index('ti_dag_date', table_name='task_instance')