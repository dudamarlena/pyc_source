# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/7e3ddad2a00b_results_key_to_query.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1233 bytes
__doc__ = 'results_key to query\n\nRevision ID: 7e3ddad2a00b\nRevises: b46fa1b0b39e\nCreate Date: 2016-10-14 11:17:54.995156\n\n'
revision = '7e3ddad2a00b'
down_revision = 'b46fa1b0b39e'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('query', sa.Column('results_key', sa.String(length=64), nullable=True))


def downgrade():
    op.drop_column('query', 'results_key')