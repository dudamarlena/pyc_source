# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/7dbf98566af7_slice_description.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1203 bytes
__doc__ = 'empty message\n\nRevision ID: 7dbf98566af7\nRevises: 8e80a26a31db\nCreate Date: 2016-01-17 22:00:23.640788\n\n'
revision = '7dbf98566af7'
down_revision = '8e80a26a31db'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('slices', sa.Column('description', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('slices', 'description')