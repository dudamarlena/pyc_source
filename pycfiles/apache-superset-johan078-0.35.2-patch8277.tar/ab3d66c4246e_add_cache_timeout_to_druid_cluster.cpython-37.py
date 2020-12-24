# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/ab3d66c4246e_add_cache_timeout_to_druid_cluster.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1235 bytes
__doc__ = 'add_cache_timeout_to_druid_cluster\n\nRevision ID: ab3d66c4246e\nRevises: eca4694defa7\nCreate Date: 2016-09-30 18:01:30.579760\n\n'
revision = 'ab3d66c4246e'
down_revision = 'eca4694defa7'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('clusters', sa.Column('cache_timeout', (sa.Integer()), nullable=True))


def downgrade():
    op.drop_column('clusters', 'cache_timeout')