# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/1e2841a4128_.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1213 bytes
__doc__ = 'empty message\n\nRevision ID: 1e2841a4128\nRevises: 5a7bad26f2a7\nCreate Date: 2015-10-05 22:11:00.537054\n\n'
revision = '1e2841a4128'
down_revision = '5a7bad26f2a7'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('table_columns', sa.Column('expression', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('table_columns', 'expression')