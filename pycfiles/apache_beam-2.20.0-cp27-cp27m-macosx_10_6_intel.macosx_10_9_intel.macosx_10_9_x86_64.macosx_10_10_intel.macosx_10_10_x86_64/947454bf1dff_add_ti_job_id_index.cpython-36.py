# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/947454bf1dff_add_ti_job_id_index.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1261 bytes
__doc__ = 'add ti job_id index\n\nRevision ID: 947454bf1dff\nRevises: bdaa763e6c56\nCreate Date: 2017-08-15 15:12:13.845074\n\n'
from alembic import op
revision = '947454bf1dff'
down_revision = 'bdaa763e6c56'
branch_labels = None
depends_on = None

def upgrade():
    op.create_index('ti_job_id', 'task_instance', ['job_id'], unique=False)


def downgrade():
    op.drop_index('ti_job_id', table_name='task_instance')