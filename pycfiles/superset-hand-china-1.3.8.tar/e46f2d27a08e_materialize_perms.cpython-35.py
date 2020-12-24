# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ljf/superset/superset18/superset/migrations/versions/e46f2d27a08e_materialize_perms.py
# Compiled at: 2017-10-30 08:27:50
# Size of source mod 2**32: 672 bytes
"""materialize perms

Revision ID: e46f2d27a08e
Revises: c611f2b591b8
Create Date: 2016-11-14 15:23:32.594898

"""
revision = 'e46f2d27a08e'
down_revision = 'c611f2b591b8'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('datasources', sa.Column('perm', sa.String(length=1000), nullable=True))
    op.add_column('dbs', sa.Column('perm', sa.String(length=1000), nullable=True))
    op.add_column('tables', sa.Column('perm', sa.String(length=1000), nullable=True))


def downgrade():
    op.drop_column('tables', 'perm')
    op.drop_column('datasources', 'perm')
    op.drop_column('dbs', 'perm')