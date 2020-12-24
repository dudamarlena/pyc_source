# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/f18570e03440_add_query_result_key_index.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1260 bytes
"""Add index on the result key to the query table.

Revision ID: f18570e03440
Revises: 1296d28ec131
Create Date: 2017-01-24 12:40:42.494787

"""
from alembic import op
revision = 'f18570e03440'
down_revision = '1296d28ec131'

def upgrade():
    op.create_index((op.f('ix_query_results_key')),
      'query', ['results_key'], unique=False)


def downgrade():
    op.drop_index((op.f('ix_query_results_key')), table_name='query')