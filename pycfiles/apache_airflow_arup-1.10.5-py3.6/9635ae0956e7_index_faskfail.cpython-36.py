# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/9635ae0956e7_index_faskfail.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1327 bytes
"""index-faskfail

Revision ID: 9635ae0956e7
Revises: 856955da8476
Create Date: 2018-06-17 21:40:01.963540

"""
from alembic import op
revision = '9635ae0956e7'
down_revision = '856955da8476'
branch_labels = None
depends_on = None

def upgrade():
    op.create_index('idx_task_fail_dag_task_date', 'task_fail',
      [
     'dag_id', 'task_id', 'execution_date'],
      unique=False)


def downgrade():
    op.drop_index('idx_task_fail_dag_task_date', table_name='task_fail')