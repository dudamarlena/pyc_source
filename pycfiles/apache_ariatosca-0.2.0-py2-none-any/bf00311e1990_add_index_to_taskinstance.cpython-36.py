# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/bf00311e1990_add_index_to_taskinstance.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1304 bytes
__doc__ = 'add index to taskinstance\n\nRevision ID: bf00311e1990\nRevises: dd25f486b8ea\nCreate Date: 2018-09-12 09:53:52.007433\n\n'
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