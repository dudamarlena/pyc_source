# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moretti/PycharmProjects/incubator-superset/superset/migrations/versions/12d55656cbca_is_featured.py
# Compiled at: 2018-08-15 11:21:52
"""is_featured

Revision ID: 12d55656cbca
Revises: 55179c7f25c7
Create Date: 2015-12-14 13:37:17.374852

"""
revision = '12d55656cbca'
down_revision = '55179c7f25c7'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('tables', sa.Column('is_featured', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('tables', 'is_featured')