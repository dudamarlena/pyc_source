# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/46f444d8b9b7_remove_coordinator_from_druid_cluster_.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1660 bytes
__doc__ = 'remove_coordinator_from_druid_cluster_model.py\n\nRevision ID: 46f444d8b9b7\nRevises: 4ce8df208545\nCreate Date: 2018-11-26 00:01:04.781119\n\n'
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