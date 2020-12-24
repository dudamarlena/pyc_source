# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/bba5a7cfc896_add_a_column_to_track_the_encryption_.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1374 bytes
"""Add a column to track the encryption state of the 'Extra' field in connection

Revision ID: bba5a7cfc896
Revises: bbc73705a13e
Create Date: 2016-01-29 15:10:32.656425

"""
from alembic import op
import sqlalchemy as sa
revision = 'bba5a7cfc896'
down_revision = 'bbc73705a13e'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('connection', sa.Column('is_extra_encrypted', (sa.Boolean), default=False))


def downgrade():
    op.drop_column('connection', 'is_extra_encrypted')