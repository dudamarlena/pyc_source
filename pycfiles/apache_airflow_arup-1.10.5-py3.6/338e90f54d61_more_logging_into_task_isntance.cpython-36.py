# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/338e90f54d61_more_logging_into_task_isntance.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1449 bytes
"""More logging into task_instance

Revision ID: 338e90f54d61
Revises: 13eb55f81627
Create Date: 2015-08-25 06:09:20.460147

"""
from alembic import op
import sqlalchemy as sa
revision = '338e90f54d61'
down_revision = '13eb55f81627'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('task_instance', sa.Column('operator', sa.String(length=1000), nullable=True))
    op.add_column('task_instance', sa.Column('queued_dttm', (sa.DateTime()), nullable=True))


def downgrade():
    op.drop_column('task_instance', 'queued_dttm')
    op.drop_column('task_instance', 'operator')