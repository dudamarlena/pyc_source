# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/bbc73705a13e_add_notification_sent_column_to_sla_miss.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1308 bytes
"""Add notification_sent column to sla_miss

Revision ID: bbc73705a13e
Revises: 4446e08588
Create Date: 2016-01-14 18:05:54.871682

"""
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