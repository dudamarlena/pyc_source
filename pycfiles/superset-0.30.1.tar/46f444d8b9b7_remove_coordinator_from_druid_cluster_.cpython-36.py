# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/46f444d8b9b7_remove_coordinator_from_druid_cluster_.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 1660 bytes
"""remove_coordinator_from_druid_cluster_model.py

Revision ID: 46f444d8b9b7
Revises: 4ce8df208545
Create Date: 2018-11-26 00:01:04.781119

"""
import sqlalchemy as sa
from alembic import op
revision = '46f444d8b9b7'
down_revision = '4ce8df208545'

def upgrade():
    with op.batch_alter_table('clusters') as (batch_op):
        batch_op.drop_column('coordinator_host')
        batch_op.drop_column('coordinator_endpoint')
        batch_op.drop_column('coordinator_port')


def downgrade():
    op.add_column('clusters', sa.Column('coordinator_host', sa.String(length=256), nullable=True))
    op.add_column('clusters', sa.Column('coordinator_port', (sa.Integer()), nullable=True))
    op.add_column('clusters', sa.Column('coordinator_endpoint', sa.String(length=256), nullable=True))