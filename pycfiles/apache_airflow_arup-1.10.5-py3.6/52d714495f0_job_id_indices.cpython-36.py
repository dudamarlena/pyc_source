# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/52d714495f0_job_id_indices.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1301 bytes
"""job_id indices

Revision ID: 52d714495f0
Revises: 338e90f54d61
Create Date: 2015-10-20 03:17:01.962542

"""
from alembic import op
revision = '52d714495f0'
down_revision = '338e90f54d61'
branch_labels = None
depends_on = None

def upgrade():
    op.create_index('idx_job_state_heartbeat', 'job', [
     'state', 'latest_heartbeat'],
      unique=False)


def downgrade():
    op.drop_index('idx_job_state_heartbeat', table_name='job')