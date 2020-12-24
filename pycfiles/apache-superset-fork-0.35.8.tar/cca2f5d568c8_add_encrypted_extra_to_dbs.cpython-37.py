# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/cca2f5d568c8_add_encrypted_extra_to_dbs.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1218 bytes
"""add encrypted_extra to dbs

Revision ID: cca2f5d568c8
Revises: b6fa807eac07
Create Date: 2019-10-09 15:05:06.965042

"""
revision = 'cca2f5d568c8'
down_revision = 'b6fa807eac07'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('dbs', sa.Column('encrypted_extra', (sa.Text()), nullable=True))


def downgrade():
    op.drop_column('dbs', 'encrypted_extra')