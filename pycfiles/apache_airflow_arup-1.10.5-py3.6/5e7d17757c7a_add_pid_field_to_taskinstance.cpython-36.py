# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/5e7d17757c7a_add_pid_field_to_taskinstance.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1245 bytes
"""add pid field to TaskInstance

Revision ID: 5e7d17757c7a
Revises: 8504051e801b
Create Date: 2016-12-07 15:51:37.119478

"""
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