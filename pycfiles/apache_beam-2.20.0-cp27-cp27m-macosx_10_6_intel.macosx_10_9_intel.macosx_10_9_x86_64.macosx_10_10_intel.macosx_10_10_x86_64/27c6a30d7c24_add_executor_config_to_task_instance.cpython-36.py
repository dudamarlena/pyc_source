# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/27c6a30d7c24_add_executor_config_to_task_instance.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1365 bytes
__doc__ = 'kubernetes_resource_checkpointing\n\nRevision ID: 33ae817a1ff4\nRevises: 947454bf1dff\nCreate Date: 2017-09-11 15:26:47.598494\n\n'
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