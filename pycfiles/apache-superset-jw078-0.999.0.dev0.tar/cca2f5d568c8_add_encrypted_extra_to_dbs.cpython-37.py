# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/cca2f5d568c8_add_encrypted_extra_to_dbs.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1218 bytes
__doc__ = 'add encrypted_extra to dbs\n\nRevision ID: cca2f5d568c8\nRevises: b6fa807eac07\nCreate Date: 2019-10-09 15:05:06.965042\n\n'
revision = 'cca2f5d568c8'
down_revision = 'b6fa807eac07'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('dbs', sa.Column('encrypted_extra', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('dbs', 'encrypted_extra')