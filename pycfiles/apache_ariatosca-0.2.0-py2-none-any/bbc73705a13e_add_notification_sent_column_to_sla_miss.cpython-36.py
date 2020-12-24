# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/bbc73705a13e_add_notification_sent_column_to_sla_miss.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1308 bytes
__doc__ = 'Add notification_sent column to sla_miss\n\nRevision ID: bbc73705a13e\nRevises: 4446e08588\nCreate Date: 2016-01-14 18:05:54.871682\n\n'
from alembic import op
import sqlalchemy as sa
revision = 'bbc73705a13e'
down_revision = '4446e08588'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('sla_miss', sa.Column('notification_sent', (sa.Boolean), default=False))


def downgrade():
    op.drop_column('sla_miss', 'notification_sent')