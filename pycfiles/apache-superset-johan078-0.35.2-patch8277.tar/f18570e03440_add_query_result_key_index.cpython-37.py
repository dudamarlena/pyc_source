# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/f18570e03440_add_query_result_key_index.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1260 bytes
__doc__ = 'Add index on the result key to the query table.\n\nRevision ID: f18570e03440\nRevises: 1296d28ec131\nCreate Date: 2017-01-24 12:40:42.494787\n\n'
from alembic import op
revision = 'f18570e03440'
down_revision = '1296d28ec131'

def upgrade():
    op.create_index((op.f('ix_query_results_key')),
      'query', ['results_key'], unique=False)


def downgrade():
    op.drop_index((op.f('ix_query_results_key')), table_name='query')