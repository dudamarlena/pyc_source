# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/27c6a30d7c24_add_executor_config_to_task_instance.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1365 bytes
"""kubernetes_resource_checkpointing

Revision ID: 33ae817a1ff4
Revises: 947454bf1dff
Create Date: 2017-09-11 15:26:47.598494

"""
from alembic import op
import sqlalchemy as sa, dill
revision = '27c6a30d7c24'
down_revision = '33ae817a1ff4'
branch_labels = None
depends_on = None
TASK_INSTANCE_TABLE = 'task_instance'
NEW_COLUMN = 'executor_config'

def upgrade():
    op.add_column(TASK_INSTANCE_TABLE, sa.Column(NEW_COLUMN, sa.PickleType(pickler=dill)))


def downgrade():
    op.drop_column(TASK_INSTANCE_TABLE, NEW_COLUMN)