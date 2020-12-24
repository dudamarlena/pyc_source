# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/1968acfc09e3_add_is_encrypted_column_to_variable_.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1303 bytes
"""add is_encrypted column to variable table

Revision ID: 1968acfc09e3
Revises: bba5a7cfc896
Create Date: 2016-02-02 17:20:55.692295

"""
from alembic import op
import sqlalchemy as sa
revision = '1968acfc09e3'
down_revision = 'bba5a7cfc896'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('variable', sa.Column('is_encrypted', (sa.Boolean), default=False))


def downgrade():
    op.drop_column('variable', 'is_encrypted')