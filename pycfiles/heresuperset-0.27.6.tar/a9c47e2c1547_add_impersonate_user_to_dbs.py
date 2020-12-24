# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moretti/PycharmProjects/incubator-superset/superset/migrations/versions/a9c47e2c1547_add_impersonate_user_to_dbs.py
# Compiled at: 2018-08-15 11:21:52
"""add impersonate_user to dbs

Revision ID: a9c47e2c1547
Revises: ca69c70ec99b
Create Date: 2017-08-31 17:35:58.230723

"""
revision = 'a9c47e2c1547'
down_revision = 'ca69c70ec99b'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('dbs', sa.Column('impersonate_user', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('dbs', 'impersonate_user')