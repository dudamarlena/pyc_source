# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/1296d28ec131_druid_exports.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1260 bytes
__doc__ = 'Adds params to the datasource (druid) table\n\nRevision ID: 1296d28ec131\nRevises: 6414e83d82b7\nCreate Date: 2016-12-06 17:40:40.389652\n\n'
revision = '1296d28ec131'
down_revision = '6414e83d82b7'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('datasources', sa.Column('params', sa.String(length=1000), nullable=True))


def downgrade():
    op.drop_column('datasources', 'params')