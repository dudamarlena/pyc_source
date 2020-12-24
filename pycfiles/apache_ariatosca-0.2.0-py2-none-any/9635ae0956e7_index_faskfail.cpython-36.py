# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/9635ae0956e7_index_faskfail.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1327 bytes
__doc__ = 'index-faskfail\n\nRevision ID: 9635ae0956e7\nRevises: 856955da8476\nCreate Date: 2018-06-17 21:40:01.963540\n\n'
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