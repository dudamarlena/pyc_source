# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/dd4ecb8fbee3_add_schedule_interval_to_dag.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1266 bytes
__doc__ = 'Add schedule interval to dag\n\nRevision ID: dd4ecb8fbee3\nRevises: c8ffec048a3b\nCreate Date: 2018-12-27 18:39:25.748032\n\n'
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