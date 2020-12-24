# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/52d714495f0_job_id_indices.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1301 bytes
__doc__ = 'job_id indices\n\nRevision ID: 52d714495f0\nRevises: 338e90f54d61\nCreate Date: 2015-10-20 03:17:01.962542\n\n'
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