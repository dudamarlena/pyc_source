# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/a6c18f869a4e_query_start_running_time.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1294 bytes
__doc__ = 'query.start_running_time\n\nRevision ID: a6c18f869a4e\nRevises: 979c03af3341\nCreate Date: 2017-03-28 11:28:41.387182\n\n'
import sqlalchemy as sa
from alembic import op
revision = 'a6c18f869a4e'
down_revision = '979c03af3341'

def upgrade():
    op.add_column('query', sa.Column('start_running_time',
      sa.Numeric(precision=20, scale=6), nullable=True))


def downgrade():
    op.drop_column('query', 'start_running_time')