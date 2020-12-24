# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/12d55656cbca_is_featured.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1204 bytes
__doc__ = 'is_featured\n\nRevision ID: 12d55656cbca\nRevises: 55179c7f25c7\nCreate Date: 2015-12-14 13:37:17.374852\n\n'
revision = '12d55656cbca'
down_revision = '55179c7f25c7'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('tables', sa.Column('is_featured', (sa.Boolean()), nullable=True))


def downgrade():
    op.drop_column('tables', 'is_featured')