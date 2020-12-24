# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/a9c47e2c1547_add_impersonate_user_to_dbs.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 1223 bytes
"""add impersonate_user to dbs

Revision ID: a9c47e2c1547
Revises: ca69c70ec99b
Create Date: 2017-08-31 17:35:58.230723

"""
revision = 'a9c47e2c1547'
down_revision = 'ca69c70ec99b'
import sqlalchemy as sa
from alembic import op

def upgrade():
    op.add_column('dbs', sa.Column('impersonate_user', (sa.Boolean()), nullable=True))


def downgrade():
    op.drop_column('dbs', 'impersonate_user')