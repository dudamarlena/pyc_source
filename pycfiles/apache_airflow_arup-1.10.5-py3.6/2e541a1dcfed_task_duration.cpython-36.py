# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/2e541a1dcfed_task_duration.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1530 bytes
"""task_duration

Revision ID: 2e541a1dcfed
Revises: 1b38cef5b76e
Create Date: 2015-10-28 20:38:41.266143

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
revision = '2e541a1dcfed'
down_revision = '1b38cef5b76e'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('task_instance') as (batch_op):
        batch_op.alter_column('duration', existing_type=mysql.INTEGER(display_width=11),
          type_=(sa.Float()),
          existing_nullable=True)


def downgrade():
    pass