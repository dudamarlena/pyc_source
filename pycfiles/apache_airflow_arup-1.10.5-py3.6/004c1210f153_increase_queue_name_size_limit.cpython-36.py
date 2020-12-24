# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/004c1210f153_increase_queue_name_size_limit.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1749 bytes
"""increase queue name size limit

Revision ID: 004c1210f153
Revises: 939bb1e647c8
Create Date: 2019-06-07 07:46:04.262275

"""
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