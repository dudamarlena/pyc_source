# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leonardo/proyectos/dashboard/incubator-superset/superset/migrations/versions/1a48a5411020_adding_slug_to_dash.py
# Compiled at: 2019-01-19 16:19:59
# Size of source mod 2**32: 1384 bytes
"""adding slug to dash

Revision ID: 1a48a5411020
Revises: 289ce07647b
Create Date: 2015-12-04 09:42:16.973264

"""
revision = '1a48a5411020'
down_revision = '289ce07647b'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('dashboards', sa.Column('slug', sa.String(length=255), nullable=True))
    try:
        op.create_unique_constraint('idx_unique_slug', 'dashboards', ['slug'])
    except:
        pass


def downgrade():
    op.drop_constraint(None, 'dashboards', type_='unique')
    op.drop_column('dashboards', 'slug')