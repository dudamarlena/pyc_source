# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/dd4ecb8fbee3_add_schedule_interval_to_dag.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1266 bytes
"""Add schedule interval to dag

Revision ID: dd4ecb8fbee3
Revises: c8ffec048a3b
Create Date: 2018-12-27 18:39:25.748032

"""
from alembic import op
import sqlalchemy as sa
revision = 'dd4ecb8fbee3'
down_revision = 'c8ffec048a3b'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('dag', sa.Column('schedule_interval', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('dag', 'schedule_interval')