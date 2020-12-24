# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/004c1210f153_increase_queue_name_size_limit.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1749 bytes
__doc__ = 'increase queue name size limit\n\nRevision ID: 004c1210f153\nRevises: 939bb1e647c8\nCreate Date: 2019-06-07 07:46:04.262275\n\n'
from alembic import op
import sqlalchemy as sa
revision = '004c1210f153'
down_revision = '939bb1e647c8'
branch_labels = None
depends_on = None

def upgrade():
    """
    Increase column size from 50 to 256 characters, closing AIRFLOW-4737 caused
    by broker backends that might use unusually large queue names.
    """
    with op.batch_alter_table('task_instance') as (batch_op):
        batch_op.alter_column('queue', type_=(sa.String(256)))


def downgrade():
    """
    Revert column size from 256 to 50 characters, might result in data loss.
    """
    with op.batch_alter_table('task_instance') as (batch_op):
        batch_op.alter_column('queue', type_=(sa.String(50)))