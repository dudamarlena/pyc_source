# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/5e7d17757c7a_add_pid_field_to_taskinstance.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1245 bytes
__doc__ = 'add pid field to TaskInstance\n\nRevision ID: 5e7d17757c7a\nRevises: 8504051e801b\nCreate Date: 2016-12-07 15:51:37.119478\n\n'
from alembic import op
import sqlalchemy as sa
revision = '5e7d17757c7a'
down_revision = '8504051e801b'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('task_instance', sa.Column('pid', sa.Integer))


def downgrade():
    op.drop_column('task_instance', 'pid')