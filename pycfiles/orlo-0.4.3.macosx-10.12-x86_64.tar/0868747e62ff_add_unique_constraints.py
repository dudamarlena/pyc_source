# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/orlo/migrations/0868747e62ff_add_unique_constraints.py
# Compiled at: 2017-04-11 12:30:39
"""Add unique constraints

Revision ID: 0868747e62ff
Revises: e60a77e44da8
Create Date: 2017-04-11 16:10:42.109777

"""
from alembic import op
import sqlalchemy as sa
revision = '0868747e62ff'
down_revision = 'e60a77e44da8'
branch_labels = ()
depends_on = None

def upgrade():
    op.create_unique_constraint(None, 'package', ['id'])
    op.create_unique_constraint(None, 'package_result', ['id'])
    op.create_unique_constraint(None, 'platform', ['id'])
    op.create_unique_constraint(None, 'release', ['id'])
    op.create_unique_constraint(None, 'release_metadata', ['id'])
    op.create_unique_constraint(None, 'release_note', ['id'])
    return


def downgrade():
    op.drop_constraint(None, 'release_note', type_='unique')
    op.drop_constraint(None, 'release_metadata', type_='unique')
    op.drop_constraint(None, 'release', type_='unique')
    op.drop_constraint(None, 'platform', type_='unique')
    op.drop_constraint(None, 'package_result', type_='unique')
    op.drop_constraint(None, 'package', type_='unique')
    return