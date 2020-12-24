# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/8504051e801b_xcom_dag_task_indices.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1321 bytes
__doc__ = 'xcom dag task indices\n\nRevision ID: 8504051e801b\nRevises: 4addfa1236f1\nCreate Date: 2016-11-29 08:13:03.253312\n\n'
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