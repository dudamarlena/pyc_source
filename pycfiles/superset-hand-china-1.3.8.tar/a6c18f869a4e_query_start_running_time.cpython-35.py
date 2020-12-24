# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ljf/superset/superset18/superset/migrations/versions/a6c18f869a4e_query_start_running_time.py
# Compiled at: 2017-10-30 08:27:50
# Size of source mod 2**32: 497 bytes
"""query.start_running_time

Revision ID: a6c18f869a4e
Revises: 979c03af3341
Create Date: 2017-03-28 11:28:41.387182

"""
from alembic import op
import sqlalchemy as sa
revision = 'a6c18f869a4e'
down_revision = '979c03af3341'

def upgrade():
    op.add_column('query', sa.Column('start_running_time', sa.Numeric(precision=20, scale=6), nullable=True))


def downgrade():
    op.drop_column('query', 'start_running_time')