# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/836c0bf75904_cache_timeouts.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1621 bytes
"""cache_timeouts

Revision ID: 836c0bf75904
Revises: 18e88e1cc004
Create Date: 2016-03-17 08:40:03.186534

"""
revision = '836c0bf75904'
down_revision = '18e88e1cc004'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('datasources', sa.Column('cache_timeout', (sa.Integer()), nullable=True))
    op.add_column('dbs', sa.Column('cache_timeout', (sa.Integer()), nullable=True))
    op.add_column('slices', sa.Column('cache_timeout', (sa.Integer()), nullable=True))
    op.add_column('tables', sa.Column('cache_timeout', (sa.Integer()), nullable=True))


def downgrade():
    op.drop_column('tables', 'cache_timeout')
    op.drop_column('slices', 'cache_timeout')
    op.drop_column('dbs', 'cache_timeout')
    op.drop_column('datasources', 'cache_timeout')